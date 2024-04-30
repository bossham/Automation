import os
import requests
import pandas as pd
from datetime import datetime
from indicator_codes import indicators

def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")

def get_timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def fetch_data(indicator_code):
    country_code = 'all'
    format_type = 'json'
    per_page = 500
    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format={format_type}&per_page={per_page}'
    response = requests.get(url)
    data = response.json()

    if len(data) > 1 and isinstance(data[0], dict):
        total_pages = data[0]['pages']
        records = []
        for page in range(1, total_pages + 1):
            paginated_url = f'{url}&page={page}'
            response = requests.get(paginated_url)
            page_data = response.json()

            if len(page_data) > 1 and isinstance(page_data[1], list):
                records.extend([
                    {
                        'Country Name': item['country']['value'],
                        'Year': int(item['date']),
                        'Value': item['value']
                    } for item in page_data[1]
                ])

        return pd.DataFrame(records) if records else None

def compare_and_save_data(base_folder, update_folder, indicator_code, old_data_df):
    new_data_df = fetch_data(indicator_code)
    if new_data_df is not None:
        old_data_df['Year'] = old_data_df['Year'].astype(int)
        comparison_df = old_data_df.merge(new_data_df, on=['Country Name', 'Year'], suffixes=('_old', '_new'))
        changes = comparison_df[comparison_df['Value_old'] != comparison_df['Value_new']]

        if not changes.empty:
            indicator_name = indicators.get(indicator_code, '알 수 없는 지표')
            timestamp = get_timestamp()
            changes_file_path = os.path.join(update_folder, f'changes_{indicator_name}_{timestamp}.csv')
            changes[['Country Name', 'Year', 'Value_old', 'Value_new']].to_csv(changes_file_path, index=False)
            print(f'Changes saved to {changes_file_path}')
            
            new_file_path = os.path.join(base_folder, f'{indicator_name}.csv')
            new_data_df.to_csv(new_file_path, index=False)
            print(f'Updated data saved for {indicator_name}')
        else:
            print('No changes found. New data was not saved.')
    else:
        print(f'Failed to fetch new data for {indicator_code}')

# 경로 설정
base_folder = 'C:/Users/정지현/Desktop/automation/end-to-end automation/Call_Indicators'
update_folder = 'C:/Users/정지현/Desktop/automation/end-to-end automation/Updated_Value'

for indicator_code in indicators:
    old_file_path = os.path.join(base_folder, f'{indicators[indicator_code]}.csv')
    if os.path.exists(old_file_path):
        old_data_df = pd.read_csv(old_file_path)
        compare_and_save_data(base_folder, update_folder, indicator_code, old_data_df)
    else:
        print(f"No existing data found for {indicators[indicator_code]}. Fetching new data...")
        new_data = fetch_data(indicator_code)
        if new_data is not None:
            ensure_directory_exists(base_folder)
            new_data.to_csv(old_file_path, index=False)
            print(f"Initial data saved for {indicators[indicator_code]}")