from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

# WebDriver 옵션 설정 (Headless 모드로 설정)
options = Options()
options.headless = True


# WebDriver 초기화
driver = webdriver.Chrome(options=options)

# 웹 페이지 열기
url = 'https://www.hanyang-u.hs.kr/?c=C01/C12/C121&sort=d_regis&orderby=desc&uid=&nyear=2024&nmonth=06&nday=28'
driver.get(url)

# tbody > tr > text
# 정보 추출을 위한 CSS selector 정의
menu_boxes = driver.find_elements(By.CSS_SELECTOR, '.sbjx')

# 데이터 저장을 위한 리스트 초기화
data = []

# 정보 추출
for menu_box in menu_boxes:
    category = menu_box.find_element(By.CSS_SELECTOR, '.cat').text.strip()
    date_menu = menu_box.find_element(By.CSS_SELECTOR, 'a').text.strip()
    data.append([category, date_menu])

# WebDriver 종료
driver.quit()

# 추출한 데이터를 DataFrame으로 변환
df = pd.DataFrame(data, columns=['Category', 'Date_Menu'])
print(df)


# # CSV 파일로 저장
# csv_file_path = 'hanyang_menu.csv'
# df.to_csv(csv_file_path, index=False)

# print(f"CSV 파일이 저장되었습니다: {csv_file_path}")