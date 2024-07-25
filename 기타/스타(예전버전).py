
#--1. 작업세팅----------------------------------------------------------------------------------------------------------------
#1. 가격 인상률 설정 
priceR=1.0              #10%인상이면 1.1
#2. URL 변경  - {} 함께변경 주의!!
urlinput="https://starsportsmall.co.kr/goods/submain_new.asp?page={}&cate=0&sword=&swhat=&listsort=new&listtype=album&listsize=20&sprice="
#3. 크롤링 페이지 범위지정
rangeFir=1
raageLas=2
#4. 코드명변경(폴더명)
code="starstorts"
codek="스타스포츠"
#5.기준가 이상만 추출
Sprice = 20000

#-----------------------------------------------------------------------------------------------------------------------------



#--2. 기본 세팅 [헤드 불러오기 + 폴더만들기 ]------------------------------------------------------------------------------------ 
from crolling_sele_head import *                  #크롤링 헤드 
# 폴더 생성 (기존재하면 삭제 후 생성)----------------------------------
path_a='C:/Users/ME/Pictures/'+tdate+code
path_b='C:/Users/ME/Pictures/'+tdate+code+'/cr'
path_c='C:/Users/ME/Pictures/'+tdate+code+'/output'
if os.path.exists(path_a):
    shutil.rmtree(path_a)
os.mkdir(path_a)
os.mkdir(path_b)
os.mkdir(path_c)
#------------------------------------------------------------------------------------------------------------------------------



#--3. 크로링 작업 시작 [개별 상품정보 추출 후에   1. 상품명, 2.가격, 3.썸네일, 4. 옵션, 5. 상세페이지 정보 추출] ---------------------
# 개별정보 패턴 추출 -----------------------------------------------------------------

for j in range(rangeFir,raageLas):
    url=urlinput.format(j)

    req=requests.get(url,headers={"User-Agent": "Mozilla/5.0" })
    soup= bs(req.content, "html.parser")

    k=soup.select("div.mList1 ul li")
    #print(k)
    #exit()


    for i in k:
        #코드명
  #      codename=str(now)[3:4]+str(now)[5:7]+str(now)[8:10]+code+str(n)
   
    #가격
 #       try:
        price=i.select_one("span.pr").get_text(strip=True)
        #price=price.replace(",","")
        #price=price.replace("w","")
        #price=price[:-2]
 
         #  price=round(int(price)*priceR,-2)   #-priceR (5~15% 더 상승)
         #  except AttributeError:
         #  price=100      
    print(price)
    
    exit()

    #연결링크
        link=i.select_one("a")
        link=link["href"]
        link=link.replace("¶","&")
        site="https://starsportsmall.co.kr/goods/"
        link=site+link
        reqq=requests.get(link,headers={"User-Agent": "Mozilla/5.0" })
        soupp= bs(reqq.content, "html.parser")

 
    #상품명
        name=soupp.select_one("div.tit-area h3.tit").get_text(strip=True)
       
        text1=name   #썸네일 상품명
     

    #카테고리    
        cate="학교체육" 

                    
 
    #썸네일
        try:
         sumnail=soupp.select_one("div.photo-zone img#zoom_mw").get('src')
        except AttributeError:
            sumnail="뭐야"

        ksum=sumnail  

        #옵션(ppp)
        #셀레니움 헤드리스방식-------------------
        from selenium import webdriver

        opti = webdriver.ChromeOptions()
        opti.add_argument('headless')

        driver = webdriver.Chrome("./chromedriver",chrome_options=opti )  
        driver.implicitly_wait(2)  #잠깐쉬기
        #-------------------------------------
        driver.get(link)
        #time.sleep(1)

        html1 = driver.page_source
        options=[]

        #옵션재고 0일때 확인

        try:

            soup = bs(html1, 'html.parser')
            stock=soup.select_one("tbody tr input[name='stockL']")
            stock=int(stock["value"])
        except AttributeError:
            stock=0         
        except TypeError:
            stock=0

        #옵션명    
        for a in range(1,10):
            try:

                soup = bs(html1, 'html.parser')
                option=soup.select_one("tbody tr:nth-of-type({}) input[name='optionTxtL']".format(a))
                option=option["value"]
                
                
            except AttributeError:
                option="없음"
            except TypeError:
                option="없음"

            options.append(option)
            k="==0=10000=0=0=0=\n".join(options)
            pp=k.split("없음")[0]
            ppp="[필수선택]\n"+pp
        if ppp.count("10000")==1:          #옵션1개짜리 없애기
            ppp=""
        else:
            ppp   


    #상세페이지 (Tsangsee)
        sanseeA=[]    
        for p in range(1,5):
            try:
                asangsee=soupp.select_one("div.tab-con img:nth-of-type({})".format(p)).get("src")
                #asangsee="".join(asangsee)
              
                #asangsee=asangsee.split("없음")[0]
            except AttributeError:
                asangsee=""  
            except IndexError:
                asangsee=""  

            sanseeA.append(asangsee)    
        sansee1=sanseeA[0]
        sansee2=sanseeA[1]
        sansee3=sanseeA[2]
        

        if price>Sprice:     #가격 기준가 이상만 이미지추출조건
            sansee1
        else:
            sansee1=""

        if stock > 0:     #재고가 있어야 추출
            sansee1
        else:
            sansee1=""        


        if len(sansee1)>0:  #상세페이지가 없으면 썸네일도 없도록
            sansee2
        else:
            sansee2=""

        if len(sansee1)>0:  #상세페이지가 없으면 썸네일도 없도록
            sansee3
        else:
            sansee3=""


        if len(sansee1)>0:  #상세페이지가 없으면 썸네일도 없도록
            ksum
        else:
            ksum=""

        # -----------키워드 추출 후 상품명--------------------------------------------------
        keword=cate  #상품명 키워드
        keword=keword.replace("/","")
        keword=keword.replace(" ","")
        relKwdStat= RelKwdStat.RelKwdStat(KRW_API_URL,KWD_API_ACCESS_LICENSE,KWD_API_SECRET_KEY,KWD_API_CUSTOMER_ID_ID)
        kwdDataList= relKwdStat.get_rel_kwd_stat_list(None,hintKeywords=keword, showDetail='1')

        keyname=[]

        for outdata in kwdDataList[:4]:          #조회수 높은순 강도높음   
                relKeyword=outdata.relKeyword  #연관키워드
                compldx=outdata.compIdx              #PC광고기반 경쟁력
                keyname.append(relKeyword)



        for outdata in kwdDataList[4:20]:     #조회수 높은순 강동"중간,낮음"
                relKeyword=outdata.relKeyword  #연관키워드
                compldx=outdata.compIdx              #PC광고기반 경쟁력
                if compldx=="높음":
                        pass
                else:
                        keyname.append(relKeyword)

        keyname=" ".join(keyname)

        name=name+codek+" /"+keyname                                                  # "/sm/학교체육/뉴스포츠"+str(now)[3:4]+str(now)[5:7]+str(now)[8:10] 
       

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

        if len(sansee1)>0:     #상세페이지가 있는것만
            sheet.append([codename,g,c,d,e,name,g,g,cate,att,g,g,g,g,price,p,q,r,s,t,u,u,g,g,g,g,g,g,g,g,g,g,ag,ppp,g,g,ak,g,g,g,g,ap,g,ar,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,bi,bj,bj,bj,bj,bj,bj,bj,bj,bj,bbs,bj,bj,bj,bj,bj])

        else:
            pass




        #상세이이지저장
        try:
            urllib.request.urlretrieve(sansee1,'C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'_01.jpg')    #이미지파일 저장   
            jm1=Image.open('C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'_01.jpg')  #이미지 열기
            jm1_width=int(jm1.size[0])   
            jm1_height=int(jm1.size[1])

            if len(sansee2)>1:

                urllib.request.urlretrieve(sansee2,'C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'_02.jpg')    #이미지파일 저장   
                jm2=Image.open('C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'_02.jpg')  #이미지 열기
                jm2_height=int(jm2.size[1])
            else:
                jm2 = Image.new("RGB", (1,1), "white")     #이미지파일 저장   
                jm2_height=int(jm2.size[1])

            if len(sansee3)>1:
                urllib.request.urlretrieve(sansee3,'C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'_03.jpg')    #이미지파일 저장   
                jm3=Image.open('C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'_03.jpg')  #이미지 열기
                jm3_height=int(jm3.size[1])
            else:
                jm3 = Image.new("RGB", (1,1), "white")     #이미지파일 저장   
                jm3_height=int(jm3.size[1]) 


            jm = Image.new("RGB", (jm1_width,(jm1_height+jm2_height+jm3_height)), "white")   #새로운 캔버스 만들기
            jm.paste(jm1,(0,0))
            jm.paste(jm2,(0,jm1_height))
            jm.paste(jm3,(0,jm1_height+jm2_height))

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




            jimcanvas = Image.new("RGB", (860, 540), "white")   #새로운 캔버스 만들기 

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
            spec1= soupp.select_one("table.specTable tr:nth-of-type(1) th").get_text(strip=True)
            spec1_1=soupp.select_one("table.specTable tr:nth-of-type(1) td").get_text(strip=True)
            spec2= soupp.select_one("table.specTable tr:nth-of-type(2) th").get_text(strip=True)
            spec2_1=soupp.select_one("table.specTable tr:nth-of-type(2) td").get_text(strip=True)
            spec3= soupp.select_one("table.specTable tr:nth-of-type(3) th").get_text(strip=True)
            spec3_1=soupp.select_one("table.specTable tr:nth-of-type(3) td").get_text(strip=True)
            spec4= soupp.select_one("table.specTable tr:nth-of-type(4) th").get_text(strip=True)
            spec4_1=soupp.select_one("table.specTable tr:nth-of-type(4) td").get_text(strip=True)
            spec5= soupp.select_one("table.specTable tr:nth-of-type(5) th").get_text(strip=True)
            spec5_1=soupp.select_one("table.specTable tr:nth-of-type(5) td").get_text(strip=True)
            spec6= soupp.select_one("table.specTable tr:nth-of-type(6) th").get_text(strip=True)
            spec6_1=soupp.select_one("table.specTable tr:nth-of-type(6) td").get_text(strip=True)
            spec7= soupp.select_one("table.specTable tr:nth-of-type(7) th").get_text(strip=True)
            spec7_1=soupp.select_one("table.specTable tr:nth-of-type(7) td").get_text(strip=True)
            spec8= soupp.select_one("table.specTable tr:nth-of-type(8) th").get_text(strip=True)
            spec8_1=soupp.select_one("table.specTable tr:nth-of-type(8) td").get_text(strip=True)
            spec9= soupp.select_one("table.specTable tr:nth-of-type(9) th").get_text(strip=True)
            spec9_1=soupp.select_one("table.specTable tr:nth-of-type(9) td").get_text(strip=True)
            spec10= soupp.select_one("table.specTable tr:nth-of-type(10) th").get_text(strip=True)
            spec10_1=soupp.select_one("table.specTable tr:nth-of-type(10) td").get_text(strip=True)

            tt2=spec1+": "+spec1_1
            tt3=spec2+": "+spec2_1
            tt4=spec3+": "+spec3_1
            tt5=spec4+": "+spec4_1
            tt6=spec5+": "+spec5_1
            tt7=spec6+": "+spec6_1
            tt8=spec7+": "+spec7_1
            tt9=spec8+": "+spec8_1
            tt10=spec9+": "+spec9_1
            tt11=spec10+": "+spec10_1


            bh=120 #첫줄위치(세로)
            bhh=30 #줄간격 (세로)
            ImageDraw.Draw(jimcanvas).text(xy=(20,100), text=tt2, font=sangsefm, fill=(30,30,30)) 
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*1)), text=tt3,font=sangsefs, fill=(30,30,30))      
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*2)), text=tt4,font=sangsefs, fill=(30,30,30))      
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*3)), text=tt5,font=sangsefs, fill=(60,60,60))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*4)), text=tt6,font=sangsefs, fill=(60,60,60))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*5)), text=tt7,font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*6)), text=tt8,font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*7)), text=tt9,font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*8)), text=tt10[:60], font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*9)), text=tt10[60:120], font=sangsefs, fill=(80,80,80))
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*10)), text=tt10[120:], font=sangsefs, fill=(80,80,80))           
            ImageDraw.Draw(jimcanvas).text(xy=(20,bh+(bhh*11)), text=tt11, font=sangsefs, fill=(80,80,80))   
            
                                                 
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
        except AttributeError:
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
            
            nameFont = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 65)
            label = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 40)

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

