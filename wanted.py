import os
import time    
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as bs
from wordcloud import WordCloud
from collections import Counter
from konlpy.tag import Okt
from matplotlib import pyplot as plt
from matplotlib import rc
import matplotlib as mpl
import re
import numpy as np
import matplotlib.font_manager as fm

# 나눔고딕 폰트 경로 설정
font_path = 'NanumGothic.ttf'

rc('font', family = 'Arial Unicode MS') # 폰트 문제 해결
plt.rcParams["font.family"] = 'NanumGothicOTF'

with open('stop_words.txt', 'r') as file:
    stop_words = file.readline().split('|')

browser = webdriver.Chrome(ChromeDriverManager().install()) 

# browser 변수에  chromeDriveManager 최신 버전 (자동 업데이트) 할당
browser.implicitly_wait(10) # 브라우저 로딩까지 10초간 대기

wantedUrl = 'https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=company.response_rate_order&years=-1&locations=all' # id parameter를 가져올 base url

browser.get(f'{wantedUrl}') # webdriver_manager가 url에 접속하게 함

actions = browser.find_element(By.CSS_SELECTOR, 'body')

html = browser.page_source # 페이지에서 html을 추출
soup = bs(html, 'html.parser') # bs4 모듈로 html 파싱

urls = [] # 빈 리스트 생성

for i in range(10):
    urls = []
    for i in browser.find_elements(By.CSS_SELECTOR, "div .Card_className__u5rsb > a"):
        a = i.get_property('href')
        urls.append(a)
    actions.send_keys(Keys.END)
    time.sleep(2)

ceritifies = ''
tag = ''
three = ''
four = ''
ten = ''

for i in range(len(urls)):
    try:
        browser.get(urls[i])

        soup = str(bs(browser.page_source, 'html.parser').select('.JobDescription_JobDescription__VWfcb span')) # 게시글 내용 가져옴
        tags = bs(browser.page_source, 'html.parser').select('.Tags_tagsClass__mvehZ ul li a')
        for l in range(len(tags)):
            thisTag = tags[l].get_text()

            if '설립3년이하' in thisTag:
                for j in range(len(soup.split('<span>')[3].split('•'))):
                    three += soup.split('<span>')[3].replace('</span>', '').replace('<br/>', '').split('•')[j]
            elif '설립4~9년' in thisTag:
                for j in range(len(soup.split('<span>')[3].split('•'))):
                    four += soup.split('<span>')[3].replace('</span>', '').replace('<br/>', '').split('•')[j]
            elif '설립10년이상' in thisTag:
                for j in range(len(soup.split('<span>')[3].split('•'))):
                    ten += soup.split('<span>')[3].replace('</span>', '').replace('<br/>', '').split('•')[j]

        ceritify = soup.split('<span>')[3].replace('</span>', '').replace('<br/>', '').split('•') # 자격요건
        # then = soup.split('<span>')[4].replace('</span>', '').replace('<br/>', '').split('•') #우대사항

        for j in range(len(ceritify)):
            ceritifies += ceritify[j + 1]
    except IndexError:
        for l in range(len(tags)):
            thisTag = tags[l].get_text()

            if '설립3년이하' in thisTag:
                three += ''
            elif '설립4~9년' in thisTag:
                four += ''
            elif '설립10년이상' in thisTag:
                ten += ''
        ceritify = ''
        ceritifies += ceritify

c = Okt().morphs(phrase=ceritifies, stem=True)
t = Okt().morphs(phrase=three, stem=True)
f = Okt().morphs(phrase=four, stem=True)
te = Okt().morphs(phrase=ten, stem=True)

c = [re.sub('[^가-힣a-zA-Z0-9]', '', word) for word in c]
three = [re.sub('[^가-힣a-zA-Z0-9]', '', word) for word in t]
four = [re.sub('[^가-힣a-zA-Z0-9]', '', word) for word in f]
ten = [re.sub('[^가-힣a-zA-Z0-9]', '', word) for word in te]

count = Counter(c)
three = Counter(three)
four = Counter(four)
ten = Counter(ten)

count = {k: v for k, v in count.items() if k not in stop_words}
three = {k: v for k, v in three.items() if k not in stop_words}
four = {k: v for k, v in four.items() if k not in stop_words}
ten = {k: v for k, v in ten.items() if k not in stop_words}

keys = list(count.keys())
values = list(count.values())

sorted_count = sorted(count.items(), key=lambda x: x[1], reverse=True) # 빈도수 내림차순으로 정렬

sorted_count = sorted_count[:25] # 상위 n개의 아이템만 남기고 제외

three = sorted(three.items(), key=lambda x: x[1], reverse=True)
three = three[:25]
four = sorted(four.items(), key=lambda x: x[1], reverse=True)
four = four[:25]
ten = sorted(ten.items(), key=lambda x: x[1], reverse=True)
ten = ten[:25]

count = dict(sorted_count) # 정렬된 빈도수 정보를 다시 딕셔너리로 변환
t = dict(three)
f = dict(four)
te = dict(ten)

print(t, f, te)

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

colors = ['lavenderblush', 'pink', 'lightpink', 'midnightblue', 'navy', 'darkblue', 'mediumblue', 'blue', 'slateblue', 'mediumpurple', 
                'mediumorchid', 'darkorchid', 'blueviolet']

# 그래프 설정
plt.figure(figsize=(10, 6))
plt.xticks(rotation=45)
font_name = fm.FontProperties(fname=font_path, size=15).get_name()
plt.rc('font', family=font_name)
plt.barh(list(count.keys()), list(count.values()), color=colors, alpha = 0.7)
plt.xlabel('빈도수')
plt.ylabel('단어')
plt.title('단어 빈도수', fontdict={
    'fontsize' : 25,
    'fontweight' : 'bold',
}, pad=25)

# 그래프 저장
plt.savefig('graph.png')

# 그래프 출력
plt.show()

# 연차별
# three : 3년차 이하
# four : 4 ~ 9년차
# ten : 10년차 이상


### 3년차 이하

print(f)
plt.rcParams["font.family"] = 'NanumGothicOTF'

sizes = t.values()
label = t.keys()
explode = list(np.zeros(len(t)))
explode[0] = 0.1
explode[1] = 0.1
explode[2] = 0.1


fig1, ax1 = plt.subplots()

ax1.pie(sizes, labels=label, labeldistance=1.2, explode=explode, autopct='%1.1f%%', pctdistance= 1.1,
        shadow=True, startangle=-50, colors=colors)

ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# plt.rcParams['font.family'] = 'NanumGothicOTF'
plt.annotate("most", xy=(0.7,-0.4), xytext=(0.4,0.3), arrowprops=dict(facecolor='white'))
plt.title('Talents required by companies with\nless than 3 years of establishment', fontdict={
    'fontsize' : 25,
    'fontweight' : 'bold',
}, pad=25)

### 4년차 ~ 9년차

plt.savefig('three.png')
plt.show()

plt.rcParams["font.family"] = 'NanumGothicOTF'

sizes = f.values()
label = f.keys()
explode = list(np.zeros(len(f)))
explode[0] = 0.1


fig1, ax1 = plt.subplots()

ax1.pie(sizes, labels=label, labeldistance=1.2, explode=explode, autopct='%1.1f%%', pctdistance= 1.1,
        shadow=True, startangle=-50, colors=colors)

ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# plt.rcParams['font.family'] = 'NanumGothicOTF'
plt.annotate("most", xy=(0.5,-0.2), xytext=(0.4,0.3), arrowprops=dict(facecolor='white'))
plt.title('Established year 4 ~ 9 years Talents\nrequired by companies', fontdict={
    'fontsize' : 25,
    'fontweight' : 'bold',
}, pad=25)

print('# 설정 되어있는 폰트 글꼴')
print (plt.rcParams['font.family'] )

plt.savefig('four.png')
plt.show()


### 10년차 이상

plt.rcParams["font.family"] = 'NanumGothicOTF'

sizes = te.values()
label = te.keys()
explode = list(np.zeros(len(ten)))
explode[0] = 0.1


fig1, ax1 = plt.subplots()

ax1.pie(sizes, labels=label, labeldistance=1.2, explode=explode, autopct='%1.1f%%', pctdistance=1.1,
        shadow=True, startangle=-50, colors=colors)

ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# plt.rcParams['font.family'] = 'NanumGothicOTF'
plt.annotate("most", xy=(0.5,-0.2), xytext=(0.4,0.3), arrowprops=dict(facecolor='white'))
plt.title('Talents required by companies with\nmore than 10 years of establishment', fontdict={
    'fontsize' : 25,
    'fontweight' : 'bold',
}, pad=25)

print('# 설정 되어있는 폰트 글꼴')
print (plt.rcParams['font.family'] )

plt.savefig('ten.png')
plt.show()