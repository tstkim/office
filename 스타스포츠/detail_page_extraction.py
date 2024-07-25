# detail_page_extraction.py
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from config import base_url, urlinput, rangeFir, rangeLas

def extract_detail_pages():
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
            detail_images = []
            for p in range(1, 5):
                try:
                    image_url = product_soup.select_one(f"div.tab-con img:nth-of-type({p})").get("src")
                    detail_images.append(image_url)
                except AttributeError:
                    detail_images.append("")

            for img_url in detail_images:
                print(f"상세 이미지 URL: {img_url}")

if __name__ == "__main__":
    extract_detail_pages()
