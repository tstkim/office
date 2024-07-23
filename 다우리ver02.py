import time
from datetime import datetime
import ssl
import requests
from bs4 import BeautifulSoup as bs
import os
import shutil
import re
import openpyxl
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request

# 작업 시작 시간 기록
now = datetime.now()  # 현재 시간을 기록
start_time = time.time()  # 작업 시작 시간을 기록
print("택수님 ! 작업을 시작할께요.. 조금만 기다려주세요*^.^*")  # 작업 시작 알림
tdate = now.strftime("%Y%m%d%H%M")
code = "dawoori"  # 적절하게 설정하세요

# SSL 오류 방지 설정
ssl._create_default_https_context = ssl._create_unverified_context

# 폴더 생성
path_a = f'C:/Users/ME/Pictures/{tdate}{code}'
path_b = f'{path_a}/cr'
path_c = f'{path_a}/output'
if os.path.exists(path_a):
    shutil.rmtree(path_a)
os.makedirs(path_b)
os.makedirs(path_c)

# 엑셀 파일 설정
wb = openpyxl.Workbook()
sheet = wb.active
sheet.append([
    "업체상품코드", "모델명", "브랜드", "제조사", "원산지", "상품명", "홍보문구", "요약상품명", 
    "카테고리코드", "사용자분류명", "한줄메모", "시중가", "원가", "표준공급가", "판매가", 
    "배송방법", "배송비", "구매수량", "과세여부", "판매수량", "이미지1URL", "이미지2URL", 
    "이미지3URL", "이미지4URL", "GIF생성", "이미지6URL", "이미지7URL", "이미지8URL", 
    "이미지9URL", "이미지10URL", "추가정보입력사항", "옵션타입", "옵션구분", "선택옵션", 
    "입력형옵션", "추가구매옵션", "상세설명", "추가상세설명", "광고/홍보", "제조일자", 
    "유효일자", "사은품내용", "키워드", "인증구분", "인증정보", "거래처", "영어상품명", 
    "중국어상품명", "일본어상품명", "영어상세설명", "중국어상세설명", "일본어상세설명", 
    "상품무게", "영어키워드", "중국어키워드", "일본어키워드", "생산지국가", 
    "전세계배송코드", "사이즈", "포장방법", "상품상세코드", "상품상세1", "상품상세2", 
    "상품상세3", "상품상세4", "상품상세5", "상품상세6", "상품상세7", "상품상세8", 
    "상품상세9", "상품상세10", "상품상세11", "상품상세12", "상품상세13", "상품상세14", 
    "상품상세15", "상품상세16", "상품상세17", "상품상세18", "상품상세19", "상품상세20", 
    "상품상세21", "상품상세22", "상품상세23", "상품상세24"
])

# ChromeDriver 자동 설치 및 업데이트 설정
chrome_service = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

# 웹드라이버 시작
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
wait = WebDriverWait(driver, 5)

# 이미지 파일명을 고유하게 만들기 위한 카운터
image_counter = 1

try:
    # 로그인 페이지로 이동
    driver.get('https://dawoori-sports.kr/member/login')
    userid_input = driver.find_element(By.NAME, 'userid')
    password_input = driver.find_element(By.NAME, 'password')
    userid_input.send_keys('flowing')
    password_input.send_keys('q6160q6160q')
    password_input.send_keys(Keys.ENTER)
    time.sleep(5)

    # 페이지 범위 설정
    start_page = 1
    end_page = 1

    # 페이지 반복 처리
    for page in range(start_page, end_page + 1):
        url = f'https://dawoori-sports.kr/goods/catalog?page={page}&searchMode=catalog&category=c0019&per=20&filter_display=lattice&code=0019'
        driver.get(url)
        time.sleep(5)
        soup = bs(driver.page_source, 'html.parser')
        base_url = 'https://dawoori-sports.kr'
        product_names = soup.find_all('span', class_='name')
        for product in product_names:
            product_name = product.get_text(strip=True)
            product_link = product.find_parent('a')['href']
            if not product_link.startswith('http'):
                product_link = base_url + product_link

            driver.get(product_link)
            time.sleep(3)
            product_soup = bs(driver.page_source, 'html.parser')
            product_price_element = product_soup.find('p', class_='org_price')
            if product_price_element:
                original_price = float(product_price_element.find('span', class_='num').get_text(strip=True).replace(',', ''))
                priceR = 1.1
                adjusted_price = original_price * priceR

                # 썸네일 이미지 주소 추출
                thumbnail_element = product_soup.find('div', class_='viewImgWrap').find('img')
                thumbnail_url = thumbnail_element['src'] if thumbnail_element else '썸네일 이미지 없음'
                if not thumbnail_url.startswith('http'):
                    thumbnail_url = base_url + thumbnail_url

                # 썸네일 이미지 저장 및 새로운 캔버스에 편집
                try:
                    urllib.request.urlretrieve(thumbnail_url, f'{path_b}/{len(sheet["A"])}_cr.jpg')
                    im = Image.open(f'{path_b}/{len(sheet["A"])}_cr.jpg')
                    im = im.resize((400, 400))

                    # 새로운 캔버스 생성
                    image = Image.new("RGB", (600, 600), "white")
                    grayg = Image.new("RGB", (600, 100), (56, 56, 56))  # 아래 검정색 바탕띠
                    image.paste(grayg, (0, 500))

                    redg = Image.new("RGB", (150, 150), (255, 61, 70))  # 위 빨간색 바탕띠
                    image.paste(redg, (440, 0))
                    
                    nameFont = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 65)
                    label = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 40)
                    
                    text1 = product_name.replace("-", "")  # 파일명에 "-" 혹은 특수문자가 있으면 오류가 난다
                    ImageDraw.Draw(image).text((10, 510), text1, font=nameFont, fill="white", stroke_fill="black", stroke_width=2)
                    ImageDraw.Draw(image).text((460, 10), "S2B", font=nameFont, fill="white", stroke_fill="red", stroke_width=2)
                    ImageDraw.Draw(image).text((505, 95), "공식", font=label, fill="white", stroke_fill="red", stroke_width=1)
                    image.paste(im, (100, 100))

                    image.save(f'{path_b}/{len(sheet["A"])}_cr.jpg')
                    image.close()
                except (ValueError, urllib.error.HTTPError, urllib.error.URLError, FileNotFoundError) as e:
                    print(f"썸네일 이미지 처리 중 오류 발생: {e}")

                # 상세 페이지 이미지 저장 및 자르기
                try:
                    detail_images = product_soup.select('.goods_desc_contents .txc-image')
                    combined_image = None

                    for img_tag in detail_images:
                        img_url = base_url + img_tag['data-original']
                        img_path = f'{path_a}/detail_{image_counter}.jpg'  # 고유한 파일명 생성
                        urllib.request.urlretrieve(img_url, img_path)
                        jm = Image.open(img_path).convert("RGB")

                        if combined_image is None:
                            combined_image = jm
                        else:
                            combined_width = max(combined_image.width, jm.width)
                            combined_height = combined_image.height + jm.height
                            new_combined_image = Image.new("RGB", (combined_width, combined_height))
                            new_combined_image.paste(combined_image, (0, 0))
                            new_combined_image.paste(jm, (0, combined_image.height))
                            combined_image = new_combined_image

                        image_counter += 1  # 이미지 파일명 증가

                    if combined_image is not None:
                        width, height = combined_image.size
                        current_image_num = len(os.listdir(path_c)) // 10 + 1  # 현재 상품 번호 계산
                        for i in range(10):
                            crop_area = (0, height * (i * 0.1), width, height * ((i + 1) * 0.1))
                            cropped_img = combined_image.crop(crop_area)
                            cropped_img.save(f'{path_c}/{current_image_num}_{i + 1:03}.jpg')
                        combined_image.close()
                except (ValueError, urllib.error.HTTPError, urllib.error.URLError, FileNotFoundError) as e:
                    print(f"상세 페이지 이미지 처리 중 오류 발생: {e}")



                # 옵션 추출
                options = []
                for a in range(2, 20):
                    try:
                        option = product_soup.select_one(f"select[name='viewOptions[]'] option:nth-of-type({a})").get_text(strip=True).replace("\n", "").replace("  ", "")
                    except AttributeError:
                        option = "없음"
                    options.append(option)

                formatted_options = [f"{opt.replace(' (품절)', '').replace(',', '')}=={0 if '없음' in opt else '10000'}=10000=0=0=0=" for opt in options if "없음" not in opt]
                ppp = "[필수선택]\n" + "\n".join(formatted_options)
                if ppp.count("10000") == 1 or ppp.count("10000") == 0:
                    ppp = ""

                print(f"상품명: {product_name}")
                print(f"변경된 가격: {adjusted_price}")
                print(f"썸네일 이미지 URL: {thumbnail_url}")
                print(f"옵션: {ppp}")

                sheet.append([None, None, None, None, None, product_name, None, None, None, None, None, None, None, None, adjusted_price, None, None, None, None, None, thumbnail_url, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, ppp, None, None, None, None, None, None, None, None, None, None])
            else:
                print(f"상품명: {product_name}")
                print("가격 정보를 찾을 수 없음")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    driver.quit()

# 현재 시간을 출력
print(now)

# 엑셀 파일 저장
wb.save(f'C:/Users/ME/Pictures/{tdate}{code}.xlsx')
print("크롤링 성공")

# 작업에 총 몇 초가 걸렸는지 출력
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
