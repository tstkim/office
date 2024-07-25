from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import re
import time

# 드라이버 설정 함수
def setup_driver(headless=False):
    options = Options()
    options.headless = headless
    options.add_argument("--disable-gpu")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 로그인 함수
def login(driver, username, password, login_url):
    driver.get(login_url)
    try:
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'userid'))
        )
        password_field = driver.find_element(By.NAME, 'password')
        username_field.send_keys(username)
        password_field.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn_resp.size_login1'))
        )
        login_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.user_info'))
        )
    except (TimeoutException, NoSuchElementException):
        print("로그인 실패")
        driver.quit()
        return False
    return True

# 재시도 로직을 포함한 요소 찾기 함수
def find_elements_with_retry(driver, by, value, retries=3, delay=2):
    for attempt in range(retries):
        try:
            elements = driver.find_elements(by, value)
            if elements:
                return elements
        except StaleElementReferenceException:
            time.sleep(delay)
            driver.refresh()
    raise StaleElementReferenceException(f"Elements with {by}={value} not found after {retries} retries")

# 상품 정보 추출 함수
def scrape_product_details(driver, product):
    product_details = {}

    try:
        name_element = find_elements_with_retry(driver, By.CSS_SELECTOR, 'ul > li.goods_name_area')[0]
        product_details['product_name'] = name_element.text.strip()
    except (NoSuchElementException, StaleElementReferenceException):
        product_details['product_name'] = "추출 안됨"

    try:
        price_elements = find_elements_with_retry(driver, By.CSS_SELECTOR, 'ul > li')
        original_price = ''
        max_price = 0
        for price_element in price_elements:
            price_text = price_element.text.strip()
            price_match = re.findall(r'(\d{1,3}(?:,\d{3})*)₩', price_text)
            for match in price_match:
                price = int(match.replace(',', ''))
                if price > max_price:
                    max_price = price
                    original_price = f"{price:,}"
        product_details['original_price'] = original_price
    except NoSuchElementException:
        product_details['original_price'] = "추출 안됨"

    try:
        name_element.click()
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.goods_detail'))
        )
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        options = [opt.text.strip() for opt in soup.select('#sbSelector_44481999')]
        product_details['options'] = options if options else ["추출 안됨"]

        thumbnails = [thumb['src'] for thumb in soup.select('#goods_thumbs > div > div > img')]
        product_details['thumbnails'] = thumbnails if thumbnails else ["추출 안됨"]

        detail_page = [img['src'] for img in soup.select('#goods_contents_quick > div.goods_information_contents.goods_description > div > div.goods_desc_contents.goods_description > p:nth-child(10) > img')]
        product_details['detail_page'] = detail_page if detail_page else ["추출 안됨"]
    except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
        product_details['options'] = ["추출 안됨"]
        product_details['thumbnails'] = ["추출 안됨"]
        product_details['detail_page'] = ["추출 안됨"]

    driver.back()
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#searchedItemDisplay > ul > li:nth-child(3) > ul > li.goods_name_area'))
        )
    except TimeoutException:
        print("이전 페이지 로드 대기에서 오류 발생")
        driver.quit()
        return None

    return product_details

# 메인 함수
def main():
    driver = setup_driver(headless=False)
    login_url = "https://dawoori-sports.kr/member/login"
    username = "flowing"
    password = "q6160q6160q"
    if not login(driver, username, password, login_url):
        return

    product_url = "https://dawoori-sports.kr/goods/catalog?page=1&searchMode=catalog&category=c0019&per=200&filter_display=lattice&code=0019"
    driver.get(product_url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#searchedItemDisplay > ul > li:nth-child(3) > ul > li.goods_name_area'))
        )
    except TimeoutException:
        print("상품 리스트 로드 대기에서 오류 발생")
        driver.quit()
        return

    product_details_list = []
    products = driver.find_elements(By.CSS_SELECTOR, '#searchedItemDisplay > ul > li')
    for product in products:
        product_details = scrape_product_details(driver, product)
        if product_details:
            product_details_list.append(product_details)

    for product in product_details_list:
        print(f"상품명: {product['product_name']}")
        print(f"할인전 가격: {product['original_price']}")
        print(f"선택 옵션: {', '.join(product['options'])}")
        print(f"썸네일: {', '.join(product['thumbnails'])}")
        print(f"상세 페이지: {', '.join(product['detail_page'])}")
        print("="*10)

    driver.quit()

if __name__ == "__main__":
    main()
