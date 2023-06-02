# https://www.jobkorea.co.kr/recruit/joblist?menucode=duty&dutyCtgr=10031#anchorGICnt_${i}

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
import re

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.implicitly_wait(3)

browser.get('https://www.jobkorea.co.kr/recruit/joblist?menucode=duty&dutyCtgr=10031')

html = browser.page_source
soup = bs(html, 'html.parser')

length = int((re.sub(r'[^0-9]', '', str(soup.select('button > span > em'))))) + 40

div, pl = divmod(length, 40)

urls = []

for i in range(1) :
    jobKoreaUrl = f'https://www.jobkorea.co.kr/recruit/joblist?menucode=duty&dutyCtgr=10031#anchorGICnt_${i}'

    browser.get(f'{jobKoreaUrl}')

    htmls = browser.page_source
    soups = bs(htmls, 'html.parser')

    for j in range(40):
        urls.append(soups.select('div .tplJobListWrap.devTplTabBx > div > table > tbody > tr > td > div > strong > a')[j]['href'])

# https://jobkorea.co.kr + urls[n]