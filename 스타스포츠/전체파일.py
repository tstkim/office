import requests
from bs4 import BeautifulSoup as bs
import openpyxl
import os
import shutil
import urllib.request
from datetime import datetime
import time
import math
from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright
from config import base_url, urlinput, rangeFir, rangeLas, price_increase_rate, minimum_price

# 기본 설정
brand_code = "star"
brand_name = "스타스포츠"
category = "학교체육"

# URL 설정
catalog_url = "https://starsportsmall.co.kr/goods/submain_new.asp?page=1&cate=0&sword=&swhat=&listsort=new&listtype=album&listsize=20&sprice="

# 작업 시작 시간 기록
now = datetime.now()
start_time = time.time()
print("택수님 ! 작업을 시작할께요.. 조금만 기다려주세요*^.^*")
tdate = now.strftime("%Y%m%d%H%M")

# 폴더 생성
base_path = f'C:/Users/ME/Pictures/{tdate}{brand_code}'
thumbnail_path = f'{base_path}/cr'
output_path = f'{base_path}/output'
if os.path.exists(base_path):
    shutil.rmtree(base_path)
os.makedirs(thumbnail_path)
os.makedirs(output_path)

# 엑셀 파일 설정
wb = openpyxl.Workbook()
sheet = wb.active
sheet.append([
    "업체상품코드", "모델명", "브랜드", "제조사", "원산지", "상품명", "홍보문구", "요약상품명",
    "카테고리코드", "사용자분류명", "한줄메모", "시중가", "원가", "표준공급가", "판매가",
    "배송방법", "배송비", "구매수량", "과세여부", "판매수량", "이미지1URL", "이미지2URL",
    "이미지3URL", "이미지4URL", "GIF생성", "이미지6URL", "이미지7URL", "이미지8URL",
    "이미지9URL", "이미지10URL", "추가정보입력사항", "옵션타입", "옵션구분", "선택옵션",
    "입력형옵션", "추가구매옵션", "상세설명", "추가상세설명", "광고/홍보", "제조일자",
    "유효일자", "사은품내용", "키워드", "인증구분", "인증정보", "거래처", "영어상품명",
    "중국어상품명", "일본어상품명", "영어상세설명", "중국어상세설명", "일본어상세설명",
    "상품무게", "영어키워드", "중국어키워드", "일본어키워드", "생산지국가",
    "전세계배송코드", "사이즈", "포장방법", "상품상세코드", "상품상세1", "상품상세2",
    "상품상세3", "상품상세4", "상품상세5", "상품상세6", "상품상세7", "상품상세8",
    "상품상세9", "상품상세10", "상품상세11", "상품상세12", "상품상세13", "상품상세14",
    "상품상세15", "상품상세16", "상품상세17", "상품상세18", "상품상세19", "상품상세20",
    "상품상세21", "상품상세22", "상품상세23", "상품상세24"
])

def sanitize_filename(filename):
    return "".join(c for c in filename if c.isalnum() or c in (' ', '.', '_')).rstrip()

def fetch_page_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')
        content = page.content()
        browser.close()
        return content

def download_image(image_url, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = os.path.join(folder, sanitize_filename(image_url.split("/")[-1]))
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as file:
                shutil.copyfileobj(response.raw, file)
            return filename
        else:
            print(f"이미지 다운로드 실패: {image_url} 상태 코드: {response.status_code}")
    except Exception as e:
        print(f"이미지 다운로드 중 오류 발생: {e} - URL: {image_url}")
    return None

def extract_product_info(product_element):
    product_info = {}

    # 가격
    price_element = product_element.select_one("span.pr")
    if price_element:
        price_text = price_element.get_text(strip=True).replace(',', '').replace('원', '')
        try:
            original_price = float(price_text)
            adjusted_price = math.ceil((original_price * price_increase_rate) / 100) * 100
            if adjusted_price < minimum_price:
                adjusted_price = minimum_price
            product_info["price"] = adjusted_price
        except ValueError:
            product_info["price"] = "가격 변환 오류"
    else:
        product_info["price"] = "가격 정보 없음"

    # 연결 링크
    link_element = product_element.select_one("a")
    if link_element:
        link = link_element["href"].replace("¶", "&")
        site = "https://starsportsmall.co.kr/goods/"
        product_info["product_link"] = site + link
    else:
        product_info["product_link"] = "링크 정보 없음"

    # 상품명
    name_element = product_element.select_one("span.ti")
    if name_element:
        name = name_element.get_text(strip=True)
        product_info["name"] = name
    else:
        product_info["name"] = "상품명 정보 없음"

    return product_info

def extract_detail_page(product_link):
    html_content = fetch_page_content(product_link)
    product_soup = bs(html_content, 'html.parser')

    detail_images = []
    for p in range(1, 5):
        try:
            image_url = product_soup.select_one(f"div.tab-con img:nth-of-type({p})").get("src")
            if image_url and not image_url.endswith('.png'):
                detail_images.append(image_url)
        except AttributeError:
            detail_images.append("")

    return detail_images

# 페이지 접근 및 데이터 추출
response = requests.get(catalog_url)
response.encoding = 'utf-8'  # 응답 인코딩 설정
if response.status_code != 200:
    print(f"Failed to access {catalog_url}")
else:
    soup = bs(response.content.decode('utf-8', 'ignore'), 'html.parser')  ##이부분 수정됨
    product_elements = soup.select("div.mList1 ul li")
    image_counter = 1  # 이미지 파일명을 고유하게 만들기 위한 카운터
    
    for product_element in product_elements:
        product_info = extract_product_info(product_element)

        if "가격 변환 오류" in str(product_info["price"]):
            print(f"가격 변환 오류: {product_info['price']}")
            continue

        # 썸네일 이미지 저장 및 새로운 캔버스에 편집
        try:
            thumbnail_url = product_info["product_link"]
            if not thumbnail_url.startswith('http'):
                thumbnail_url = base_url + thumbnail_url
            thumbnail_path_local = f'{thumbnail_path}/{image_counter}_cr.jpg'
            downloaded_thumbnail = download_image(thumbnail_url, thumbnail_path)
            if downloaded_thumbnail:
                try:
                    im = Image.open(downloaded_thumbnail)
                    im = im.resize((400, 400))

                    # 새로운 캔버스 생성
                    image = Image.new("RGB", (600, 600), "white")
                    gray_background = Image.new("RGB", (600, 100), (56, 56, 56))  # 아래 검정색 바탕띠
                    image.paste(gray_background, (0, 500))

                    red_background = Image.new("RGB", (150, 150), (255, 61, 70))  # 위 빨간색 바탕띠
                    image.paste(red_background, (440, 0))

                    name_font = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 65)
                    label_font = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 40)

                    text1 = product_info["name"].replace("-", "")  # 파일명에 "-" 혹은 특수문자가 있으면 오류가 난다
                    ImageDraw.Draw(image).text((10, 510), text1, font=name_font, fill="white", stroke_fill="black", stroke_width=2)
                    ImageDraw.Draw(image).text((460, 10), "S2B", font=name_font, fill="white", stroke_fill="red", stroke_width=2)
                    ImageDraw.Draw(image).text((505, 95), "공식", font=label_font, fill="white", stroke_fill="red", stroke_width=1)
                    image.paste(im, (100, 100))

                    image.save(thumbnail_path_local)
                    image.close()
                except UnidentifiedImageError:
                    print(f"이미지 파일 인식 오류: {thumbnail_path_local}")
        except (ValueError, urllib.error.HTTPError, urllib.error.URLError, FileNotFoundError) as e:
            print(f"썸네일 이미지 처리 중 오류 발생: {e}")

        # 상세 페이지 이미지 저장 및 자르기
        try:
            detail_images = extract_detail_page(product_info["product_link"])
            combined_image = None
            current_image_num = len(os.listdir(output_path)) // 10 + 1  # 현재 상품 번호 계산

            for img_url in detail_images:
                if not img_url.startswith('http'):
                    img_url = base_url + img_url
                img_path = f'{base_path}/detail_{image_counter}.jpg'  # 고유한 파일명 생성
                downloaded_detail_image = download_image(img_url, base_path)
                if downloaded_detail_image:
                    try:
                        jm = Image.open(downloaded_detail_image).convert("RGB")
                    except UnidentifiedImageError:
                        print(f"이미지 파일 인식 오류: {img_path}")
                        continue

                    if combined_image is None:
                        combined_image = jm
                    else:
                        combined_width = max(combined_image.width, jm.width)
                        combined_height = combined_image.height + jm.height
                        new_combined_image = Image.new("RGB", (combined_width, combined_height), "white")
                        new_combined_image.paste(combined_image, (0, 0))
                        new_combined_image.paste(jm, (0, combined_image.height))
                        combined_image = new_combined_image

            if combined_image is not None:
                width, height = combined_image.size
                for i in range(10):
                    crop_area = (0, height * (i * 0.1), width, height * ((i + 1) * 0.1))
                    cropped_img = combined_image.crop(crop_area)
                    cropped_img.save(f'{output_path}/{current_image_num}_{i + 1:03}.jpg')
                combined_image.close()
        except (ValueError, urllib.error.HTTPError, urllib.error.URLError, FileNotFoundError) as e:
            print(f"상세 페이지 이미지 처리 중 오류 발생: {e}")

        # 옵션 처리
        formatted_options = []
        options = product_info.get("options", "").split("\n")
        for option in options:
            if "없음" not in option:
                option = option.replace(" (품절)", "").replace(",", "")
                if "(+" in option:
                    name, extra_price = option.split("(+")
                    extra_price = extra_price.replace("₩)", "").strip()
                    formatted_option = f"{name}=={extra_price}=10000=0=0=0="
                else:
                    parts = option.split("==")
                    if len(parts) == 2:
                        name, extra_price = parts
                        formatted_option = f"{name}=={extra_price}=10000=0=0=0="
                    else:
                        formatted_option = f"{option}==0=10000=0=0=0="
                formatted_options.append(formatted_option)

        # 최종 옵션 문자열 만들기
        option_string = "[필수선택]\n" + "\n".join(formatted_options)

        # 옵션 1개짜리 없애기
        if option_string.count("10000") == 1:
            option_string = ""
        # 옵션 없는 것 필수선택 없애기
        if option_string.count("10000") == 0:
            option_string = ""

        print(f"상품명: {product_info['name']}")
        print(f"변경된 가격: {product_info['price']}")
        print(f"썸네일 이미지 URL: {product_info['product_link']}")
        print(f"옵션: {option_string}")

        # 추가 코드 시작
        product_code = str(now)[3:4] + str(now)[5:7] + str(now)[8:10] + brand_code + str(image_counter)
        empty_str = ""  # 공백
        brand = brand_name  # 브랜드
        manufacturer = brand_name  # 제조사
        origin = "국내=서울=강남구"  # 원산지
        attributes = brand_code + tdate
        payment_method = "선결제"
        shipping_fee = "3500"
        purchase_quantity = "0"
        tax_status = "y"
        inventory = "9000"
        thumbnail_url_final = f"http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/cr/{image_counter}_cr.jpg"  # 날짜 수정할 것
        option_type = "" if option_string == "" else "SM"
        description = f"""<center> <img src='http://gi.esmplus.com/tstkimtt/head.jpg' /><br>
        <img src='http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/output/{current_image_num}_001.jpg' /><br />
        <img src='http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/output/{current_image_num}_002.jpg' /><br />
        <img src='http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/output/{current_image_num}_003.jpg' /><br />
        <img src='http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/output/{current_image_num}_004.jpg' /><br />
        <img src='http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/output/{current_image_num}_005.jpg' /><br />
        <img src='http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/output/{current_image_num}_006.jpg' /><br />
        <img src='http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/output/{current_image_num}_007.jpg' /><br />
        <img src='http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/output/{current_image_num}_008.jpg' /><br />
        <img src='http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/output/{current_image_num}_009.jpg' /><br />
        <img src='http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/output/{current_image_num}_010.jpg' /><br />
        <img src='http://gi.esmplus.com/tstkimtt/deliver.jpg' /></center>"""
        coupon = "쿠폰"
        category_code = "c"
        weight = "25"
        detailed_description = "상세설명일괄참조"
        free_gift = "N"

        if len(detail_images) > 0 and product_info["price"] != " ":  # 상세페이지가 있고 가격이 비어있지 않은 경우만
            sheet.append([product_code, empty_str, brand, manufacturer, origin, product_info['name'], empty_str, empty_str, category, attributes, empty_str, empty_str, empty_str, empty_str, empty_str, product_info["price"], payment_method, shipping_fee, purchase_quantity, tax_status, inventory, thumbnail_url_final, thumbnail_url_final, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, option_type, option_string, empty_str, empty_str, description, empty_str, empty_str, empty_str, empty_str, coupon, empty_str, category_code, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, empty_str, weight, detailed_description, detailed_description, detailed_description, detailed_description, detailed_description, detailed_description, free_gift, detailed_description, detailed_description, detailed_description, detailed_description, detailed_description, thumbnail_url])

        image_counter += 1  # 다음 상품을 위해 카운터 증가

# 현재 시간을 출력
print(now)

# 엑셀 파일 저장
wb.save(f'C:/Users/ME/Pictures/{tdate}{brand_code}.xlsx')
print("크롤링 성공")

# 작업에 총 몇 초가 걸렸는지 출력
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
