from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.implicitly_wait(10)

wantedUrl = 'https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&locations=all'

browser.get(f'{wantedUrl}')

html = browser.page_source
soup = bs(html, 'html.parser')

urls = []

length = len(str(soup.select('div .List_List_container__JnQMS > ul > li > div > a')).split('<a aria-label')) - 1

for i in range(length):
    urls.append(soup.select('div .List_List_container__JnQMS > ul > li > div > a')[i]['href'])

