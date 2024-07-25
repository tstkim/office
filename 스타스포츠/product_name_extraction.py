# product_name_extraction.py
import requests
from bs4 import BeautifulSoup as bs
from config import urlinput, rangeFir, rangeLas

def extract_product_names():
    for j in range(rangeFir, rangeLas):
        url = urlinput.format(j)
        req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = bs(req.content, "html.parser")
        product_elements = soup.select("div.mList1 ul li")

        for product_element in product_elements:
            try:
                product_name = product_element.select_one("span.ti").get_text(strip=True)
            except AttributeError:
                product_name = "상품명을 찾을 수 없습니다."
            print(f"상품명: {product_name}")

if __name__ == "__main__":
    extract_product_names()
