import requests
import pandas as pd
from bs4 import BeautifulSoup

# 소독제 품목기준코드 기준으로 추출
disinfectants = pd.read_csv("disin_basic/disinfectants.csv")['품목명']

#항목 parsing 함수작성하기
def parse():
    try:
        ENTRPS_PRMISN_NO = item.find("ENTRPS_PRMISN_NO").get_text()
        ENTRPS = item.find("ENTRPS").get_text()
        PRDUCT = item.find("PRDUCT").get_text()
        MTRAL_SN = item.find("MTRAL_SN").get_text()
        MTRAL_CODE = item.find("MTRAL_CODE").get_text()
        MTRAL_NM = item.find("MTRAL_NM").get_text()
        QNT = item.find("QNT").get_text()
        ITEM_SEQ = item.find("ITEM_SEQ").get_text()

        return {
            "업체허가번호":ENTRPS_PRMISN_NO,
            "업체명":ENTRPS,
            "제품명":PRDUCT,
            "일련번호":MTRAL_SN,
            "원료코드":MTRAL_CODE,
            "원료명":MTRAL_NM,
            "분량":QNT,
            "품목기준코드":ITEM_SEQ
             }
    except AttributeError as e:
        return {
            "업체허가번호":None,
            "업체명":None,
            "제품명":None,
            "일련번호":None,
            "원료코드":None,
            "원료명":None,
            "분량":None,
            "품목기준코드":None
             }

# 의약품 소독제 주성분 추출
service_key = 'i4kidk21c3X/hLkySwIiPJ8aTr1xRqQ/CWnluHr1zG2jx1LUBZrsfheuojj5ZlO79XhfL0gAEfmrz3TqpVWidg=='
url = 'http://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService02/getDrugPrdtMcpnDtlInq?'

active = []

for n in disinfectants:
    params = {'serviceKey' : service_key, 
              'pageNo' : '1', 
              'numOfRows' : '1',
              'Prduct' : n
            }
    
    r = requests.get(url, params)
    soup = BeautifulSoup(r.text, 'lxml-xml')
    items = soup.find_all("item")
    
    # row = []
    # row2 = []
    for item in items:
        active.append(parse())

disin_active = pd.DataFrame(active)
disin_active.to_csv("disin_active.csv", mode="w")
