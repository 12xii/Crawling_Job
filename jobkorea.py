# https://www.jobkorea.co.kr/recruit/joblist?menucode=duty&dutyCtgr=10031#anchorGICnt_${i}

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import re

browser = webdriver.Chrome(ChromeDriverManager().install()) # browser 변수에  chromeDriveManager 최신 버전 (자동 업데이트) 할당
browser.implicitly_wait(10) # 브라우저 로딩까지 10초간 대기

browser.get('https://www.jobkorea.co.kr/recruit/joblist?menucode=duty&dutyCtgr=10031') # webdriver_manager가 url에 접속하게 함

html = browser.page_source # 페이지에서 html을 추출
soup = bs(html, 'html.parser') # bs4 모듈로 html 파싱

length = int((re.sub(r'[^0-9]', '', str(soup.select('button > span > em'))))) + 40 # 정규식 활용 전체 공고 개수 확인

div, pl = divmod(length, 40) # 페이지네이션된 총 페이지 수 확인

urls = [] # 빈 리스트 생성

for i in range(1) :
    jobKoreaUrl = f'https://www.jobkorea.co.kr/recruit/joblist?menucode=duty&dutyCtgr=10031#anchorGICnt_${i}' # id parameter를 가져올 base url

    browser.get(f'{jobKoreaUrl}') # webdriver_manager가 url에 접속하게 함

    htmls = browser.page_source # 페이지에서 html을 추출
    soups = bs(htmls, 'html.parser') # bs4 모듈로 html 파싱

    for j in range(40): # 페이지네이션 된 페이지 당 공고는 최대 40개씩 할당되어있음
        urls.append(soups.select('div .tplJobListWrap.devTplTabBx > div > table > tbody > tr > td > div > strong > a')[j]['href']) # urls 리스트에 각 id parameter 추가

# https://jobkorea.co.kr + urls[n]