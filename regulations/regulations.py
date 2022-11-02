# Import packages
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

# defining the scope of the application
scope_app = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#credentials to the account
cred = ServiceAccountCredentials.from_json_keyfile_name('../keys/medical-disinfectants-e387e81a7562.json',scope_app) 

# authorize the clientsheet 
client = gspread.authorize(cred)

# get the sample of the Spreadsheet
sheet = client.open('Regulations') # The name of the sheet is Relations

# get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0) # the value, 0, indicates the first sheet

# get all the records of the data
records = sheet_instance.get_all_values()

# Convert it to the dataframe of Pandas'
df = pd.DataFrame(records)

# Export it to the directory in csv
df.to_csv('Regulations.csv', mode='w')

