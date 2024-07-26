import requests  # HTTP 요청을 보내기 위해 requests 라이브러리를 임포트
from bs4 import BeautifulSoup as bs  # HTML 파싱을 위해 BeautifulSoup을 임포트
from urllib.parse import urljoin  # URL 결합을 위해 urljoin을 임포트
from playwright.sync_api import sync_playwright  # 동기 Playwright API를 임포트
from config import base_url, urlinput, rangeFir, rangeLas  # 설정값을 임포트

def fetch_page_content(url):
    with sync_playwright() as p:  # Playwright를 동기 모드로 사용
        browser = p.chromium.launch(headless=True)  # Chromium 브라우저를 헤드리스 모드로 실행
        page = browser.new_page()  # 새로운 페이지 열기
        page.goto(url)  # 주어진 URL로 이동
        page.wait_for_load_state('networkidle')  # 네트워크가 유휴 상태가 될 때까지 대기
        content = page.content()  # 페이지의 HTML 콘텐츠를 가져오기
        browser.close()  # 브라우저 닫기
        return content  # HTML 콘텐츠 반환

def extract_detail_pages():
    for j in range(rangeFir, rangeLas):  # 주어진 범위 내에서 반복
        url = urlinput.format(j)  # URL 생성
        req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})  # HTTP GET 요청
        soup = bs(req.content, "html.parser")  # BeautifulSoup을 사용하여 HTML 파싱
        product_elements = soup.select("div.mList1 ul li")  # 제품 요소 선택

        for product_element in product_elements:  # 각 제품 요소에 대해 반복
            link_element = product_element.select_one("a")  # 링크 요소 선택
            if link_element:  # 링크 요소가 존재하는 경우
                link = link_element["href"].replace("¶", "&").replace("^", "&")  # 링크 정제
                base2 = "https://starsportsmall.co.kr/goods/"  # 기본 URL
                product_link = urljoin(base2, link)  # 정제된 링크와 기본 URL 결합
                
                # 새로운 페이지 내용 가져오기
                html_content = fetch_page_content(product_link)  # fetch_page_content 함수 호출
                product_soup = bs(html_content, 'html.parser')  # BeautifulSoup으로 HTML 파싱

                # 상세 이미지 URL 추출
                detail_images = []
                for p in range(1, 5):
                    try:
                        image_url = product_soup.select_one(f"div.tab-con img:nth-of-type({p})").get("src")
                        if image_url and not image_url.endswith('.png'):  # PNG 파일 제외
                            detail_images.append(image_url)
                    except AttributeError:
                        detail_images.append("")

                # 상품 세부 정보 추출
                spec_table = product_soup.select_one("table.specTable")
                if spec_table:
                    rows = spec_table.select("tr")
                    product_details = {}
                    for row in rows:
                        th = row.select_one("th").get_text(strip=True)
                        td = row.select_one("td").get_text(strip=True)
                        product_details[th] = td
                
                # 출력
                for img_url in detail_images:
                    print(f"상세 이미지 URL: {img_url}")
                if product_details:
                    print("상품 세부 정보:")
                    for key, value in product_details.items():
                        print(f"{key}: {value}")

if __name__ == "__main__":
    extract_detail_pages()
