import requests
from bs4 import BeautifulSoup
import csv

years = [2019,2020,2021,2022,2023,2024]
months = list(range(1,13))

months = [str(x).zfill(2) for x in months]
base_url = 'https://www.hanyang-u.hs.kr/?c=C01/C12/C121&sort=d_regis&orderby=desc&uid=&nyear={}&nmonth={}&nday=28'

for year in years:
    for month in months:
        menu_info = []
        # 웹페이지 URL
        url = base_url.format(year, month)

        # HTTP GET 요청
        response = requests.get(url)

        # 요청이 성공했는지 확인
        if response.status_code == 200:
            # BeautifulSoup 객체 생성
            soup = BeautifulSoup(response.content, 'html.parser')

            # 텍스트 가져오기
            text_elements = soup.select('tbody > tr > td')
            for text in text_elements:
                menu_info.append(text.text)

            csv_file = 'hanyang_info/' + f'{year}_{month}.csv'
            with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)

                for menu in menu_info:
                    writer.writerow([menu])
                # writer.writerow(['날짜', '구분', '이미지 URL'])  # 헤더를 작성합니다.
                # writer.writerows([menu_info])  # 데이터를 CSV 파일에 작성합니다.

            print(f'CSV 파일 {csv_file}이(가) 성공적으로 생성되었습니다.')


        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
