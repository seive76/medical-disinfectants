# Import packages
from urllib.request import urlopen 
from bs4 import BeautifulSoup
import pandas as pd

# df = pd.read_csv("../disin_basic/disinfectants.csv")
df = pd.read_csv("../disin_basic/disinfectants.csv")

# Website landing page to be scrapped from
path = "https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq="

# 'path'와 연결할 'keys'대상 생성 from 데이터셋, df
keys = df['품목기준코드']

# 스트립핑할 데이터셋 생성
df2 = pd.DataFrame(columns=['code', 'year', 'sales'])

# Loop over the keys
for key in keys:
    try:
        # Open the URL
        web = path + str(key)
        web = urlopen(web)
        soup = BeautifulSoup(web, "html.parser")
        
        for link in soup.find_all('th'):
            if '실적' in link.text:
                table = soup.find('table', class_= 's-dr_table dr_table_type2')

                # Collect data
                for row in table.tbody.find_all('tr'):
                    # Find all data for each column
                    columns = row.find_all('td')

                    if columns:
                        year = columns[0].text.strip()
                        sales = columns[1].text.strip()

                        df2 = df2.append({'code': key, 'year': year, 'sales': sales}, ignore_index=True)
    
    except Exception as e:
        print(f"An error occurred with key {key}: {e}")

# 데이터셋(df)에서 3개 컬럼만 추출, 새데이터셋 생성
df3 = df[['품목기준코드', '품목명', '업체명']]

# 데이터셋 'df2'에서 'df3'을 연결하고, 컬럼 '품목기준코드'기준으로 데이터 추출하기
df4 = df2.merge(df3, left_on = 'code', right_on = '품목기준코드', how= 'left')

# 정리된 데이터셋 csv 파일 만들기
df4.to_csv("disin_sales_via_scraping.csv", mode = "a")

