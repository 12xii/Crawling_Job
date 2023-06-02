from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs

browser = webdriver.Chrome(ChromeDriverManager().install()) # browser 변수에  chromeDriveManager 최신 버전 (자동 업데이트) 할당
browser.implicitly_wait(10) # 브라우저 로딩까지 10초간 대기

wantedUrl = 'https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&locations=all' # id parameter를 가져올 base url

browser.get(f'{wantedUrl}') # webdriver_manager가 url에 접속하게 함

html = browser.page_source # 페이지에서 html을 추출
soup = bs(html, 'html.parser') # bs4 모듈로 html 파싱

urls = [] # 빈 리스트 생성

length = len(str(soup.select('div .List_List_container__JnQMS > ul > li > div > a')).split('<a aria-label')) - 1 # 총 공고 개수 가져오기

for i in range(length):
    urls.append(soup.select('div .List_List_container__JnQMS > ul > li > div > a')[i]['href']) # urls 리스트에 각 id parameter 추가

# https://www.wanted.co.kr + urls[n]