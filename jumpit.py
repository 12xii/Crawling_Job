from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs

browser = webdriver.Chrome(ChromeDriverManager().install())
browser.implicitly_wait(3)

jumpitUrl = 'https://www.jumpit.co.kr/positions'

browser.get(f'{jumpitUrl}')

html = browser.page_source
soup = bs(html, 'html.parser')

urls = []

selects = str(soup.select('div .sc-fIosxK.fKzIXW > a')).replace('[', '').split('>,')

lengths = len(selects)

for i in range(lengths):
   urls.append(soup.select('div .sc-fIosxK.fKzIXW > a')[i]['href'])