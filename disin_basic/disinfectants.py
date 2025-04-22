import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import logging
from typing import List, Dict, Optional, Set
import time
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry
from config import API_CONFIG
import json
from pathlib import Path
import hashlib
import urllib.parse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DisinfectantScraper:
    def __init__(self, service_key: str, url: str, product_types: List[str], max_retries: int = 3):
        self.service_key = service_key
        self.url = url
        self.product_types = product_types
        self.max_retries = max_retries
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)
        self.processed_pages: Set[int] = set()
        self.load_cache()
        
    def __enter__(self):
        self.session = requests.Session()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.save_cache()

    def get_cache_path(self, page: int) -> Path:
        """Generate cache file path for a page."""
        cache_key = hashlib.md5(f"{page}_{self.service_key}".encode()).hexdigest()
        return self.cache_dir / f"page_{cache_key}.json"

    def load_cache(self):
        """Load processed pages from cache."""
        try:
            for cache_file in self.cache_dir.glob("page_*.json"):
                if cache_file.stat().st_size > 0:
                    page_num = int(cache_file.stem.split('_')[1])
                    self.processed_pages.add(page_num)
        except Exception as e:
            logging.warning(f"Error loading cache: {e}")

    def save_cache(self):
        """Save processed pages to cache."""
        try:
            for page in self.processed_pages:
                cache_path = self.get_cache_path(page)
                with open(cache_path, 'w') as f:
                    json.dump({"page": page}, f)
        except Exception as e:
            logging.warning(f"Error saving cache: {e}")

    @sleep_and_retry
    @limits(calls=30, period=60)
    def fetch_page(self, page: int) -> Optional[List[Dict]]:
        """Fetch a single page with retry logic and caching."""
        if page in self.processed_pages:
            logging.debug(f"Page {page} already processed, skipping")
            return None

        # Decode the service key
        decoded_key = urllib.parse.unquote(self.service_key)
        
        params = {
            'serviceKey': decoded_key,
            'pageNo': str(page + 1),
            'numOfRows': '100',
            'type': 'xml'
        }
        
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(self.url, params=params, timeout=30)
                response.raise_for_status()
                
                # Log the response for debugging
                logging.debug(f"Response for page {page}: {response.text[:500]}...")
                
                # Check for API error messages
                root = ET.fromstring(response.text)
                result_code = root.find('.//resultCode')
                if result_code is not None and result_code.text != '00':
                    error_msg = root.find('.//resultMsg')
                    logging.error(f"API Error on page {page}: {error_msg.text if error_msg is not None else 'Unknown error'}")
                    return None
                
                soup = BeautifulSoup(response.text, 'lxml-xml')
                matches = []
                
                for item in soup.find_all('item'):
                    # Check if the item matches any of our product types
                    prduct_type = item.find('PRDUCT_TYPE')
                    if prduct_type is not None:
                        # Extract the numeric code from the product type
                        type_code = prduct_type.text.split(']')[0].strip('[')
                        if type_code in self.product_types:
                            parsed_item = self.parse_item(item)
                            if parsed_item:
                                matches.append(parsed_item)
                
                if matches:
                    self.processed_pages.add(page)
                    logging.info(f"Page {page}: Found {len(matches)} matches")
                else:
                    logging.warning(f"No matches found for page {page}")
                
                return matches
                
            except requests.RequestException as e:
                if attempt == self.max_retries - 1:
                    logging.error(f"Failed to fetch page {page} after {self.max_retries} attempts: {e}")
                    return None
                time.sleep(2 ** attempt)  # Exponential backoff
            except ET.ParseError as e:
                logging.error(f"XML parsing error on page {page}: {e}")
                return None
                
        return None

    def parse_item(self, item) -> Dict:
        """Parse a single item with error handling and validation."""
        try:
            parsed_data = {
                "품목기준코드": item.find("ITEM_SEQ").get_text().strip(),
                "품목명": item.find("ITEM_NAME").get_text(),
                "업체명": item.find("ENTP_NAME").get_text(),
                "품목허가일자": item.find("ITEM_PERMIT_DATE").get_text(),
                "업종": item.find("INDUTY").get_text(),
                "품목일련번호": item.find("PRDLST_STDR_CODE").get_text(),
                "전문/일반": item.find("SPCLTY_PBLC").get_text(),
                "분류명": item.find("PRDUCT_TYPE").get_text(),
                "품목허가번호": item.find("PRDUCT_PRMISN_NO").get_text(),
                "주성분": item.find("ITEM_INGR_NAME").get_text(),
                "주성분수": item.find("ITEM_INGR_CNT").get_text(),
                "신고/허가": item.find("PERMIT_KIND_CODE").get_text(),
                "취하일자": item.find("CANCEL_DATE").get_text(),
                "취하구분": item.find("CANCEL_NAME").get_text(),
                "이미지": item.find("BIG_PRDT_IMG_URL").get_text(),
                "업일련번호": item.find("ENTP_SEQ").get_text(),
                "업허가번호": item.find("ENTP_NO").get_text(),
                "보험코드": item.find("EDI_CODE").get_text()
            }
            
            # Validate required fields
            if not parsed_data["품목기준코드"]:
                logging.warning("Empty product code found")
                return None
            
            # Clean and validate data
            for key, value in parsed_data.items():
                if isinstance(value, str):
                    parsed_data[key] = value.strip()
            
            return parsed_data
        except AttributeError as e:
            logging.warning(f"Error parsing item: {e}")
            return None

    def scrape_all_pages(self, total_pages: int, max_workers: int = 10) -> List[Dict]:
        """Scrape all pages using thread pool with progress tracking and memory optimization."""
        all_matches = []
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Create a list of pages to process, excluding already processed ones
            pages_to_process = [p for p in range(total_pages) if p not in self.processed_pages]
            
            if not pages_to_process:
                logging.info("All pages have already been processed")
                return all_matches
                
            futures = {executor.submit(self.fetch_page, page): page for page in pages_to_process}
            
            with tqdm(total=len(pages_to_process), desc="Scraping pages") as pbar:
                for future in as_completed(futures):
                    page_num = futures[future]
                    try:
                        matches = future.result()
                        if matches:
                            all_matches.extend(matches)
                            # Save progress periodically
                            if len(all_matches) % 100 == 0:
                                self.save_progress(all_matches)
                    except Exception as e:
                        logging.error(f"Error processing page {page_num}: {e}")
                    pbar.update(1)
                    
                    # Update progress bar with estimated time remaining
                    elapsed = time.time() - start_time
                    pages_per_second = pbar.n / elapsed if elapsed > 0 else 0
                    if pages_per_second > 0:
                        remaining_pages = len(pages_to_process) - pbar.n
                        eta = remaining_pages / pages_per_second
                        pbar.set_postfix({"ETA": f"{eta:.1f}s"})
                    
        return all_matches

    def save_progress(self, matches: List[Dict]):
        """Save progress to a temporary file."""
        try:
            temp_df = pd.DataFrame(matches)
            temp_file = "disinfectants_temp.csv"
            temp_df.to_csv(
                temp_file,
                mode="w",
                index=False,
                encoding='utf-8-sig'
            )
            logging.info(f"Progress saved: {len(matches)} records")
        except Exception as e:
            logging.error(f"Error saving progress: {e}")

def main():
    # Load configuration
    load_dotenv()
    service_key = os.getenv('DATA_GO_KR_API_KEY')
    if not service_key:
        logging.error("API key not found in environment variables")
        return

    # Initialize scraper with context manager
    with DisinfectantScraper(
        service_key=service_key,
        url=API_CONFIG['base_url'],
        product_types=API_CONFIG['product_types']
    ) as scraper:
        try:
            logging.info("Starting data scraping...")
            all_matches = scraper.scrape_all_pages(
                total_pages=API_CONFIG['total_pages']
            )
            
            if all_matches:
                df = pd.DataFrame(all_matches)
                output_file = "disinfectants.csv"
                df.to_csv(
                    output_file,
                    mode="w",
                    index=False,
                    encoding='utf-8-sig'
                )
                logging.info(
                    f"Successfully saved {len(all_matches)} records to {output_file}"
                )
            else:
                logging.error("No data was scraped successfully")
                
        except Exception as e:
            logging.error(f"Error during scraping: {str(e)}")

if __name__ == "__main__":
    main()