from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# 기본 설정
url = "https://starsportsmall.co.kr/goods/submain_new.asp"

# ChromeDriver 설정
chrome_service = Service(ChromeDriverManager().install())
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# 웹드라이버 시작
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
driver.get(url)

# URL 접근 확인
print("URL 접근 성공")

# 페이지 소스 출력 (확인용)
print(driver.page_source[:500])  # 페이지 소스의 처음 500자를 출력

driver.quit()
