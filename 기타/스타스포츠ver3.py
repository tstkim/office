import requests
from bs4 import BeautifulSoup as bs
import openpyxl
import os
import shutil
import urllib.request
from urllib.parse import urljoin
from datetime import datetime
import time
import math
from PIL import Image, ImageDraw, ImageFont
from PIL import Image, UnidentifiedImageError
from urllib.parse import quote
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
raageLas = 2

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

# image_counter 초기화
image_counter = 0

for j in range(rangeFir, raageLas):
    url = urlinput.format(j)
    req = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = bs(req.content, "html.parser")

    product_elements = soup.select("div.mList1 ul li")

    for product_element in product_elements:
        # 상품명 추출
        try:
            product_name = product_element.select_one("span.ti").get_text(strip=True)
        except AttributeError:
            product_name = "상품명을 찾을 수 없습니다."

        # 가격 추출
        try:
            price = product_element.select_one("span.pr").get_text(strip=True)
            price = price.replace(",", "").replace("원", "")
            original_price = float(price)
            adjusted_price = math.ceil((original_price * price_increase_rate) / 100) * 100
            if adjusted_price < minimum_price:
                adjusted_price = minimum_price
        except AttributeError:
            adjusted_price = "가격 정보 없음"
        except ValueError:
            print(f"가격 변환 오류: {price}")
            adjusted_price = minimum_price

        # 연결 링크 추출
        link_element = product_element.select_one("a")
        if link_element:
            link = link_element["href"].replace("¶", "&")
            link = link.replace("^", "&")
            product_link = urljoin(base_url, link)
        else:
            product_link = "링크 정보 없음"

        # 상세 페이지로 이동하여 썸네일 URL 추출
        product_response = requests.get(product_link)
        if product_response.status_code != 200:
            print(f"Failed to access {product_link}")
            continue

        product_response.encoding = product_response.apparent_encoding
        product_soup = bs(product_response.text, 'html.parser')
        thumbnail_element = product_soup.select_one("div.photo-zone img")
        if thumbnail_element:
            sumnail = thumbnail_element.get('src')
        else:
            sumnail = "없음"
        product_info = {
            "sumnail": sumnail,
            "name": product_name
        }

        # 썸네일 이미지 저장 및 새로운 캔버스에 편집
        try:
            thumbnail_url = product_info["sumnail"]
            if not thumbnail_url.startswith('http'):
                thumbnail_url = base_url + thumbnail_url
            urllib.request.urlretrieve(thumbnail_url, f'{thumbnail_path}/{image_counter}_cr.jpg')
            im = Image.open(f'{thumbnail_path}/{image_counter}_cr.jpg')
            im = im.resize((400, 400))

            # 새로운 캔버스 생성
            image = Image.new("RGB", (600, 600), "white")
            gray_background = Image.new("RGB", (600, 100), (56, 56, 56))
            image.paste(gray_background, (0, 500))

            red_background = Image.new("RGB", (150, 150), (255, 61, 70))
            image.paste(red_background, (440, 0))

            name_font = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 65)
            label_font = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 40)

            text1 = product_info["name"].replace("-", "")
            ImageDraw.Draw(image).text((10, 510), text1, font=name_font, fill="white", stroke_fill="black", stroke_width=2)
            ImageDraw.Draw(image).text((460, 10), "S2B", font=name_font, fill="white", stroke_fill="red", stroke_width=2)
            ImageDraw.Draw(image).text((505, 95), "공식", font=label_font, fill="white", stroke_fill="red", stroke_width=1)
            image.paste(im, (100, 100))

            image.save(f'{thumbnail_path}/{image_counter}_cr.jpg')
            image.close()
        except (ValueError, urllib.error.HTTPError, urllib.error.URLError, FileNotFoundError) as e:
            print(f"썸네일 이미지 처리 중 오류 발생: {e}")
            continue

        # 상세 페이지 이미지 저장 및 자르기
        try:
            detail_images = []
            for p in range(1, 5):
                try:
                    asangsee = product_element.select_one(f"div.tab-con img:nth-of-type({p})").get("src")
                    detail_images.append(asangsee)
                except AttributeError:
                    detail_images.append("")
                except IndexError:
                    detail_images.append("")
            
            combined_image = None
            for img_url in detail_images:
                if not img_url.startswith('http'):
                    img_url = base_url + img_url
                img_path = f'{base_path}/detail_{image_counter}.jpg'
                try:
                    urllib.request.urlretrieve(img_url, img_path)
                    jm = Image.open(img_path).convert("RGB")
                except (urllib.error.HTTPError, urllib.error.URLError, FileNotFoundError) as e:
                    print(f"상세 페이지 이미지 처리 중 오류 발생: {e}")
                    continue
                except UnidentifiedImageError as e:
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
                current_image_num = len(os.listdir(output_path)) // 10 + 1
                for i in range(10):
                    crop_area = (0, height * (i * 0.1), width, height * ((i + 1) * 0.1))
                    cropped_img = combined_image.crop(crop_area)
                    cropped_img.save(f'{output_path}/{current_image_num}_{i + 1:03}.jpg')
                combined_image.close()
        except (ValueError, urllib.error.HTTPError, urllib.error.URLError, FileNotFoundError) as e:
            print(f"상세 페이지 이미지 처리 중 오류 발생: {e}")

        # 옵션 처리
        formatted_options = []
        options = "옵션 없음".split("\n")
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

        option_string = "[필수선택]\n" + "\n".join(formatted_options)
        if option_string.count("10000") == 1:
            option_string = ""
        if option_string.count("10000") == 0:
            option_string = ""

        print(f"상품명: {product_name}")
        print(f"변경된 가격: {adjusted_price}")
        print(f"썸네일 이미지 URL: {product_link}")
        print(f"옵션: {option_string}")

        product_code = str(now)[3:4] + str(now)[5:7] + str(now)[8:10] + brand_code + str(image_counter)
        brand = brand_name
        manufacturer = brand_name
        origin = "국내=서울=강남구"
        attributes = brand_code + tdate
        payment_method = "선결제"
        shipping_fee = "3500"
        purchase_quantity = "0"
        tax_status = "y"
        inventory = "9000"
        thumbnail_url_final = f"http://ai.esmplus.com/tstkimtt/{tdate}{brand_code}/cr/{image_counter}_cr.jpg"
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

        if len(detail_images) > 0 and adjusted_price != " ":
            sheet.append([
                product_code, "", brand, manufacturer, origin, product_name, "", "", category, attributes, "", "", "", "",
                adjusted_price, payment_method, shipping_fee, purchase_quantity, tax_status, inventory, thumbnail_url_final,
                thumbnail_url_final, "", "", "", "", "", "", "", "", "", "", option_type, option_string, "", "", description,
                "", "", "", "", coupon, "", category_code, "", "", "", "", "", "", "", "", "", "", "", "", "", weight,
                detailed_description, detailed_description, detailed_description, detailed_description,
                detailed_description, detailed_description, free_gift, detailed_description, detailed_description,
                detailed_description, detailed_description, detailed_description, thumbnail_url
            ])

        image_counter += 1

print(now)
wb.save(f'C:/Users/ME/Pictures/{tdate}{brand_code}.xlsx')
print("크롤링 성공")

end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")
