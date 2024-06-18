import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# df = pd.read_csv("../disin_basic/disinfectants.csv")
df = pd.read_csv("../disin_basic/disinfectants.csv")

# Base URL for scraping
base_url = "https://nedrug.mfds.go.kr/pbp/CCBBB01/getItemDetail?itemSeq="

# Extract keys from the dataset
keys = df['품목기준코드']

# Function to scrape data for a single key
def scrape_data(key):
    try:
        # Construct the URL
        url = base_url + str(key)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the relevant table
        table = soup.find('table', class_='s-dr_table dr_table_type2')
        if not table:
            return []

        data = []
        for row in table.tbody.find_all('tr'):
            columns = row.find_all('td')
            if columns:
                year = columns[0].text.strip()
                sales = columns[1].text.strip()
                data.append({'code': key, 'year': year, 'sales': sales})
        
        return data
    except Exception as e:
        print(f"An error occurred with key {key}: {e}")
        return []

# Use ThreadPoolExecutor to scrape data in parallel
all_data = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(scrape_data, key) for key in keys]
    for future in as_completed(futures):
        all_data.extend(future.result())

# Create DataFrame from the collected data
df2 = pd.DataFrame(all_data)

# Extract relevant columns from the original dataset
df3 = df[['품목기준코드', '품목명', '업체명']]

# Merge the scraped data with the original data
df4 = df2.merge(df3, left_on='code', right_on='품목기준코드', how='left')

# Save the cleaned data to a CSV file
df4.to_csv("disin_sales_via_scraping.csv", index=False, mode="w")
