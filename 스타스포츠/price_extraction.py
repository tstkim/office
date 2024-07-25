# price_extraction.py
import requests
from bs4 import BeautifulSoup as bs
import math
from config import urlinput, rangeFir, rangeLas, price_increase_rate, minimum_price

def extract_prices():
    for j in range(rangeFir, rangeLas):
        url = urlinput.format(j)
        req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        soup = bs(req.content, "html.parser")
        product_elements = soup.select("div.mList1 ul li")

        for product_element in product_elements:
            try:
                price = product_element.select_one("span.pr").get_text(strip=True)
                price = price.replace(",", "").replace("원", "")
                original_price = float(price)
                adjusted_price = math.ceil((original_price * price_increase_rate) / 100) * 100
                if adjusted_price < minimum_price:
                    adjusted_price = minimum_price
            except (AttributeError, ValueError):
                adjusted_price = "가격 정보 없음"
            print(f"가격: {adjusted_price}")

if __name__ == "__main__":
    extract_prices()
