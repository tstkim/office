# config.py
from datetime import datetime

# 기본 설정
brand_code = "star"
brand_name = "스타스포츠"
category = "학교체육"
price_increase_rate = 1.0
minimum_price = 10000
base_url = "https://starsportsmall.co.kr"

# URL 설정
urlinput = "https://starsportsmall.co.kr/goods/submain_new.asp?page={}&cate=0&sword=&swhat=&listsort=new&listtype=album&listsize=20&sprice="
rangeFir = 1
rangeLas = 2

# 작업 시작 시간 기록
now = datetime.now()
start_time = now.strftime("%Y%m%d%H%M")
print("Configuration loaded successfully.")
