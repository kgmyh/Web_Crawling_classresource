# 피클로 저장된 뉴스리스트의 뉴스 크롤링 (기사제목, 내용)
# **스포츠 뉴스는 포멧이 다르다.**
# - 기사 제목: div#main_content > div.article_header > h3#articleTitle
#     ==> h3#articleTitle 로만 가능
# - 기사 내용: div#main_content  div#articleBodyContents
#      ==> div#articleBodyContents  로만 가능

#02에서 가져온 목록으로 뉴스 크롤링
# 끝나고 차후 다른 검색(블로그, 쇼핑 등) 도 해보도록
import requests
from bs4 import BeautifulSoup 
from bs4.element import Tag, Comment  #뒤에서 script 태그와 주석을 제거 하기 위해
import pickle
import pandas as pd

with open('인공지능_news_list.pkl','rb') as f:
    news_link_list = pickle.load(f)

news_content_list = []
for idx, url in enumerate(news_link_list):
    print(idx, url)
    if idx == 21:
        break
    res = requests.get(url)
    
    try: # 잘못된 url(sports 등 - 형식이 달라 안된다. except에서 continue시킨다.))
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'lxml')

            title = soup.select_one('h3#articleTitle').get_text().strip()
            

        #     javascript코드 상관없이 내용 읽어들이기
            content = soup.select_one('div#articleBodyContents').get_text().strip()  #여기선 주석은 알아서 빼준다.
        #  <script> 태그 제거 & 주석
            #간단버전
            content = content.replace('// flash 오류를 우회하기 위한 함수 추가','').replace('function _flash_removeCallback() {}','')
            
            # Comment 객체 또는 Tag객체인데 태그명이 script인 것은 뺀다.
            # NavigableString의 경우는 그냥 content에 붙인다.
            
            
        #     content_container = soup.select_one('div#articleBodyContents')
        #     content = ''
        #     for item in content_container:
        #         if type(item) == Comment or (type(item) == Tag and item.name == 'script'): #하나씩 할 때는 주석을 빼야 한다.
        #             continue

        #         if type(item) == Tag:
        #             content += item.get_text().strip()
        #         else: #NavigableString
        #             content += item

            news_content_list.append([title,content])
            
        else:
            print('오류발생:', res.status_code)
            print(res.text)
            
    except:
        print("{}번째 url 기사 읽는 도중 오류".format(idx))
        continue

#파일저장
df = pd.DataFrame(news_content_list,  columns=['기사제목','기사내용'])
print(df.head())