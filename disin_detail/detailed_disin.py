import logging
from typing import Dict, List, Optional
import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
CONFIG = {
    'SERVICE_KEY': 'i4kidk21c3X/hLkySwIiPJ8aTr1xRqQ/CWnluHr1zG2jx1LUBZrsfheuojj5ZlO79XhfL0gAEfmrz3TqpVWidg==',
    'BASE_URL': 'http://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService03/getDrugPrdtPrmsnDtlInq02',
    'INPUT_FILE': '../disin_basic/disinfectants.csv',
    'OUTPUT_FILE': 'detailed_disin.csv',
    'MAX_WORKERS': 5,
    'BATCH_SIZE': 50
}

class DrugInfoScraper:
    def __init__(self):
        self.session = self._create_session()
        self.fields_mapping = {
            'ITEM_SEQ': '품목기준코드',
            'ITEM_NAME': '제품명',
            'ENTP_NAME': '기업명',
            'ITEM_PERMIT_DATE': '품목허가일자',
            'CNSGN_MANUF': '위탁제조업체',
            'ETC_OTC_CODE': '전문일반',
            'CHART': '성상',
            'BAR_CODE': '표준코드',
            'MATERIAL_NAME': '원료성분',
            'EE_DOC_ID': '효능효과',
            'UD_DOC_ID': '용법용량',
            'NB_DOC_ID': '주의사항',
            'INSERT_FILE': '첨부문서',
            'STORAGE_METHOD': '저장방법',
            'VALID_TERM': '유효기간',
            'REEXAM_TARGET': '재심사대상',
            'REEXAM_DATE': '재심사기간',
            'PACK_UNIT': '포장단위',
            'EDI_CODE': '보험코드',
            'DOC_TEXT': '제조방법',
            'PERMIT_KIND_NAME': '허가/신고구분',
            'ENTP_NO': '업체허가번호',
            'MAKE_MATERIAL_FLAG': '완제/원료구분',
            'NEWDRUG_CLASS_NAME': '신약',
            'INDUTY_TYPE': '업종구분',
            'CANCEL_DATE': '취소일자',
            'CANCEL_NAME': '상태',
            'CHANGE_DATE': '변경일자',
            'NARCOTIC_KIND_CODE': '마약종류코드',
            'GBN_NAME': '변경이력',
            'TOTAL_CONTENT': '총량',
            'EE_DOC_DATA': '효능효과데이터',
            'UD_DOC_DATA': '용법용량데이터',
            'NB_DOC_DATA': '주의사항데이터',
            'PN_DOC_DATA': '주의사항전문데이터',
            'MAIN_ITEM_INGR': '유효성분',
            'INGR_NAME': '첨가제',
            'ATC_CODE': 'ATC코드'
        }

    @staticmethod
    def _create_session() -> requests.Session:
        """Create a session with retry strategy."""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def parse_item(self, item) -> Dict[str, Optional[str]]:
        """Parse a single item from the API response."""
        result = {}
        for eng_field, kor_field in self.fields_mapping.items():
            try:
                field_data = item.find(eng_field)
                result[kor_field] = field_data.get_text() if field_data else None
            except AttributeError:
                result[kor_field] = None
        return result

    def fetch_drug_info(self, item_seq: str) -> Dict[str, Optional[str]]:
        """Fetch information for a single drug item."""
        try:
            params = {
                'serviceKey': CONFIG['SERVICE_KEY'],
                'pageNo': '1',
                'numOfRows': '1',
                'item_seq': item_seq
            }
            
            response = self.session.get(CONFIG['BASE_URL'], params=params)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'lxml-xml')
            items = soup.find_all("item")
            
            if items:
                return self.parse_item(items[0])
            return {field: None for field in self.fields_mapping.values()}
            
        except Exception as e:
            logger.error(f"Error fetching data for item {item_seq}: {str(e)}")
            return {field: None for field in self.fields_mapping.values()}

    def process_batch(self, item_seqs: List[str]) -> List[Dict[str, Optional[str]]]:
        """Process a batch of item sequences using ThreadPoolExecutor."""
        with ThreadPoolExecutor(max_workers=CONFIG['MAX_WORKERS']) as executor:
            return list(executor.map(self.fetch_drug_info, item_seqs))

def main():
    try:
        logger.info("Starting drug information collection process...")
        
        # Read input data
        df = pd.read_csv(CONFIG['INPUT_FILE'])
        item_seqs = df['품목기준코드'].astype(str).tolist()
        
        scraper = DrugInfoScraper()
        all_results = []
        
        # Process in batches
        total_batches = (len(item_seqs) + CONFIG['BATCH_SIZE'] - 1) // CONFIG['BATCH_SIZE']
        for i in range(0, len(item_seqs), CONFIG['BATCH_SIZE']):
            batch = item_seqs[i:i + CONFIG['BATCH_SIZE']]
            logger.info(f"Processing batch {(i // CONFIG['BATCH_SIZE']) + 1}/{total_batches}")
            batch_results = scraper.process_batch(batch)
            all_results.extend(batch_results)
        
        # Convert to DataFrame and save
        detailed_disin = pd.DataFrame(all_results)
        detailed_disin.to_csv(CONFIG['OUTPUT_FILE'], index=False, encoding='utf-8')
        logger.info(f"Data successfully saved to {CONFIG['OUTPUT_FILE']}")
        
    except Exception as e:
        logger.error(f"An error occurred during execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()