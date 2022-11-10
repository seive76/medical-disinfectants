import pandas as pd

def merge():
    # Import all the sales records from the same directory
    df1 = pd.read_csv("medicalSales2017.csv")
    df2 = pd.read_csv("medicalSales2018.csv")
    df3 = pd.read_csv("medicalSales2019.csv")
    df4 = pd.read_csv("medicalSales2020.csv")
    df5 = pd.read_csv("medicalSales2021.csv")

    # Add a new column, year
    df1['year'] = 2017
    df2['year'] = 2018
    df3['year'] = 2019
    df4['year'] = 2020
    df5['year'] = 2021

    # Merge sales of years, 19, 20, 21 
    merged_01 = pd.concat([df3, df4, df5])

    # 2017년 데이터 열 이름 변경 to 국가, 포장단위, 금액(USD), 품명
    df1.rename(columns={'품명':'영문명', '한글명':'품명', '포장단위(규격)':'포장단위', ' 금액(US$)':' 금액(USD)', '제조국':'국가'}, inplace=True)

    # 2018년 열 이름 변경 to 국가, 포장단위, 금액(USD), 품명
    df2.rename(columns={'품명':'영문명', '한글품명':'품명', '금액(US$)':' 금액(USD)', '제조국':'국가'}, inplace=True)

    # Retrieve columns needed
    df1 = df1[['전문/일반','품명','국가', '포장단위', ' 금액(USD)', 'year' ]]
    df2 = df2[['전문/일반','품명','국가', '포장단위', ' 금액(USD)', 'year']]

    # Merge all the retrieved with merge_01
    df = pd.concat([df1, df2, merged_01])

    # Change columns names to a way to match with the sales data
    df.rename(columns={' 금액(USD)':'sales', '품명':'품목명'}, inplace=True)

    # Retrieve necessory columns 
    sales = df[['전문/일반', '품목명', '국가', '포장단위', 'sales', 'year']]

    # Define a formula that cleans the sales column ready to be converted to numbers
    def to_clean(price):
        price = price.replace(',','')
        price = price.replace('  - ','')
        price = price.replace(' ','')
        price = price.replace('-','')
        return price

    # Clean the sales records and convert to integer
    sales['sales'] = sales.sales.apply(to_clean)
    # sales['sales'] = sales.sales.astype(int)

    # Get rid of empty values
    sales = sales[sales['sales']!='']

    # Convert the year column to datetime type
    sales['year']= pd.to_datetime(sales['year'], format='%Y')

    # Export the sales records
    # sales.to_csv("mergedSales.csv", mode="w")

    sales.loc[(sales['품목명']=='페라세이프'), '품목명']="페라세이프(과붕산나트륨)"
    sales.loc[(sales['품목명']=='노코리즈액'), '품목명']='노코리즈액(과산화수소수30%)'
    sales.loc[(sales['품목명']=='싸이덱스오피에이액'), '품목명']='싸이덱스오피에이액(오토프탈알데하이드)'
    sales.loc[(sales['품목명']=='스테리스-20액'), '품목명']='스테리스-20액(35%과초산)'
    sales.loc[(sales['품목명']=='스테리스-40액'), '품목명']='스테리스-40액(35.5%과아세트산)'
    sales.loc[(sales['품목명']=='아세사이드액'), '품목명']='아세사이드액(저농도과초산평형혼합물)'
    sales.loc[(sales['품목명']=='페라스텔액'), '품목명']='페라스텔액(과초산4%)'
    sales.loc[(sales['품목명']=='에이치엠씨엔에프산'), '품목명']='에이치엠씨엔에프산(과탄산나트륨)'
    sales.loc[(sales['품목명']=='트리스텔스포리와입스앤폼'), '품목명']='트리스텔 스포리와입스앤폼'
    sales.loc[(sales['품목명']=='조양피에이에이15액'), '품목명']='조양피에이에이15액(과아세트산액)'

    # Export the cleaned sales records for the disinfectant segment
    sales.to_csv("mergingSales.csv", mode="w")

merge()