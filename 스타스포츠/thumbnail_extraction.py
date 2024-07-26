# thumbnail_extraction.py
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from config import base_url, urlinput, rangeFir, rangeLas

def extract_thumbnails():
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
            print(product_link)
            product_response = requests.get(product_link)
            if product_response.status_code != 200:
                print(f"Failed to access {product_link}")
                continue

            product_soup = bs(product_response.text, 'html.parser')
            thumbnail_element = product_soup.select_one("img#zoom_mw")
            if thumbnail_element:
                thumbnail = thumbnail_element.get('data-zoom-image')
                print(f"썸네일 URL: {thumbnail}")
            else:
                # 썸네일이 없을 경우 출력하지 않음
                pass

if __name__ == "__main__":
    extract_thumbnails()
