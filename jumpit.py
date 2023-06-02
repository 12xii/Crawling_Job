from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs

browser = webdriver.Chrome(ChromeDriverManager().install()) # browser 변수에  chromeDriveManager 최신 버전 (자동 업데이트) 할당
browser.implicitly_wait(10) # 브라우저 로딩까지 10초간 대기

jumpitUrl = 'https://www.jumpit.co.kr/positions' # id parameter를 가져올 base url

browser.get(f'{jumpitUrl}') # webdriver_manager가 url에 접속하게 함

html = browser.page_source # 페이지에서 html을 추출
soup = bs(html, 'html.parser') # bs4 모듈로 html 파싱

urls = [] # 빈 리스트 생성

selects = str(soup.select('div .sc-fIosxK.fKzIXW > a')).replace('[', '').split('>,')
lengths = len(selects) # 총 공고 개수 가져오기

for i in range(lengths):
   urls.append(soup.select('div .sc-fIosxK.fKzIXW > a')[i]['href']) # urls 리스트에 각 id parameter 추가

# https://www.jumpit.co.kr + urls[n]