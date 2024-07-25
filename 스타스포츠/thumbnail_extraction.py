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
                product_link = urljoin(base_url, link)
            else:
                product_link = "링크 정보 없음"

            product_response = requests.get(product_link)
            if product_response.status_code != 200:
                print(f"Failed to access {product_link}")
                continue

            product_response.encoding = product_response.apparent_encoding
            product_soup = bs(product_response.text, 'html.parser')
            thumbnail_element = product_soup.select_one("div.photo-zone img")
            if thumbnail_element:
                thumbnail = thumbnail_element.get('src')
            else:
                thumbnail = "없음"
            print(f"썸네일 URL: {thumbnail}")

if __name__ == "__main__":
    extract_thumbnails()
