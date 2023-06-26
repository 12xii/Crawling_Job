import os    
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from wordcloud import WordCloud
import numpy as np
from collections import Counter
from konlpy.tag import Okt
from matplotlib import pyplot as plt
import re

browser = webdriver.Chrome(ChromeDriverManager().install()) # browser 변수에  chromeDriveManager 최신 버전 (자동 업데이트) 할당
browser.implicitly_wait(10) # 브라우저 로딩까지 10초간 대기

jumpitUrl = 'https://www.jumpit.co.kr/positions' # id parameter를 가져올 base url

browser.get(f'{jumpitUrl}') # webdriver_manager가 url에 접속하게 함

html = browser.page_source # 페이지에서 html을 추출
soup = bs(html, 'html.parser') # bs4 모듈로 html 파싱

urls = [] # 빈 리스트 생성

selects = str(soup.select('div .sc-fIosxK.fKzIXW > a')).replace('[', '').split('>,')
length = len(selects) # 총 공고 개수 가져오기

for i in range(length):
   param = soup.select('div .sc-fIosxK.fKzIXW > a')[i]['href'] # 각 id parameter 가져오기
   urls.append(f'https://www.jumpit.co.kr{param}') # urls 리스트에 각 id parameter를 추가한 URL 추가

# https://www.jumpit.co.kr + urls[n]

ceritifies = ''

for i in range(length):
    try:
        browser.get(urls[i])

        soup = str(bs(browser.page_source, 'html.parser').select('.JobDescription_JobDescription__VWfcb span')) # 게시글 내용 가져옴

        ceritify = soup.split('<span>')[3].replace('</span>', '').replace('<br/>', '') # 자격요건
        # then = soup.split('<span>')[4].replace('</span>', '').replace('<br/>', '').split('•') #우대사항

        ceritifies += ceritify
    except IndexError:
        print(soup)
        ceritify = ''
        ceritifies += ceritify
        

# count = Counter(Okt().morphs(phrase=ceritifies, stem=True))

# for leng in count :
#      if(len(leng) <= 1): del count[leng]

c = Okt().morphs(phrase=ceritifies, stem=True)

c = [re.sub('[^가-힣a-zA-Z0-9]', '', word) for word in c]

count = Counter(c)




sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True) # 빈도수 내림차순으로 정렬


sorted_count = sorted_count[:10] # 상위 n개의 아이템만 남기고 제외


count = dict(sorted_count) # 정렬된 빈도수 정보를 다시 딕셔너리로 변환

wc = WordCloud(
     font_path=font_path, # 서체 지정
       width= 400, 
       height=400, 
       scale=2.0, 
       max_font_size=100, 
       background_color="white", 
       collocations=False
     ).generate_from_frequencies(count)


wc.to_file('test.png') # 파일로 다운로드

# 그래프 설정
plt.figure(figsize=(10, 6))
plt.bar(count.keys(), count.values())
plt.xticks(rotation=45)
plt.xlabel('단어')
plt.ylabel('빈도수')
plt.title('단어 빈도수')
plt.rcParams['font.family'] = 'NanumGothic'

# 그래프 저장
plt.savefig('graph.png')

# 그래프 출력
plt.show()