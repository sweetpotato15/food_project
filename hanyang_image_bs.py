import time
import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve # 이미지를 저장할 때 사용
 

## 1) 모든 페이지에 있는 uid 가져와서 image_uid 에 저장
base_url = 'https://www.hanyang-u.hs.kr/?c=C01/C12/C122&sort=d_regis&orderby=desc&p={}' 
base_src = 'https://www.hanyang-u.hs.kr/?c=C01/C12/C122&p=2&sort=d_regis&orderby=desc&uid={}'
n = 1

image_uid = []
image_info = []
for page in range(1,72):  
    try:
        url = base_url.format(page)
        response = requests.post(url)
    
        soup = BeautifulSoup(response.content, 'html.parser')
        images = soup.find_all('div',class_='sbjx')

        for i in images:
            uid = i.a['href'].split('uid=')[-1]
            image_uid.append(uid)
        
        for i in images:
            text = i.text.strip()
            text = text.replace(' ','')
            text = text.replace('.','_')
            text = text.replace('?','')
            image_info.append(text[:15])

    except Exception as ex: # 이미지가 없는 경우 종료
        print(f" 크롤링 완료{ex}")
        break
print('url_uid 완료')
print(len(image_uid))
print(len(image_info))

# 2) 해당 uid 타고 이미지 있는 url 들어가서 src 얻기
image_src = []
for uid in image_uid:
    try:
        url = base_src.format(uid)
        response = requests.post(url)
    
        soup = BeautifulSoup(response.content, 'html.parser')
        div_tags = soup.find('div',class_='attach')
        img_src = div_tags.img['src']
        image_src.append(img_src)
        # if img_src.endswith('png') is False: # png형식의 파일은 저장하지 않는다. 
        #     image_src.append(img_src) # 이미지의 source 주소를 가져와 imgurl list에 추가한다

    except Exception as ex: # 이미지가 없는 경우 종료
        image_src.append('')
        print(f" 2크롤링 완료{ex}")
        continue

print('src 완료')
print(len(image_src))

# 3) image_src에 해당하는 이미지 다운로드 받기
for i, src in enumerate(image_src):
    if src:
        urlretrieve(src, "hanyang_image/" + f'{image_info[i]}' + ".jpg") 

