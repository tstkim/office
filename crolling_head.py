#n 선언!! (페이지를 임의로 분류해야할때만 변경) -------------
n=1

#기본 시간세팅 -------------------
import time
from datetime import datetime
now=datetime.now()
tdate=str(now)[2:4]+str(now)[5:7]+str(now)[8:10]    #년월일
start_time = time.time()                            #시작시점표시
print("택수님 ! 작업을 시작할께요.. 조금만 기다려주세요*^.^*")                              #작업시작 


#오류 방지-----------------------------------------------------------
## ssl오류 권한오류시(다운이미지오류)
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
# 이미지 다운받을때 페이지 없을때 오류
from urllib.error import HTTPError
from urllib.error import URLError
#----------------------------------------------------------------

import requests
from bs4 import BeautifulSoup as bs
import urllib.request   #이미지파일저장
from urllib.request import urlopen

import os    #폴더만들때
import shutil #폴더삭제시

import pyautogui

import re    #정규식

import openpyxl          #엑셀로 추출(상용함)
wb = openpyxl.Workbook()    
sheet = wb.active
sheet.append(["업체상품코드","모델명","브랜드","제조사","원산지","상품명","홍보문구","요약상품명","카테고리코드","사용자분류명","한줄메모","시중가","원가","표준공급가","판매가","배송방법","배송비","구매수량","과세여부","판매수량","이미지1URL","이미지2URL","이미지3URL","이미지4URL","GIF생성","이미지6URL","이미지7URL","이미지8URL","이미지9URL","이미지10URL","추가정보입력사항","옵션타입","옵션구분","선택옵션","입력형옵션","추가구매옵션","상세설명","추가상세설명","광고/홍보","제조일자","유효일자","사은품내용","키워드","인증구분","인증정보","거래처","영어상품명","중국어상품명","일본어상품명","영어상세설명","중국어상세설명","일본어상세설명","상품무게","영어키워드","중국어키워드","일본어키워드","생산지국가","전세계배송코드","사이즈","포장방법","상품상세코드","상품상세1","상품상세2","상품상세3","상품상세4","상품상세5","상품상세6","상품상세7","상품상세8","상품상세9","상품상세10","상품상세11","상품상세12","상품상세13","상품상세14","상품상세15","상품상세16","상품상세17","상품상세18","상품상세19","상품상세20","상품상세21","상품상세22","상품상세23","상품상세24"
])

#이미지사이즈 변경  ------------------------------
from PIL import Image, ImageDraw, ImageFont
from PIL import ImageFile   ##잘린 이미지 에러방지(OSError)
from PIL import UnidentifiedImageError
ImageFile.LOAD_TRUNCATED_IMAGES = True

Image.MAX_IMAGE_PIXELS = 8947848  # 예를 들어 5000만 픽셀로 제한

