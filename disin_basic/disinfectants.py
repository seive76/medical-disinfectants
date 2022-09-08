import requests
import pandas as pd
from bs4 import BeautifulSoup

#파싱후 출력 항목 추출 함수
def parse():
    try:
        ITEM_SEQ = item.find("ITEM_SEQ").get_text()
        ITEM_NAME = item.find("ITEM_NAME").get_text()
        ENTP_NAME = item.find("ENTP_NAME").get_text()
        ITEM_PERMIT_DATE = item.find("ITEM_PERMIT_DATE").get_text()
        INDUTY = item.find("INDUTY").get_text()
        PRDLST_STDR_CODE = item.find("PRDLST_STDR_CODE").get_text()
        SPCLTY_PBLC = item.find("SPCLTY_PBLC").get_text()
        PRDUCT_TYPE = item.find("PRDUCT_TYPE").get_text()
        PRDUCT_PRMISN_NO = item.find("PRDUCT_PRMISN_NO").get_text()
        ITEM_INGR_NAME = item.find("ITEM_INGR_NAME").get_text()
        ITEM_INGR_CNT = item.find("ITEM_INGR_CNT").get_text()
        PERMIT_KIND_CODE = item.find("PERMIT_KIND_CODE").get_text()
        CANCEL_DATE = item.find("CANCEL_DATE").get_text()
        CANCEL_NAME = item.find("CANCEL_NAME").get_text()
        BIG_PRDT_IMG_URL = item.find("BIG_PRDT_IMG_URL").get_text()
        ENTP_SEQ = item.find("ENTP_SEQ").get_text()
        ENTP_NO = item.find("ENTP_NO").get_text()
        EDI_CODE = item.find("EDI_CODE").get_text()
        return {
            "품목기준코드":ITEM_SEQ,
            "품목명":ITEM_NAME,
            "업체명":ENTP_NAME,
            "품목허가일자":ITEM_PERMIT_DATE,
            "업종":INDUTY,
            "품목일련번호":PRDLST_STDR_CODE,
            "전문/일반":SPCLTY_PBLC,
            "분류명":PRDUCT_TYPE,
            "품목허가번호":PRDUCT_PRMISN_NO,
            "주성분":ITEM_INGR_NAME,
            "주성분수":ITEM_INGR_CNT,
            "신고/허가":PERMIT_KIND_CODE,
            "취하일자":CANCEL_DATE,
            "취하구분":CANCEL_NAME,
            "이미지":BIG_PRDT_IMG_URL,
            "업일련번호": ENTP_SEQ,
            "업허가번호": ENTP_NO,
            "보험코드": EDI_CODE
        }
    except AttributeError as e:
        return {
            "품목기준코드":None,
            "품목명":None,
            "업체명":None,
            "품목허가일자":None,
            "업종":None,
            "품목일련번호":None,
            "전문/일반":None,
            "분류명":None,
            "품목허가번호":None,
            "주성분":None,
            "주성분수":None,
            "신고/허가":None,
            "취하일자":None,
            "취하구분":None,
            "이미지":None,
            "업일련번호":None,
            "업허가번호":None,
            "보험코드":None
        }

# 공공데이터 API 접속 url & 기본정보 파라미터
url = 'http://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService02/getDrugPrdtPrmsnInq02?'

# 공공데이터 service key
service_key = 'i4kidk21c3X/hLkySwIiPJ8aTr1xRqQ/CWnluHr1zG2jx1LUBZrsfheuojj5ZlO79XhfL0gAEfmrz3TqpVWidg=='


# 공공데이터 의약품 기본정보 파싱 함수
def disin_parsing():
    row = []
    for n in range(521):
        params = {'serviceKey' : service_key, 
                  'pageNo' : n+1, 
                  'numOfRows' : '100'
                 }
    
        r = requests.get(url, params)
        soup = BeautifulSoup(r.text, 'lxml-xml')
        items = soup.find_all("item")
    
        for item in items:
            row.append(parse())

    df=pd.DataFrame(row)
    df=df[df['분류명']=='[07390]기타의 공중위생용약']
    df.to_csv("disinfectants.csv", mode="w")

