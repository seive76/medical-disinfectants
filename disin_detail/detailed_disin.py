import requests
import pandas as pd
from bs4 import BeautifulSoup

# 소독제 품목기준코드 기준으로 추출
item_seqs = pd.read_csv("../disin_basic/disinfectants.csv")['품목기준코드']

#항목 parsing 함수작성하기
def parse():
    try:
        ITEM_SEQ = item.find("ITEM_SEQ").get_text()
        ITEM_NAME = item.find("ITEM_NAME").get_text()
        ENTP_NAME = item.find("ENTP_NAME").get_text()
        ITEM_PERMIT_DATE = item.find("ITEM_PERMIT_DATE").get_text()
        CNSGN_MANUF = item.find("CNSGN_MANUF").get_text()
        ETC_OTC_CODE = item.find("ETC_OTC_CODE").get_text()
        CHART = item.find("CHART").get_text()
        BAR_CODE = item.find("BAR_CODE").get_text()
        MATERIAL_NAME = item.find("MATERIAL_NAME").get_text()
        EE_DOC_ID = item.find("EE_DOC_ID").get_text()
        UD_DOC_ID = item.find("UD_DOC_ID").get_text()
        NB_DOC_ID = item.find("NB_DOC_ID").get_text()
        INSERT_FILE = item.find("INSERT_FILE").get_text()
        STORAGE_METHOD = item.find("STORAGE_METHOD").get_text()
        VALID_TERM = item.find("VALID_TERM").get_text()
        REEXAM_TARGET = item.find("REEXAM_TARGET").get_text()
        REEXAM_DATE = item.find("REEXAM_DATE").get_text()
        PACK_UNIT = item.find("PACK_UNIT").get_text()
        EDI_CODE = item.find("EDI_CODE").get_text()
        DOC_TEXT = item.find("DOC_TEXT").get_text()
        PERMIT_KIND_NAME = item.find("PERMIT_KIND_NAME").get_text()
        ENTP_NO = item.find("ENTP_NO").get_text()
        MAKE_MATERIAL_FLAG = item.find("MAKE_MATERIAL_FLAG").get_text()
        NEWDRUG_CLASS_NAME = item.find("NEWDRUG_CLASS_NAME").get_text()
        INDUTY_TYPE = item.find("INDUTY_TYPE").get_text()
        CANCEL_DATE = item.find("CANCEL_DATE").get_text()
        CANCEL_NAME = item.find("CANCEL_NAME").get_text()
        CHANGE_DATE = item.find("CHANGE_DATE").get_text()
        NARCOTIC_KIND_CODE = item.find("NARCOTIC_KIND_CODE").get_text()
        GBN_NAME = item.find("GBN_NAME").get_text()
        TOTAL_CONTENT = item.find("TOTAL_CONTENT").get_text()
        EE_DOC_DATA = item.find("EE_DOC_DATA").get_text()
        UD_DOC_DATA = item.find("UD_DOC_DATA").get_text()
        NB_DOC_DATA = item.find("NB_DOC_DATA").get_text()
        PN_DOC_DATA = item.find("PN_DOC_DATA").get_text()
        MAIN_ITEM_INGR = item.find("MAIN_ITEM_INGR").get_text()
        INGR_NAME = item.find("INGR_NAME").get_text()
        ATC_CODE = item.find("ATC_CODE").get_text()

        return {
            "품목기준코드":ITEM_SEQ,
            "품목명":ITEM_NAME,
            "제품명":ENTP_NAME,
            "품목허가일자":ITEM_PERMIT_DATE,
            "위탁제조업체":CNSGN_MANUF,
            "전문일반":ETC_OTC_CODE,
            "성상":CHART,
            "표준코드":BAR_CODE,
            "원료성분":MATERIAL_NAME,
            "효능효과":EE_DOC_ID,
            "용법용량":UD_DOC_ID,
            "주의사항":NB_DOC_ID,
            "첨부문서":INSERT_FILE,
            "저장방법":STORAGE_METHOD,
            "유효기간":VALID_TERM,
            "재심사대상":REEXAM_TARGET,
            "재심사기간":REEXAM_DATE,
            "포장단위":PACK_UNIT,
            "보험코드":EDI_CODE,
            "제조방법":DOC_TEXT,
            "허가/신고구분":PERMIT_KIND_NAME,
            "업체허가번호":ENTP_NO,
            "완제/원료구분":MAKE_MATERIAL_FLAG,
            "신약":NEWDRUG_CLASS_NAME,
            "업종구분":INDUTY_TYPE,
            "취소일장":CANCEL_DATE,
            "상태":CANCEL_NAME,
            "변경일장":CHANGE_DATE,
            "마약종류코드":NARCOTIC_KIND_CODE,
            "변경이력":GBN_NAME,
            "총량":TOTAL_CONTENT,
            "효능효과데이터":EE_DOC_DATA,
            "용법용량데이터":UD_DOC_DATA,
            "주의사항데이터":NB_DOC_DATA,
            "주의상항전문데이터":PN_DOC_DATA,
            "유효성분":MAIN_ITEM_INGR,
            "첨가제":INGR_NAME,
            "ATC코드":ATC_CODE
        }
    except AttributeError as e:
        return {
            "품목기준코드":None,
            "품목명":None,
            "제품명":None,
            "품목허가일자":None,
            "위탁제조업체":None,
            "전문일반":None,
            "성상":None,
            "표준코드":None,
            "원료성분":None,
            "효능효과":None,
            "용법용량":None,
            "주의사항":None,
            "첨부문서":None,
            "저장방법":None,
            "유효기간":None,
            "재심사대상":None,
            "재심사기간":None,
            "포장단위":None,
            "보험코드":None,
            "제조방법":None,
            "허가/신고구분":None,
            "업체허가번호":None,
            "완제/원료구분":None,
            "신약":None,
            "업종구분":None,
            "취소일장":None,
            "상태":None,
            "변경일장":None,
            "마약종류코드":None,
            "변경이력":None,
            "총량":None,
            "효능효과데이터":None,
            "용법용량데이터":None,
            "주의사항데이터":None,
            "주의상항전문데이터":None,
            "유효성분":None,
            "첨가제":None,
            "ATC코드":None
             }

# 의약품 제품 허가정보 추출
service_key = 'i4kidk21c3X/hLkySwIiPJ8aTr1xRqQ/CWnluHr1zG2jx1LUBZrsfheuojj5ZlO79XhfL0gAEfmrz3TqpVWidg=='
url = 'http://apis.data.go.kr/1471000/DrugPrdtPrmsnInfoService02/getDrugPrdtPrmsnDtlInq01?'

detailed = []

for n in item_seqs:
    params = {'serviceKey' : service_key, 
              'pageNo' : '1', 
              'numOfRows' : '1',
              'item_seq' : n
            }
    
    r = requests.get(url, params)
    soup = BeautifulSoup(r.text, 'lxml-xml')
    items = soup.find_all("item")
    
    for item in items:
        detailed.append(parse())

# Convert to DataFrame
detailed_disin = pd.DataFrame(detailed)
detailed_disin.to_csv("detailed_disin.csv", mode="w")