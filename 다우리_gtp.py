from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import re

# 웹드라이버 설정
options = Options()
options.headless = False  # 디버깅을 위해 False로 설정
options.add_argument("--disable-gpu")

# 크롬드라이버 자동 설치 및 초기화
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    # 로그인 페이지 접속
    login_url = "https://dawoori-sports.kr/member/login"
    driver.get(login_url)

    # 로그인 정보 입력
    username_field = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.NAME, 'userid'))
    )
    password_field = driver.find_element(By.NAME, 'password')

    username_field.send_keys('flowing')
    password_field.send_keys('q6160q6160q')

    # 로그인 버튼 클릭
    login_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn_resp.size_login1'))
    )
    login_button.click()

    # 로그인 후 페이지 로드 대기
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '.user_info'))
    )

    # 상품 페이지로 이동
    product_url = "https://dawoori-sports.kr/goods/catalog?page=1&searchMode=catalog&category=c0019&per=200&filter_display=lattice&code=0019"
    driver.get(product_url)

    # 상품 리스트 로드 대기
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#searchedItemDisplay > ul > li:nth-child(3) > ul > li.goods_name_area'))
    )

    # 상품명과 할인전 가격 추출
    product_details = []
    products = driver.find_elements(By.CSS_SELECTOR, '#searchedItemDisplay > ul > li')
    for product in products:
        name_element = product.find_element(By.CSS_SELECTOR, 'ul > li.goods_name_area')
        price_elements = product.find_elements(By.CSS_SELECTOR, 'ul > li')  # 모든 li 요소
        product_name = name_element.text.strip()
        
        # 할인전 가격 찾기 (가장 큰 숫자로 가정)
        original_price = ''
        max_price = 0
        for price_element in price_elements:
            price_text = price_element.text.strip()
            price_match = re.findall(r'(\d{1,3}(?:,\d{3})*)₩', price_text)
            for match in price_match:
                # 콤마 제거 후 정수 변환
                price = int(match.replace(',', ''))
                if price > max_price:
                    max_price = price
                    original_price = f"{price:,}"  # ₩ 기호 제거
        
        product_details.append((product_name, original_price))

    # 상품명과 할인전 가격 출력
    for name, price in product_details:
        print(f"상품명: {name}, 할인전 가격: {price}")

finally:
    # 드라이버 종료
    driver.quit()
