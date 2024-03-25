import requests
import pandas as pd

def fetch_all_indicators(url):
    indicators = []
    response = requests.get(url)
    data = response.json()

    if len(data) > 1 and isinstance(data[0], dict):
        total_pages = data[0]['pages']  # 전체 페이지 수
        for page in range(1, total_pages + 1):
            paginated_url = f"{url}&page={page}"
            response = requests.get(paginated_url)
            page_data = response.json()

            if len(page_data) > 1 and isinstance(page_data[1], list):
                for item in page_data[1]:
                    indicators.append({
                        'Indicator ID': item['id'],
                        'Name': item['name'],
                        'Description': item['sourceNote']
                    })
    return indicators


base_url = "http://api.worldbank.org/v2/indicator?format=json&per_page=500"
indicators = fetch_all_indicators(base_url)


df = pd.DataFrame(indicators)
print(df.head())


csv_file_path = 'C:/Users/정지현/automation/WB/world_bank_indicators_all.csv'
df.to_csv(csv_file_path, index=False)
print(f"Indicator list saved to {csv_file_path}")
