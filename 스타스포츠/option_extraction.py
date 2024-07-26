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

def extract_options_ready():
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
                options = []  # 옵션 리스트 초기화

                try:
                    stock = product_soup.select_one("tbody tr input[name='stockL']")  # 재고 정보 선택
                    stock = int(stock["value"]) if stock else 0  # 재고 정보가 존재하면 정수로 변환
                except AttributeError:  # 속성 에러 예외 처리
                    stock = 0
                except TypeError:  # 타입 에러 예외 처리
                    stock = 0

                for a in range(1, 10):  # 1부터 9까지 옵션 인덱스 반복
                    try:
                        option = product_soup.select_one(f"tbody tr:nth-of-type({a}) input[name='optionTxtL']")  # 옵션 정보 선택
                        option = option["value"] if option else "없음"  # 옵션 정보가 존재하면 값 추출
                    except AttributeError:  # 속성 에러 예외 처리
                        option = "없음"
                    except TypeError:  # 타입 에러 예외 처리
                        option = "없음"

                    options.append(option)  # 옵션 리스트에 추가

                if not options:  # 옵션 리스트가 비어있는 경우
                    options.append("없음")  # "없음" 추가

                k = "==0=10000=0=0=0=\n".join(options)  # 옵션 리스트를 문자열로 결합
                ppp = "[필수선택]\n" + k.split("없음")[0]  # "없음" 이전의 문자열 추출
                if ppp.count("10000") == 1:  # "10000"이 1개만 있는 경우
                    ppp = ""  # 빈 문자열로 설정
                else:
                    ppp  # 그대로 유지

                print(f"옵션: {ppp if ppp else '옵션 없음'}")  # 옵션 출력
            else:
                print("링크 정보 없음")  # 링크 정보가 없는 경우 메시지 출력

if __name__ == "__main__":  # 메인 실행 부분
    extract_options_ready()  # extract_options_ready 함수 호출
