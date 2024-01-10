import requests
from bs4 import BeautifulSoup
import pandas as pd
import asyncio
import aiohttp


def get_news_list():
    """requests를 이용해 조회"""
    url = 'https://media.daum.net/'
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text)
        li_list = soup.select('.list_newsissue > li')
        # li 들을 목록으로 조회한 뒤 반복문 돌리면서 link 와 내용가져오기
        # 내용
        title_list = []
        # 링크
        link_list = []

        # 순위 빼는 것 아래 GUIDE 확인
        for li in li_list:
        #     print(li)
            a_tag = li.select_one('.cont_thumb > strong > a')
            link_list.append(a_tag.get('href'))
            txt = a_tag.get_text().strip()
            title_list.append(txt)
            
        
        return pd.DataFrame({'title':title_list, 'link':link_list})
    
def get_news_data(url):
    
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        p_list = soup.select('.news_view .article_view p')  #  p 태그에 문단별로 들어가 있다. text만 가져올 것이므로 p선택
        news = []
        for p in p_list:
            news.append(p.get_text())
        news =''.join(news)
    return news
    # async with session.get(url) as res: #요청 및 응답 with 문 빠져 나오면 연결 끊는다.
    #     txt = await res.text() #IO 작업이므로
    #     soup = BeautifulSoup(txt, 'lxml')
    #     p_list = soup.select('.news_view .article_view p')  #  p 태그에 문단별로 들어가 있다. text만 가져올 것이므로 p선택
    #     news = []
    #     for p in p_list:
    #         news.append(p.get_text())
    #     news = ' '.join(news)
    # return news+"\n\n"

def get_news_detail(df):
    """뉴스 상세 링크 DataFrame을 받는다."""
    # 아직 실행된 것이 아니라, 실행할 것을 계획하는 단계
    # 날짜를 받아서 조호하는 것으로 수업에는 진행.
    result = [get_news_data(url) for url in df["link"]]
    return result

if __name__ == '__main__':
    import time 
    start = time.time()
    df = get_news_list()
    print(df)
    results = get_news_detail(df)
    end = time.time()
    print("---------걸린시간:",end-start)
    print(results)
    # with open('news.txt', 'w', encoding='utf-8') as f:
    #     f.writelines(results)
        