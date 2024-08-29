#--작업세팅------------------------------------------------------------
#1. 가격 인상률 설정 
priceR=1              #10%인상이면 1.1
#2. URL 변경  - {} 함께변경 주의!!
urlinput="https://kidus.co.kr/product/outer.html?cate_no=72&page={}"
#3. 크롤링 페이지 범위지정
rangeFir=1
raageLas=6
#4. 코드명변경(폴더명)
code="kidus"
codek="키더스" #오성은 헤더값변경했음 확인할것~!!
#5.기준가 이상만 추출
Sprice = 5000
#---------------------------------------------------------------------

from crolling_head import *

# 폴더 생성 (기존재하면 삭제 후 생성)
path_a='C:/Users/ME/Pictures/'+tdate+code
path_b='C:/Users/ME/Pictures/'+tdate+code+'/cr'
path_c='C:/Users/ME/Pictures/'+tdate+code+'/output'
if os.path.exists(path_a):
    shutil.rmtree(path_a)
os.mkdir(path_a)
os.mkdir(path_b)
os.mkdir(path_c)
#--------------------------------------------------------------------
# <코딩시작>
for j in range(rangeFir,raageLas):
    url=urlinput.format(j)
    req=requests.get(url,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36" })
    soup= bs(req.content, "html.parser")

    k=soup.select("div ul li.item.xans-record-")                                         #도는 패턴
    #print(k)
 
    for i in k:
        #코드명
        codename=str(now)[3:4]+str(now)[5:7]+str(now)[8:10]+code+str(n)
        
        #상품명    
        name=i.select_one("p.name").get_text(strip=True)
        name=name.replace("상품명:","")
        text1=name       #썸네일 상품명
        #print(name)

        #가격
        try:
            price=i.select_one('li.xans-record-:nth-of-type(2)') .get_text(strip=True)
            price=price.replace("판매가:","")            
            price=price.replace(",","")
            price=price.replace("원","")
            price=price.replace(" ","")
            price=round(int(price)*priceR,-2) #백원단위 반올림 #-priceR (5~15% 더 상승)
        except AttributeError:
            price=100    
        except ValueError:            
            price=100   
        #print(price)
            #썸네일
        try:
         sumnail=i.select_one("div.box img ").get('src')
        except AttributeError:
            sumnail="뭐야"

        ksum="http:"+sumnail  
        #print(ksum)

    #연결링크
        link=i.select_one("a")
        link=link["href"]
        site="http://kidus.co.kr/"
        link=site+link
        reqq=requests.get(link,headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36" })
        soupp= bs(reqq.content, "html.parser")
        #print(link)
      
    #카테고리    
        cate="학교체육" 
                    
        options=[]
        for a in range(1,10):
            try:
                option=soupp.select_one("select#product_option_id1 optgroup option:nth-of-type({})".format(a)).get_text(strip=True) 
           
            except AttributeError:
                option="없음"

            options.append(option)
            k="==0=10000=0=0=0=\n".join(options) 
            k=k.replace(" (+","==")      #추가금액 시작
            k=k.replace("원)==0","")
            k=k.replace("원)(품절)==0","")   #추가금액 끝
            k=k.replace(",","")                                                            
            k=k.replace("품절","상품준비중(미정)")    
            k=k.split("없음")[0]
            ppp="[필수선택]\n"+k
        if len(ppp)==7:          #옵션1개짜리 없애기
            ppp=""
        else:
            ppp    
        #print(ppp)
      
    #상세페이지 (Tsangsee)
        try:
            sangsee=soupp.select('div#prdDetail img[ec-data-src*=web]')#.get("src")
            sangsee=sangsee[1]
            sangsee=site+sangsee["ec-data-src"]
        except AttributeError:
            sangsee=""  
        except IndexError:
            sangsee=""  
        #print(sangsee)    
      
        if price>Sprice:     #가격 기준가 이상만 이미지추출조건
            sangsee
        else:
            sangsee=""



        if len(sangsee)>0:  #상세페이지가 없으면 썸네일도 없도록
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

        name=name+" "+codek+" /"+keyname                                                  # "/sm/학교체육/뉴스포츠"+str(now)[3:4]+str(now)[5:7]+str(now)[8:10] 
       #-------------------------------------------------------------------------------------
        g=""  #공백
        c=codek #브랜드
        d=codek #제조사
        e="국내=서울=강남구" #원산지
        att=tdate+code
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
                                                                <img src='http://gi.esmplus.com/tstkimtt/deliver.jpg' /></center>"
                                              
        ap="쿠폰"
        ar="c"
        bi="25"
        bj="상세설명일괄참조"
        bbs="N"

        if len(sangsee)>0:     #상세페이지가 있는것만
            sheet.append([codename,g,c,d,e,name,g,g,cate,att,g,g,g,g,price,p,q,r,s,t,u,u,g,g,g,g,g,g,g,g,g,g,ag,ppp,g,g,ak,g,g,g,g,ap,g,ar,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,bi,bj,bj,bj,bj,bj,bj,bj,bj,bj,bbs,bj,bj,bj,bj,bj])

        else:
            pass

        #상세이이지저장
        try:
            urllib.request.urlretrieve(sangsee,'C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'_01.jpg')    #이미지파일 저장   
            jm=Image.open('C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'_01.jpg')  #이미지 열기


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
            im=im.resize((550,550))

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
            ImageDraw.Draw(image).text(xy=(510,10), text="핫한", font=nameFont, fill="white", stroke_fill="red", stroke_width=2,)    #라벨
            ImageDraw.Draw(image).text(xy=(535,95), text="꿀탬", font=label, fill="white", stroke_fill="red", stroke_width=1,)    #라벨


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

