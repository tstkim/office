# 필요한 라이브러리 불러오기
import time  # 시간을 다루기 위한 도구
from datetime import datetime  # 날짜와 시간을 다루기 위한 도구
import ssl  # 인터넷 보안과 관련된 문제를 해결하기 위한 도구
import requests  # 인터넷에서 데이터를 가져오기 위한 도구
from bs4 import BeautifulSoup as bs  # 인터넷에서 가져온 데이터를 쉽게 읽고 쓸 수 있게 도와주는 도구
import os  # 운영체제와 상호작용하기 위한 도구
import shutil  # 파일과 디렉토리를 복사하거나 이동하기 위한 도구
import re  # 정규 표현식을 사용하여 텍스트를 검색하고 수정하기 위한 도구
import openpyxl  # 엑셀 파일을 읽고 쓰기 위한 도구
from PIL import Image, ImageDraw, ImageFont  # 이미지를 처리하기 위한 도구

# Selenium 라이브러리 불러오기
from selenium import webdriver  # 웹 브라우저를 제어하기 위한 도구
from selenium.webdriver.common.by import By  # HTML 요소를 찾기 위한 방법을 제공하는 도구
from selenium.webdriver.chrome.service import Service  # Chrome 웹드라이버 서비스를 관리하는 도구
from selenium.webdriver.chrome.options import Options  # Chrome 웹드라이버의 옵션을 설정하는 도구
from webdriver_manager.chrome import ChromeDriverManager  # Chrome 웹드라이버를 자동으로 설치하고 업데이트하는 도구
from selenium.webdriver.common.keys import Keys  # 키보드 키를 사용하기 위한 도구
from selenium.webdriver.support.ui import WebDriverWait  # 웹 페이지가 로드될 때까지 기다리는 도구
from selenium.webdriver.support import expected_conditions as EC  # 특정 조건이 만족될 때까지 기다리는 도구

# 작업 시작 시간 기록
now = datetime.now()  # 현재 시간을 기록
start_time = time.time()  # 작업 시작 시간을 기록
print("택수님 ! 작업을 시작할께요.. 조금만 기다려주세요*^.^*")  # 작업 시작 알림

# SSL 오류 방지 설정
ssl._create_default_https_context = ssl._create_unverified_context

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
chrome_service = Service(ChromeDriverManager().install())  # Chrome 웹드라이버를 자동으로 다운로드하고 설정
chrome_options = Options()
chrome_options.add_argument('--headless')  # 브라우저 창을 띄우지 않도록 설정 (백그라운드에서 실행)
chrome_options.add_argument('--disable-gpu')  # GPU(그래픽 처리 장치)를 사용하지 않도록 설정

# 웹드라이버 시작
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)  # Chrome 웹드라이버를 시작
wait = WebDriverWait(driver, 5)  # 웹 페이지가 로드될 때까지 최대 5초 기다림

try:
    # 로그인 페이지로 이동
    driver.get('https://dawoori-sports.kr/member/login')  # 웹사이트의 로그인 페이지로 이동

    # 로그인 정보 입력
    userid_input = driver.find_element(By.NAME, 'userid')  # 사용자 아이디 입력란을 찾음
    password_input = driver.find_element(By.NAME, 'password')  # 사용자 비밀번호 입력란을 찾음
    userid_input.send_keys('flowing')  # 아이디 입력란에 아이디 입력
    password_input.send_keys('q6160q6160q')  # 비밀번호 입력란에 비밀번호 입력

    # 엔터 키로 로그인
    password_input.send_keys(Keys.ENTER)  # 비밀번호 입력란에서 엔터 키를 누름

    # 로그인 완료 대기
    time.sleep(5)  # 충분한 대기 시간을 줌

    # 페이지 범위 설정
    start_page = 1  # 시작 페이지 번호
    end_page = 1    # 끝 페이지 번호

    # 페이지 반복 처리
    for page in range(start_page, end_page + 1):
        # 각 페이지로 이동
        url = f'https://dawoori-sports.kr/goods/catalog?page={page}&searchMode=catalog&category=c0019&per=20&filter_display=lattice&code=0019'
        driver.get(url)

        # 페이지 로드 대기
        time.sleep(5)  # 페이지가 완전히 로드될 때까지 대기

        # 페이지 내용 파싱 (HTML 분석)
        page_source = driver.page_source  # 페이지의 HTML 소스를 가져옴
        soup = bs(page_source, 'html.parser')  # BeautifulSoup을 사용하여 HTML 소스를 파싱



    # 사이트의 기본 URL
    base_url = 'https://dawoori-sports.kr'  # 사이트의 기본 URL

    # 상품명과 가격 추출 및 저장
    product_names = soup.find_all('span', class_='name')  # HTML 소스에서 'span' 태그 중 클래스가 'name'인 모든 요소를 찾음
    for product in product_names:  # 찾은 모든 상품명 요소에 대해 반복
        product_name = product.get_text(strip=True)
        product_link = product.find_parent('a')['href']  # 상품의 링크 추출
        if not product_link.startswith('http'):  # 상대 경로를 절대 경로로 변환
            product_link = base_url + product_link

        # 상품 페이지로 이동
        driver.get(product_link)
        time.sleep(3)  # 페이지 로드 대기

        # 페이지 내용 파싱 (HTML 분석)
        product_page_source = driver.page_source  # 상품 페이지의 HTML 소스를 가져옴
        product_soup = bs(product_page_source, 'html.parser')  # BeautifulSoup을 사용하여 HTML 소스를 파싱

        # 가격 추출 및 설정
        product_price_element = product_soup.find('p', class_='org_price')
        if product_price_element:
            original_price = product_price_element.find('span', class_='num').get_text(strip=True)
            original_price = float(original_price.replace(',', ''))  # 쉼표 제거 후 숫자로 변환

            # 가격 인상률 설정 (조정 가능)
            priceR = 1.1  # 예: 10% 인상 (필요에 따라 조정 가능)
            adjusted_price = original_price * priceR  # 가격 인상률 적용

            # 상품명과 변경된 가격을 출력
            print(f"상품명: {product_name}")
            print(f"변경된 가격: {adjusted_price:.2f} 원")
        else:
            print(f"상품명: {product_name}")
            print("가격 정보를 찾을 수 없음")


except Exception as e:
    print(f"오류 발생: {e}")  # 오류가 발생하면 오류 메시지를 출력

finally:
    # 웹드라이버 종료
    driver.quit()  # 웹드라이버 종료

# 현재 시간을 출력
print(now)

# 엑셀 파일 저장
wb.save('C:/Users/ME/Pictures/' + str(now)[11:13] + str(now)[14:16] + '.xlsx')  # 엑셀 파일을 저장
print("크롤링 성공")

# 작업에 총 몇 초가 걸렸는지 출력
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
