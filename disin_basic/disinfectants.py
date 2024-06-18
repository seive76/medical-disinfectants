import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

# Parsing function
def parse(item):
    try:
        return {
            "품목기준코드": item.find("ITEM_SEQ").get_text(),
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
    except AttributeError:
        return {
            "품목기준코드": None,
            "품목명": None,
            "업체명": None,
            "품목허가일자": None,
            "업종": None,
            "품목일련번호": None,
            "전문/일반": None,
            "분류명": None,
            "품목허가번호": None,
            "주성분": None,
            "주성분수": None,
            "신고/허가": None,
            "취하일자": None,
            "취하구분": None,
            "이미지": None,
            "업일련번호": None,
            "업허가번호": None,
            "보험코드": None
        }
    
# Fetch function
def fetch_data(page, service_key, url, product_types):
    params = {
        'serviceKey': service_key,
        'pageNo': page + 1,
        'numOfRows': '100'
    }
    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'lxml-xml')
        matches = []
        for item in soup.find_all('item'):
            if item.find('PRDUCT_TYPE').text in product_types:
                matches.append(parse(item))
        return matches
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []
    
# Main script
service_key = "i4kidk21c3X/hLkySwIiPJ8aTr1xRqQ/CWnluHr1zG2jx1LUBZrsfheuojj5ZlO79XhfL0gAEfmrz3TqpVWidg=="
url = "http://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService05/getDrugPrdtPrmsnInq05?"
product_types = ['[07390]기타의 공중위생용약', '[07320]방역용 살균소독제']
all_matches = []

# Use ThreadPoolExecutor to parallelize the requests
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_data, n, service_key, url, product_types) for n in range(600)]
    for future in as_completed(futures):
        all_matches.extend(future.result())

# Create DataFrame and save to CSV
df = pd.DataFrame(all_matches)
df.to_csv("disinfectants.csv", mode="w", index=False)