# World Bank API 데이터

이 저장소는 월드뱅크 API를 사용하여 얻은 데이터를 담고 있습니다. 이 데이터는 월드뱅크에서 제공한 개방형 라이선스에 따라 사용되었습니다.

## 데이터 출처

이 데이터는 월드뱅크에서 제공한 API를 통해 수집되었습니다. 월드뱅크는 전 세계의 경제, 사회, 환경 등에 관한 데이터를 제공하는 국제기구입니다.

- 데이터 제공처: [월드뱅크](https://data.worldbank.org/)
- API 문서: [월드뱅크 개발자 정보](https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information)

## 라이선스

이 데이터는 Creative Commons Attribution 4.0 International (CC BY 4.0) 라이선스에 따라 제공됩니다. 따라서 데이터를 사용, 수정, 배포하는 경우 출처를 표시해야 합니다.

라이선스 전문은 [여기](https://creativecommons.org/licenses/by/4.0/legalcode)에서 확인할 수 있습니다.

## py 파일 설명
WB_API > Call_API > call_WB_api.py:
- 이 코드는 World Bank API에서 지정된 모든 국가의 다양한 경제 지표 데이터를 JSON 형식으로 다운로드 받아, 이를 CSV 파일로 변환하여 지정된 경로에 저장하는 과정을 자동화합니다.
- This code automates the process of downloading various economic indicator data for all specified countries from the World Bank API in JSON format, converting it into CSV files, and saving them to a designated path.

Compare_Indicators > Compare.py : 
- 이 코드는 World Bank API에서 최신 데이터를 엑셀 형식으로 다운로드하여 기존 데이터와 비교한 후, 변경된 값을 CSV 파일로 저장하는 과정을 자동화합니다. 변경 사항이 있으면 해당 변경 사항을 'changes_{indicator}.csv' 파일로 저장하고, 변경 사항이 없을 경우 저장하지 않습니다.
- This code automates the process of downloading the latest data in Excel format from the World Bank API, comparing it with existing data, and saving any changes in a CSV file. If there are changes, it saves them in a 'changes_{indicator}.csv' file; if there are no changes, it does not save the file.

end-to-end automation > all-process.py:
- 이 코드는 World Bank API를 통해 다양한 지표 데이터를 수집하고, 기존 데이터와 비교하여 변경된 부분을 탐지합니다. 변경된 데이터는 타임스탬프가 포함된 파일 이름으로 Updated_Value 폴더에 저장되며, 최신 데이터는 Call_Indicators 폴더에 저장됩니다.
- This code collects various indicator data through the World Bank API and detects any changes compared to existing data. Changes are saved in the Updated_Value folder with file names including timestamps, while the latest data is stored in the Call_Indicators folder.
