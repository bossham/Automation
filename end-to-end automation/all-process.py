import os
import requests
import numpy as np
import pandas as pd
from datetime import datetime
from indicator_codes import indicators

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"{path} 디렉토리를 생성했습니다.")

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def fetch_data(indicator_code):
    country_code = 'all'
    format_type = 'json'
    per_page = 500
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format={format_type}&per_page={per_page}'
    response = requests.get(url)
    data = response.json()
    
    records = []
    if len(data) > 1 and isinstance(data[0], dict) and 'pages' in data[0]:
        total_pages = data[0]['pages']
        for page in range(1, total_pages + 1):
            paginated_url = f'{url}&page={page}'
            response = requests.get(paginated_url)
            page_data = response.json()
            if len(page_data) > 1 and isinstance(page_data[1], list):
                records.extend([
                    {
                        'Country Name': item['country']['value'],
                        'Year': int(item['date']),
                        'Value': item['value'] if item['value'] is not None else None
                    } for item in page_data[1]
                ])
    return pd.DataFrame(records) if records else None

def compare_and_save_data(base_folder, update_folder, indicator_code, old_data_df):
    new_data_df = fetch_data(indicator_code)
    if new_data_df is not None:
        new_data_df.set_index(['Country Name', 'Year'], inplace=True)
        old_data_df.set_index(['Country Name', 'Year'], inplace=True)
        combined_df = pd.concat([old_data_df, new_data_df], axis=1, keys=['old', 'new'], join='outer')

        def check_changes(row):
            old_val = row[('old', 'Value')]
            new_val = row[('new', 'Value')]
            if pd.isna(old_val) and pd.isna(new_val):
                return False
            elif pd.isna(old_val) or pd.isna(new_val):
                return True
            else:
                return old_val != new_val
        changes = combined_df.apply(check_changes, axis=1)
        changes_df = combined_df[changes]

        if not changes_df.empty:
            changes_df['Old Value'] = changes_df['old', 'Value']
            changes_df['New Value'] = changes_df['new', 'Value']
            changes_df.reset_index(inplace=True)
            changes_df = changes_df[['Country Name', 'Year', 'Old Value', 'New Value']]

            ensure_directory_exists(update_folder)
            changes_file_path = os.path.join(update_folder, f'changes_{indicators[indicator_code]}_{get_timestamp()}.csv')
            changes_df.to_csv(changes_file_path, index=False)
            print(f'변경된 사항을 {changes_file_path}에 저장했습니다.')

            new_data_df.reset_index().to_csv(os.path.join(base_folder, f'{indicators[indicator_code]}.csv'), index=False)
            print(f'{indicators[indicator_code]} 데이터가 업데이트 되었습니다.')
        else:
            print(f'{indicators[indicator_code]} 지표에 대한 변경사항이 없어 파일이 저장되지 않았습니다.')
    else:
        print(f'{indicator_code} 지표 데이터를 가져오는 데 실패했습니다.')

def main():
    # 경로 수정
    base_folder = 'C:/Users/정지현/Desktop/automation/end-to-end automation/Call_Indicators'
    update_folder = 'C:/Users/정지현/Desktop/automation/end-to-end automation/Updated_Value'
    
    ensure_directory_exists(base_folder)
    ensure_directory_exists(update_folder)
    
    for indicator_code in indicators:
        indicator_filename = f'{indicators[indicator_code]}.csv'
        old_file_path = os.path.join(base_folder, indicator_filename)
        
        if os.path.exists(old_file_path):
            old_data_df = pd.read_csv(old_file_path)
            compare_and_save_data(base_folder, update_folder, indicator_code, old_data_df)
        else:
            print(f'{indicators[indicator_code]}에 대한 기존 데이터가 없습니다. 새 데이터를 가져오는 중...')
            new_data = fetch_data(indicator_code)
            if new_data is not None:
                new_data.to_csv(old_file_path, index=False)
                print(f'{indicators[indicator_code]}의 초기 데이터를 저장했습니다.')

if __name__ == '__main__':
    main()
