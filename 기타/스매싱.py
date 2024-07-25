#--1. 작업세팅----------------------------------------------------------------------------------------------------------------
#1. 가격 인상률 설정  (#10%인상이면 1.1)
priceR=1.1              
#2. URL 변경  - {} 함께변경 주의!!
urlinput="https://smashingsports.co.kr/shop/shopbrand.html?s_type=search_engine_finder&sort=order&page={}&finder_type=custom&keyword=%C5%B0%B5%E5%C1%FC&money1=&money2=&add_keyword="
#3. 크롤링 페이지 범위지정 (1~4페이지이면 1,5로 입력)
rangeFir=1
raageLas=11
#4. 코드명설정 (폴더명)
code="smashing"
codek="스매싱"
#5.기준가 이상만 추출
Sprice =10000
#-----------------------------------------------------------------------------------------------------------------------------



#--2. 기본 세팅 [헤드 불러오기 + 폴더만들기 ]------------------------------------------------------------------------------------ 
from crolling_head import *                  #크롤링 헤드 
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

    k=soup.select("div.tb-center")
#    print(k)

    #1. 상품명
    for i in k:
        nam=i.select_one("li.dsc").get_text(strip=True) 
    


        nam1=nam.split(" ")       #상품명뽑기    (스매싱 스포츠만 적용 아래내줄까지)
        text1=" ".join(nam1[2:4])
        nam=" ".join(nam1[:5]) 
        name=nam.replace("- ","") 

        codename=str(now)[3:4]+str(now)[5:7]+str(now)[8:10]+code+str(n)
        #print(name)        


    #가격-price 
        try:
            pric=i.select_one("li.price").get_text(strip=True)    
            pric=pric.replace(",","")
            price=pric.split('원')[0].replace(",", "")
            price=round(int(price)*priceR,-2)
        except AttributeError:
            price="가격전화문의"

        # print(name,price)


                                          
     #상품 링크 ()   
        link=i.select_one("a").get('href')                                                         #(링크추출)
                                                                                                   
        urll="http://smashingsports.co.kr"+link                                                                                            #1deep페이지 시작
        reqq=requests.get(urll,headers={"User-Agent": "Mozilla/5.0" })
        soupp= bs(reqq.content, "html.parser")


        name=name+" /"+ "sm/학교체육/뉴스포츠"+str(now)[3:4]+str(now)[5:7]+str(now)[8:10] 


    #카테고리    
        cate="학교체육" 
        # cate=soupp.select_one("font#MK_xcodename").get_text(strip=True)                 #(카테고리) 불필요
        #-------------------------------------------------------------------------------------


        #썸네일
        try:
            sumnail=soupp.select_one("div.thumb-wrap img.detail_image").get('src')       
            sumnail = re.split(r'\?', sumnail)         #jpg 뒤에 이상한 문자들이 붙어서 jpg이후 삭제
            sumnail = sumnail[0]
        except AttributeError:
            sumnail="뭐야"

        ksum="http://smashingsports.co.kr"+sumnail  

        # print(ksum)
      
        #옵션(ppp)
        options=[]
        for a in range(2,20):
            try:
                option=soupp.select_one("select[name='optionlist[]'] option:nth-of-type({})".format(a)).get_text(strip=True) 
                option=option.replace("\n","")
                option=option.replace("  ","")            
          
            except AttributeError:
                option="없음"

            options.append(option)

            k="==0=10000=0=0=0=\n".join(options)
            c=k.replace(" (+","==")
            s=c.replace("원)==0","")
            ss=s.replace("원)(품절)==0","") 
            ss=ss.replace("품절","상품준비중(미정)")    
            p=ss.replace(",","")
            pp=p.split("없음")[0]
            ppp="[필수선택]\n"+pp[:-1]
        if ppp.count("10000")==1:          #옵션1개짜리 없애기
            ppp=""
        else:
            ppp     
        if ppp.count("10000")==0:          #옵션없는것 필수선택없애기
            ppp=""
        else:
            ppp   
            # print(ppp)    

        # print(name)



        #상세페이지 (Tsangsee)
        # "OPENEDITOR" 주석 이후와 "하단공통정보 삽입" 주석 이전의 이미지 추출
        openeditor_comment = soupp.find(text=lambda text: text and 'OPENEDITOR' in text)
        end_common_info_comment = soupp.find(text=lambda text: text and '하단공통정보 삽입' in text)

        if openeditor_comment and end_common_info_comment:
            images_between_comments = openeditor_comment.find_all_next('img')
            
            # jpg 파일만 출력
            for img in images_between_comments:
                try:
                    img_url = img['src']
                    if img_url.lower().endswith('.jpg') and end_common_info_comment not in img.parents:
                        Tsangsee=img_url
                except KeyError:
                    pass  # 'src' 속성이 없는 경우 이미지 URL을 가져올 수 없으므로 예외 처리
        else:
            pass


          
        if price>Sprice:     #가격 기준가 이상만 이미지추출조건
            Tsangsee
        else:
            Tsangsee=""

        if len(Tsangsee)>0:  #상세페이지가 없으면 썸네일도 없도록
            ksum
        else:
            ksum=""


     


        g=""  #공백
        c=codek #브랜드
        d=codek #제조사
        e="국내=서울=강남구" #원산지
        att=code+tdate
        p="선결제"
        q="3500"
        r="0"
        s="y"
        t="9000"

        u="http://ai.esmplus.com/tstkimt/"+tdate+code+"/cr/"+str(n)+"_cr.jpg"    #날짜 수정할것
        if ppp=="":
            ag=""
        else:
            ag="SM"
        ak="<center> <img src='http://gi.esmplus.com/tstkimtt/head.jpg' /><br>  \
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

        if len(Tsangsee)>0:     #상세페이지가 있는것만
            sheet.append([codename,g,c,d,e,name,g,g,cate,att,g,g,g,g,price,p,q,r,s,t,u,u,g,g,g,g,g,g,g,g,g,g,ag,ppp,g,g,ak,g,g,g,g,ap,g,ar,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,bi,bj,bj,bj,bj,bj,bj,bj,bj,bj,bbs,bj,bj,bj,bj,bj,ksum,Tsangsee])

        else:
            pass




        #상세이이지저장
        try:
            urllib.request.urlretrieve(Tsangsee,'C:/Users/ME/Pictures/'+tdate+code+'/'+ str(n)+'.jpg')    #이미지파일 저장   
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
            im=im.resize((400,400))

            image = Image.new("RGB", (600, 600), "white")   #새로운 캔버스 만들기

            Eimage= Image.new("RGB",(1,1), "white") #1필셀이미지만들기
            Eimage.save('C:/Users/ME/Pictures/'+tdate+code+'/output/event.jpg') 
           


            grayg=Image.new("RGB",(600,100),(56,56,56))   #아래 검정색 바탕띠
            image.paste(grayg,(0,500))

            
            redg=Image.new("RGB",(150,150),(255,61,70))   #위 빨간색 바탕띠
            image.paste(redg,(440,0))
            
            nameFont = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 65)
            label = ImageFont.truetype("C:/Windows/Fonts/NanumGothicExtraBold.ttf", 40)

            text1=text1.replace("-","")  #파일명에 "-" 혹은 특수문자가 있으면 오류가 난다

            ImageDraw.Draw(image).text(xy=(10,510), text=text1, font=nameFont, fill="white", stroke_fill="black", stroke_width=2,)    #상품명
            ImageDraw.Draw(image).text(xy=(460,10), text="S2B", font=nameFont, fill="white", stroke_fill="red", stroke_width=2,)    #라벨
            ImageDraw.Draw(image).text(xy=(505,95), text="공식", font=label, fill="white", stroke_fill="red", stroke_width=1,)    #라벨
            image.paste(im,(100,100))                         #캔버스를 중앙에 넣어보자 100xp씩 우로,밑으로 

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


