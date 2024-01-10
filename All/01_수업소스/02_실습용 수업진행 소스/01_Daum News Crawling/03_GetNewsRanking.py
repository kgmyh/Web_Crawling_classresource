# 다음 일자별 랭킹 뉴스 링크 

#-------------------------------------------------------
# 목록에 링크가 있고 링크를 클릭하면 세부사항이 있는 경우
# 목록을 따라가면서 크롤링 하나 목록에서 링크를 크롤링 하고 그 링크를 반복하면서 내용을 크롤링하나.
# (동시에? 따로)
# 성능상 차이는 없다.
# 링크를 크롤링하고 그 다음에 내용을 크롤링 하는 것이 효율적이다.
# 이유
# 1. 크롤링중 에러 나면 어디서 났는지 확인이 쉽고, 더 중요한 것은 이어서 하기가 용이하다. (목록에서 에러난 것 부터 하면 되므로)
# 2. 컴퓨터가 여러대면 목록의 내용을 나눠서 할 수 있으므로 빠르게 처리할 수 있다.
#-------------------------------------------------------


# https://media.daum.net/ranking/랭킹종류
#   랭킹종류: popular(많이본), kkomkkom(열독률), bestreply(댓글순), age(연령별), empathy(실시간공감) 
#   랭킹 종류는 하나씩 클릭해 본다.
#  - 여기선 popular로 한다.
# 상단의 날짜를 움직이면 날짜별 뉴스 랭킹 목록을 볼수 있다.
# 날짜별 url: https://media.daum.net/ranking/popular/?regDate=20191024

#--------------페이지 분석-------------#
# ul.list_news2 > li 가 각 뉴스들이다. 
# 하위에 <a>가 있고 <div class=cont_thumb> 가 있는데 <a>는 사진이고 div가 뉴스제목과 줄임내용이다. (사진이 먼저나옴)
# 뉴스 상세 링크와 제목:   div.cont_thumb > strong.tit_thumb > a
# 신문사                   :   div.cont_thumb > strong.tit_thumb > span.info_news
# 줄임 내용:                  div.cont_thumb  > div.desc_thumb

# 1. ul.list_news2 > li > div.cont_thumb 를 select로 조회 (div.cont_thumb)내에 제목, 링크, 줄임내용 있으므로.
# 2. 반복문을 돌리면서 각 내용을 가져온다.
import pandas as pd 
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime #모듈:datetime, class:datetime
url = 'https://media.daum.net/ranking/popular/'


res = requests.get(url)
if res.status_code == 200:
    soup = BeautifulSoup(res.text, 'lxml')
    news_list = soup.select('ul.list_news2 > li > div.cont_thumb')
    # print(len(news_list))
    # print(news_list[0])
    content_list = [] # (링크, 제목, 신문사, 요약))
    for div in news_list:
        link = div.select_one('strong.tit_thumb > a').get('href').strip()
        title = div.select_one('strong.tit_thumb > a').text.strip()
        newspaper = div.select_one('strong.tit_thumb > span.info_news').text.strip()
        summary = div.select_one('div.desc_thumb').text.strip()
        content_list.append([link, title, newspaper, summary])
        # csv 파일로 쓰기
    curr_date = datetime.now().strftime('%Y-%m-%d')
    df = pd.DataFrame(content_list, columns=['링크','제목','신문사','기사요약'])
    df.to_csv('news_list_{}.csv'.format(curr_date), index=False)
    # with open('news_list_{}.csv'.format(curr_date), 'wt', encoding='UTF-8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerows(content_list)

