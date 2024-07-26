import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urllib.parse import urljoin
from config import base_url, urlinput, rangeFir, rangeLas

def setup_selenium():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(2)
    return driver

def extract_options_ready():
    driver = setup_selenium()
    for j in range(rangeFir, rangeLas):
        url = urlinput.format(j)
        req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = bs(req.content, "html.parser")
        product_elements = soup.select("div.mList1 ul li")

        for product_element in product_elements:
            link_element = product_element.select_one("a")
            if link_element:
                link = link_element["href"].replace("¶", "&").replace("^", "&")
                base2 = "https://starsportsmall.co.kr/goods/"
                product_link = urljoin(base2, link)
            else:
                product_link = "링크 정보 없음"

            driver.get(product_link)
            html1 = driver.page_source
            options = []

            try:
                soup = bs(html1, 'html.parser')
                stock = soup.select_one("tbody tr input[name='stockL']")
                stock = int(stock["value"]) if stock else 0
            except AttributeError:
                stock = 0
            except TypeError:
                stock = 0

            for a in range(1, 10):
                try:
                    soup = bs(html1, 'html.parser')
                    option = soup.select_one(f"tbody tr:nth-of-type({a}) input[name='optionTxtL']")
                    option = option["value"]
                except AttributeError:
                    option = "없음"
                except TypeError:
                    option = "없음"

                options.append(option)

            if not options:
                options.append("없음")

            k = "==0=10000=0=0=0=\n".join(options)
            ppp = "[필수선택]\n" + k.split("없음")[0]
            if ppp.count("10000") == 1:
                ppp = ""
            else:
                ppp

            print(f"옵션: {ppp if ppp else '옵션 없음'}")

if __name__ == "__main__":
    extract_options_ready()
