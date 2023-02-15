from urllib.request import urlopen 
from bs4 import BeautifulSoup
import pandas as pd

# 소독제 등록 제품 가져오기
df = pd.read_csv("../disin_basic/disinfectants.csv")

# 소독제 품목기준코드 리스트 생성
keys = df['품목기준코드']

# 웹추출 빈 데이터프레임 생성
df = pd.DataFrame(columns = ['code', 'year', 'sales'])

# 웹사이트 url 주소
path = "https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq="

# 웹사이트 데이터 추출 - 소독제 제품별 랜딩페이지 접속 & Soup변환
for key in keys:
    web = path + str(key)
    web = urlopen(web)
    soup = BeautifulSoup(web, "html.parser")
    
    # 추출 objects 중 생산 소독제만 필터
    for link in soup.find_all('th'):
        if '생산실적' in link.text:
            table = soup.find('table', class_= 's-dr_table dr_table_type2')
            
            # 관련 테이블접속, 데이터 추출
            for row in table.tbody.find_all('tr'):
                # find all data for each column
                columns = row.find_all('td')

                if(columns != []):
                    year = columns[0].text.strip()
                    sales = columns[1].text.strip()

                    # sales 데이터프레임에 기입하기
                    df = df.append({'code': key ,'year': year, 'sales': sales}, ignore_index=True)

import re

# 세일즈 데이터 변환하기
df['sales'] = [re.sub(r'[^0-9]', "", sale) for sale in df.sales]
df['sales'] = [int(sale) for sale in df.sales]

# 연도 문자데이터 datetime 변환 & 연도변도
df['year'] = [re.sub(r'[^0-9]', "", yr) for yr in df.year]
df.year = [pd.to_datetime(int(yr),format='%Y') for yr in df.year]
df.year = pd.DatetimeIndex(df['year']).year

# 생산실적 데이터 추가 제품정보 업데이트 데이트셋 추출
disin = pd.read_csv('../disin_basic/disinfectants.csv')
dis_cols = ['품목명', '업체명', '품목허가일자', '분류명', '주성분', '품목기준코드']
disin = disin[dis_cols]

# 병합
df = pd.merge(df, disin, how = 'left', left_on='code', right_on='품목기준코드')

# 데이터 Export
df.to_csv('producedSales.csv', mode="w")