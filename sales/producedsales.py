import logging
from urllib.request import urlopen 
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import List, Dict
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    'INPUT_FILE': '../disin_basic/disinfectants.csv',
    'OUTPUT_FILE': 'producedSales.csv',
    'BASE_URL': "https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq=",
    'REQUEST_DELAY': 1,  # seconds between requests
    'DIS_COLS': ['품목명', '업체명', '품목허가일자', '분류명', '주성분', '품목기준코드']
}

def load_disinfectant_data() -> pd.DataFrame:
    """Load the disinfectant product data from CSV."""
    try:
        return pd.read_csv(CONFIG['INPUT_FILE'])
    except FileNotFoundError:
        logger.error(f"Input file not found: {CONFIG['INPUT_FILE']}")
        raise

def scrape_sales_data(product_codes: List[str]) -> pd.DataFrame:
    """Scrape sales data for each product code."""
    sales_data = []
    
    for code in product_codes:
        try:
            url = CONFIG['BASE_URL'] + str(code)
            logger.info(f"Scraping data for product code: {code}")
            
            with urlopen(url) as response:
                soup = BeautifulSoup(response, "html.parser")
                
                for link in soup.find_all('th'):
                    if '실적' in link.text:
                        table = soup.find('table', class_='s-dr_table dr_table_type2')
                        if table and table.tbody:
                            for row in table.tbody.find_all('tr'):
                                columns = row.find_all('td')
                                if columns:
                                    year = columns[0].text.strip()
                                    sales = columns[1].text.strip()
                                    sales_data.append({
                                        'code': code,
                                        'year': year,
                                        'sales': sales
                                    })
            
            time.sleep(CONFIG['REQUEST_DELAY'])  # Be nice to the server
            
        except Exception as e:
            logger.error(f"Error scraping data for product code {code}: {str(e)}")
            continue
    
    return pd.DataFrame(sales_data)

def process_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """Process and clean the sales data."""
    # Clean sales data
    df['sales'] = df['sales'].apply(lambda x: re.sub(r'[^0-9]', "", str(x)))
    df['sales'] = df['sales'].astype(int)
    
    # Process year data
    df['year'] = df['year'].apply(lambda x: re.sub(r'[^0-9]', "", str(x)))
    df['year'] = pd.to_datetime(df['year'], format='%Y').dt.year
    
    return df

def main():
    try:
        # Load initial data
        logger.info("Loading disinfectant data...")
        disin_df = load_disinfectant_data()
        product_codes = disin_df['품목기준코드'].tolist()
        
        # Scrape sales data
        logger.info("Scraping sales data...")
        sales_df = scrape_sales_data(product_codes)
        
        # Process the data
        logger.info("Processing sales data...")
        sales_df = process_sales_data(sales_df)
        
        # Merge with original data
        logger.info("Merging data...")
        disin_df = disin_df[CONFIG['DIS_COLS']]
        final_df = pd.merge(sales_df, disin_df, 
                          how='left', 
                          left_on='code', 
                          right_on='품목기준코드')
        
        # Save results
        logger.info(f"Saving results to {CONFIG['OUTPUT_FILE']}...")
        final_df.to_csv(CONFIG['OUTPUT_FILE'], index=False)
        logger.info("Process completed successfully!")
        
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    main()