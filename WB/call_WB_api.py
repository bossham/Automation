import os
import requests
import pandas as pd
from indicator_codes import indicator_codes


# 공통 요청 매개변수 설정
country_code = 'all'  
format_type = 'json'  
per_page = 500  

for indicator_code in indicator_codes:

    url = f'http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?format={format_type}&per_page={per_page}'

    response = requests.get(url)
    data = response.json()

    # 전체 페이지 수 확인 및 데이터 수집
    if len(data) > 1 and isinstance(data[0], dict):
        total_pages = data[0]['pages']
        
        records = []
        for page in range(1, total_pages + 1):
            paginated_url = f'{url}&page={page}'
            response = requests.get(paginated_url)
            page_data = response.json()

            if len(page_data) > 1 and isinstance(page_data[1], list):
                for item in page_data[1]:
                    records.append({
                        'Country Name': item['country']['value'],
                        'Year': item['date'],
                        'Value': item['value']
                    })


        df = pd.DataFrame(records)


        # 파일 저장 경로 설정
        folder_path = 'C:/Users/정지현/automation/WB_Data'
        csv_file_name = f'{indicator_code}.csv'
        csv_file_path = os.path.join(folder_path, csv_file_name)


        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
            except Exception as e:
                print(f"Failed to create directory {folder_path}. Error: {e}")
                # 폴더 생성 실패 시, 추가 작업 없이 종료
                exit()


        try:
            df.to_csv(csv_file_path, index=False)
            print(f"Data for {indicator_code} saved to {csv_file_path}")
        except Exception as e:
            print(f"Failed to save data for {indicator_code} to {csv_file_path}. Error: {e}")
