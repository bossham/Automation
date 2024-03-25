## 라이브러리 세팅
import os
import requests
import warnings
import pandas as pd
from io import BytesIO

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

## 다운받았던 파일 불러오기
old_file_path = 'C:/Users/정지현/automation/Compare_Indicators/Old_Indicators/CO2 emissions (kg per PPP $ of GDP).xlsx'
old_df = pd.read_excel(old_file_path, skiprows=3)

## 추후 csv 확장자로 변경필요 (WB_API/CALL_API 참고)
## 현재는 가지고 있는 파일이 xlsx 확장자라 어쩔 수 없이 동일 확장자로 비교
indicator = 'EN.ATM.CO2E.PP.GD'
url = f'http://api.worldbank.org/v2/en/indicator/{indicator}?downloadformat=excel'

response = requests.get(url) 

excel_data = BytesIO(response.content)
new_df = pd.read_excel(excel_data, sheet_name=0, skiprows=3)

new_file_path = f'C:/Users/정지현/automation/Compare_Indicators/WB_Data/{indicator}.csv'

folder_path = os.path.dirname(new_file_path)
os.makedirs(folder_path, exist_ok=True)

new_df.to_csv(new_file_path, index=False)

## 변경된 값이 있는지 비교 후 저장
old_df.columns = old_df.columns.map(str)
new_df.columns = new_df.columns.map(str)

old_df.set_index('Country Code', inplace=True)
new_df.set_index('Country Code', inplace=True)


changes = []

for year in old_df.columns[3:]:
    for country in old_df.index:

        old_value = old_df.at[country, year]
        new_value = new_df.at[country, year] if country in new_df.index else None
        
        if old_value != new_value:
            changes.append({
                'Country Code': country,
                'Year': year,
                'Old Value': old_value,
                'New Value': new_value
            })

if changes:
    changes_df = pd.DataFrame(changes)
    changes_file_path = f'C:/Users/정지현/automation/Compare_Indicators/Updated_Value/changes_{indicator}.csv'
    changes_df.to_csv(changes_file_path, index=False)
    print(f'Changes saved to {changes_file_path}')
else:
    print('No changes found. No file was saved.')