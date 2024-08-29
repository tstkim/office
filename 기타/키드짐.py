#--작업세팅------------------------------------------------------------
#1. 가격 인상률 설정 
priceR=1.05              #10%인상이면 1.1
#2. URL 변경  - {} 함께변경 주의!!
urlinput="http://www.kidgym.co.kr/product/list.html?cate_no=25&page={}"

#3. 크롤링 페이지 범위지정
rangeFir=1
raageLas=2
#4. 코드명변경(폴더명)
code="kidgym"
codek="키드짐"
#5.기준가 이상만 추출
Sprice =20000
#-----------------------------------------------------------------------------------------------------------------------------




import time
from datetime import datetime
now=datetime.now()
tdate=str(now)[2:4]+str(now)[5:7]+str(now)[8:10]    #년월일

from requests.models import HTTPError 

# 작업 시작 메시지를 출력합니다.--
print("Process Start")
# 시작 시점의 시간을 기록합니다.--
start_time = time.time()

import requests
from bs4 import BeautifulSoup as bs


import urllib.request   #이미지파일저장

## ssl오류 권한오류시(다운이미지오류)-----
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
###-----------------

# 이미지 다운받을때 페이지 없을때 오류
from urllib.error import HTTPError
from urllib.error import URLError

import os    #폴더만들때
import shutil #폴더삭제시

import pyautogui



import openpyxl          #엑셀로 추출(상용함)
wb = openpyxl.Workbook()    
sheet = wb.active
sheet.append(["업체상품코드","모델명","브랜드","제조사","원산지","상품명","홍보문구","요약상품명","카테고리코드","사용자분류명","한줄메모","시중가","원가","표준공급가","판매가","배송방법","배송비","구매수량","과세여부","판매수량","이미지1URL","이미지2URL","이미지3URL","이미지4URL","GIF생성","이미지6URL","이미지7URL","이미지8URL","이미지9URL","이미지10URL","추가정보입력사항","옵션타입","옵션구분","선택옵션","입력형옵션","추가구매옵션","상세설명","추가상세설명","광고/홍보","제조일자","유효일자","사은품내용","키워드","인증구분","인증정보","거래처","영어상품명","중국어상품명","일본어상품명","영어상세설명","중국어상세설명","일본어상세설명","상품무게","영어키워드","중국어키워드","일본어키워드","생산지국가","전세계배송코드","사이즈","포장방법","상품상세코드","상품상세1","상품상세2","상품상세3","상품상세4","상품상세5","상품상세6","상품상세7","상품상세8","상품상세9","상품상세10","상품상세11","상품상세12","상품상세13","상품상세14","상품상세15","상품상세16","상품상세17","상품상세18","상품상세19","상품상세20","상품상세21","상품상세22","상품상세23","상품상세24"
])




n=1


# 폴더 생성 (기존재하면 삭제 후 생성)
path_a='C:/Users/ME/Pictures/'+tdate+code
path_b='C:/Users/ME/Pictures/'+tdate+code+'/cr'
path_c='C:/Users/ME/Pictures/'+tdate+code+'/output'
if os.path.exists(path_a):
    shutil.rmtree(path_a)

os.mkdir(path_a)
os.mkdir(path_b)
os.mkdir(path_c)

#이미지사이즈 변경
from PIL import Image, ImageDraw, ImageFont

from PIL import ImageFile   ##잘린 이미지 에러방지(OSError)
ImageFile.LOAD_TRUNCATED_IMAGES = True



#-------------------------------------------



#--------------------------------------------------------------------------------------------------------------------------------------------------------

for j in range(rangeFir,raageLas):
    url=urlinput.format(j)

    req=requests.get(url,headers={"User-Agent": "Mozilla/5.0" })
    soup= bs(req.content, "html.parser")



    #k=soup.find_all("font",{"style":"font-size:15px;color:#050505;font-weight:bold;"})
    k=soup.select("ul.prdList li.xans-record- div.thumbnail")



      
    #상품명
    for i in k:
        nam=i.select_one("img")#).get_text(strip=True)
        name=nam["alt"]
        
        text1=name   #썸네일 상품명

    #코드명
        codename=str(now)[3:4]+str(now)[5:7]+str(now)[8:10]+code+str(n)

    #연결링크
        link=i.select_one("a")
        link=link["href"]
        site="http://www.kidgym.co.kr/"
        link=site+link
        reqq=requests.get(link,headers={"User-Agent": "Mozilla/5.0" })
        soupp= bs(reqq.content, "html.parser")

    #카테고리    
        cate="학교체육"     

    #가격
        try:
            price=soupp.select_one("strong#span_product_price_text").get_text(strip=True)    
            price=price.replace(",","")
            price=price[:-1]
            price=round(int(price)*priceR,-2)   #-priceR (5~15% 더 상승)
        except AttributeError:
            price=100                          
 
    #썸네일
        try:
         sumnail=soupp.select_one("img.BigImage").get('src')
        except AttributeError:
            sumnail="뭐야"

        ksum="http:"+sumnail  



    #옵션(ppp)  --키드짐은 1개만 추출되게앴음
        options=[]
        for a in range(1,2):
            try:
                option=soupp.select_one("select#product_option_id1 optgroup option:nth-of-type({})".format(a)).get_text(strip=True) 
           
            except AttributeError:
                option="없음"

            options.append(option)
            k="".join(options)                 # k="==0=10000=0=0=0=\n".join(options)
            k=k+"==0=10000=0=0=0=\n"                                       
            ss=k.replace("품절","상품준비중(미정)")    
            pp=ss.split("없음")[0]
            ppp="[필수선택]\n"+pp
        if len(ppp)==7:          #옵션1개짜리 없애기
            ppp=""
        else:
            ppp    

    #상세페이지 (Tsangsee)
        try:

            sangseee=soupp.select_one("div.cont" ).get_text(strip=True)                #텍스트 상세
            sangseee=sangseee.replace("※ 이미지 무단복제시, 처벌 대상이 될 수 있습니다.","")
            sangseee=sangseee.replace("●",".")
            sangseee=sangseee.replace("▶",".")
            sangseee=sangseee.split(".")

        except AttributeError:
            sangseee=""

        


        try:
            asangsee=soupp.select_one("div.cont img[src*=web]").get("src")                #이미지상세
            
        except AttributeError:
            asangsee=""  

        asangsee="http://www.kidgym.co.kr"+asangsee
        asangsee=asangsee.replace("www.kidgym.co.kr//","")

        
        if price>Sprice:     #가격 기준가 이상만 이미지추출조건
            asangsee
        else:
            asangsee=""

        if len(asangsee)>0:  #상세페이지가 없으면 썸네일도 없도록
            ksum
        else:
            ksum=""



        name=name+" /"+"키드짐/학교체육/뉴스포츠/스포츠용품 학교체육용품 체육교구 청소년체육"+str(now)[3:4]+str(now)[5:7]+str(now)[8:10]                                                 # "/sm/학교체육/뉴스포츠"+str(now)[3:4]+str(now)[5:7]+str(now)[8:10] 
       
        #-------------------------------------------------------------------------------------
    
     


        g=""  #공백
        c=codek #브랜드
        d=codek #제조사
        e="국내=서울=강남구" #원산지
        att=code+tdate
        p="선결제"
        q="3000"
        r="0"
        s="y"
        t="9000"

        u="http://ai.esmplus.com/tstkimt/"+tdate+code+"/cr/"+str(n)+"_cr.jpg"    #날짜 수정할것
        if ppp=="":
            ag=""
        else:
            ag="SM"
        ak="<center> <img src='http://gi.esmplus.com/tstkimtt/head.jpg' /><br> <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/event.jpg' /><br /> \
        <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"_001.jpg' /><br /> \
            <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"_002.jpg' /><br />\
                <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"_003.jpg' /><br />\
                     <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"_004.jpg' /><br />\
                         <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"_005.jpg' /><br />\
                             <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"_006.jpg' /><br /> \
                                 <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"_007.jpg' /><br />\
                                     <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"_008.jpg' /><br />\
                                         <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"_009.jpg' /><br />\
                                              <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"_010.jpg' /><br />\
                                                    <img src='http://ai.esmplus.com/tstkimt/"+tdate+code+"/output/"+str(n)+"head.jpg' /><br />\
                                                        <img src='http://gi.esmplus.com/tstkimtt/deliver.jpg' /></center>"

        ap="쿠폰"
        ar="c"
        bi="25"
        bj="상세설명일괄참조"
        bbs="N"

        if len(asangsee)>0:     #상세페이지가 있는것만
            sheet.append([codename,g,c,d,e,name,g,g,cate,att,g,g,g,g,price,p,q,r,s,t,u,u,g,g,g,g,g,g,g,g,g,g,ag,ppp,g,g,ak,g,g,g,g,ap,g,ar,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,bi,bj,bj,bj,bj,bj,bj,bj,bj,bj,bbs,bj,bj,bj,bj,bj,ksum,asangsee])

        else:
            pass




        #상세이이지저장
        try:
            urllib.request.urlretrieve(asangsee,'C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'.jpg')    #이미지파일 저장   
            jm=Image.open('C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'.jpg')  #이미지 자르기
            jm = jm.convert("RGB")
            width=int(jm.size[0])   
            height=int(jm.size[1])
            jm1=jm.crop((0,0,width,height-(height*0.9)))
            jm1.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'_001.jpg')
            jm2=jm.crop((0,height*0.1,width,height-(height*0.8)))
            jm2.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'_002.jpg')
            jm3=jm.crop((0,height*0.2,width,height-(height*0.7)))
            jm3.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'_003.jpg')
            jm4=jm.crop((0,height*0.3,width,height-(height*0.6)))
            jm4.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'_004.jpg')
            jm5=jm.crop((0,height*0.4,width,height-(height*0.5)))
            jm5.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'_005.jpg')
            jm6=jm.crop((0,height*0.5,width,height-(height*0.4)))
            jm6.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'_006.jpg')            
            jm7=jm.crop((0,height*0.6,width,height-(height*0.3)))
            jm7.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'_007.jpg')
            jm8=jm.crop((0,height*0.7,width,height-(height*0.2)))
            jm8.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'_008.jpg')
            jm9=jm.crop((0,height*0.8,width,height-(height*0.1)))
            jm9.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'_009.jpg')
            jm10=jm.crop((0,height*0.9,width,height))
            jm10.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'_010.jpg')


            jimcanvas = Image.new("RGB", (860, 700), "white")   #새로운 캔버스 만들기 

            sangsefL = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 40)
            sangsefs = ImageFont.truetype("C:/Windows/Fonts/Malgunsl.ttf", 15)
            sangsefm = ImageFont.truetype("C:/Windows/Fonts/Malgunsl.ttf", 20)

            nameFont = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 65)
            label = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 40)

            Topt=Image.new("RGB",(250,60),(56,56,56))   #상세맨위 검정색 바탕띠
            jimcanvas.paste(Topt,(0,0))
            Topt1=Image.new("RGB",(860,1),(56,56,56))   #상세맨위 검정색 얇은줄
            jimcanvas.paste(Topt1,(0,59))
            ImageDraw.Draw(jimcanvas).text(xy=(20,5), text="Detail Spec", font=label, fill="white", stroke_fill="black", stroke_width=1,)            

            #텍스트 (각 리스트를 텍스트로 변환)
            tt2="● "+"".join(sangseee[:2])
            tt3="▶ "+"".join(sangseee[2:3])
            tt4="".join(sangseee[3:4])
            tt5="".join(sangseee[4:5])
            tt6="".join(sangseee[5:6])
            tt7="".join(sangseee[6:7])
            tt8="".join(sangseee[7:8])
            tt9="".join(sangseee[8:9])
            tt10="".join(sangseee[9:10]) 

            bh=120 #첫줄위치(세로)
            bhh=30 #줄간격 (세로)
            ImageDraw.Draw(jimcanvas).text(xy=(20,100), text=tt2, font=sangsefm, fill=(30,30,30)) 
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*1)), text=tt3[:65], font=sangsefm, fill=(30,30,30))      
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*2)), text=tt3[65:], font=sangsefm, fill=(30,30,30))      
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*3)), text=tt4[:65], font=sangsefs, fill=(60,60,60))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*4)), text=tt4[65:], font=sangsefs, fill=(60,60,60))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*5)), text=tt5[:65], font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*6)), text=tt5[65:], font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*7)), text=tt6[:65], font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*8)), text=tt6[65:], font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*9)), text=tt7[:65], font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*10)), text=tt7[65:], font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*11)), text=tt8[:65], font=sangsefs, fill=(80,80,80))                                   
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*12)), text=tt8[65:], font=sangsefs, fill=(80,80,80))                                   
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*13)), text=tt9[:65], font=sangsefs, fill=(80,80,80))                                   
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*14)), text=tt9[65:], font=sangsefs, fill=(80,80,80))                                   
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*15)), text=tt10[:65], font=sangsefs, fill=(80,80,80))                                  
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*16)), text=tt10[65:], font=sangsefs, fill=(80,80,80))                                 
            jimcanvas.save('C:/Users/ME/Pictures/'+tdate+code+'/output/'+ str(n)+'head.jpg')
            jm.close() 

        except ValueError:
            pass   
        except HTTPError:
            pass
        except URLError:
            pass
        except FileNotFoundError:
            pass       



        #썸네일 이미지저장
        try:
            urllib.request.urlretrieve(ksum,'C:/Users/ME/Pictures/'+tdate+code+'/cr/'+ str(n)+'_cr.jpg')    #이미지파일 저장  
            im=Image.open('C:/Users/ME/Pictures/'+tdate+code+'/cr/'+ str(n)+'_cr.jpg')        #이미지 사이즈 조정 
            im=im.resize((600,600))

            image = Image.new("RGB", (650, 650), "white")   #새로운 캔버스 만들기

            Eimage= Image.new("RGB",(1,1), "white") #1필셀이미지만들기
            Eimage.save('C:/Users/ME/Pictures/'+tdate+code+'/output/event.jpg') 

            image.paste(im,(10,50))                         #이미지 먼저 붙이자         


            grayg=Image.new("RGB",(650,100),(56,56,56))   #아래 검정색 바탕띠
            image.paste(grayg,(0,550))

            
            redg=Image.new("RGB",(140,150),(255,61,70))   #위 빨간색 바탕띠
            image.paste(redg,(500,0))
            


            text1=text1.replace("-","")  #파일명에 "-" 혹은 특수문자가 있으면 오류가 난다

            ImageDraw.Draw(image).text(xy=(10,560), text=text1, font=nameFont, fill="white", stroke_fill="black", stroke_width=2,)    #상품명
            ImageDraw.Draw(image).text(xy=(510,10), text="S2B", font=nameFont, fill="white", stroke_fill="red", stroke_width=2,)    #라벨
            ImageDraw.Draw(image).text(xy=(535,95), text="공식", font=label, fill="white", stroke_fill="red", stroke_width=1,)    #라벨


            image.save('C:/Users/ME/Pictures/'+tdate+code+'/cr/'+ str(n)+'_cr.jpg') 
    
            image.close()

        except ValueError:
            pass 
        except HTTPError:
            pass     
        except URLError:
            pass   
        except FileNotFoundError:
            pass


        n+=1 

print(now)
wb.save('C:/Users/ME/Pictures/'+str(now)[11:13]+str(now)[14:16]+'.xlsx')   # 엑셀시트저장하기
print("크롤링성공")

# 작업에 총 몇 초가 걸렸는지 출력합니다.
end_time = time.time()
print("The Job Took " + str(end_time - start_time) + " seconds.")



