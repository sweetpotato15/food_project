from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import requests
import os
import re
import urllib.request

image_uids = []
image_info = []

## 1) 초기화면에서 image 별 uid 찾아서 image_uids에 저장, image 별 중식/석식 날짜 정보를 image_info에 저장
for page in range(1, 4):
    
    try :
        url = f'https://www.hanyang-u.hs.kr/?c=C01/C12/C122&sort=d_regis&orderby=desc&p={page}'
        driver = webdriver.Chrome()
        driver.get(url)

        a_elements = driver.find_elements(By.XPATH,"//div[@class='gallery']//div[@class='sbjx']//a" )
        for idx, a in enumerate(a_elements):
            href = a.get_attribute('href')
            href = href.split('uid=')[-1]
            if href:
                image_uids.append(href)
                # print(f'이미지 링크 {idx+1} : {href}')

        
        response = requests.get(url)
        html = response.text
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = BeautifulSoup(html, 'html.parser')

        # 각 sbjx 클래스를 가진 요소를 찾아서 텍스트를 가져옴
        for sbjx in soup.find_all('div', class_='sbjx'):
            # sbjx 요소 안의 모든 텍스트를 합침
            span_text = sbjx.get_text(strip=True)        
            original_text = span_text.split()[0]
            original_text = original_text.replace('.','_')
            image_info.append(original_text)

    except Exception as e:
        print(f'에러 발생 : {e}')



## 2) 해당 uid url들어가서 이미지 src찾아서 image_srcs 에 저장
absolute_uid = 'https://www.hanyang-u.hs.kr/?c=C01/C12/C122&sort=d_regis&orderby=desc&uid='
image_srcs = []

for uid in image_uids:
    uid_url = absolute_uid + uid

    try :
        driver.get(uid_url)

        img_elements = driver.find_elements(By.XPATH, "//div[@class='attach']//img")
        for idx, a in enumerate(img_elements):
            src = a.get_attribute('src')
            if src:
                image_srcs.append(src)

    except Exception as e:
        print(f'에러 발생 : {e}')


## 3) 이미지 src에 있는 이미지 다운로드 해서 특정 폴더에 저장
folder_path = 'food_project/hanyang_food/'

for i, src in enumerate(image_srcs):
    try :
        response = requests.get(src)
        file_name = f"{image_info[i]}.jpg"
        file_path = os.path.join(folder_path, file_name)
        # 이미지 다운로드
        driver.get(src)
        time.sleep(2)  # 이미지가 로드될 때까지 대기
    
        # 이미지 저장
        # with open(file_path, 'wb') as f:
        #     f.write(response.content)
        urllib.request.urlretrieve(src,f'./hanyang_food/{image_info[i]}.jpg')

        print(f"{file_name} 다운로드 완료")

    except Exception as e:
        print(f"{image_info[i]}메뉴판 사진을 다운로드할 수 없습니다:", e)