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
    
async def get_news_data(url, session):
    
    async with session.get(url) as res: #요청 및 응답 with 문 빠져 나오면 연결 끊는다.
        txt = await res.text() #IO 작업이므로
        soup = BeautifulSoup(txt, 'lxml')
        p_list = soup.select('.news_view .article_view p')  #  p 태그에 문단별로 들어가 있다. text만 가져올 것이므로 p선택
        news = []
        for p in p_list:
            news.append(p.get_text())
        news = ' '.join(news)
    return news+"\n\n"

async def get_news_detail(df):
    """뉴스 상세 링크 DataFrame을 받는다."""
    # 아직 실행된 것이 아니라, 실행할 것을 계획하는 단계
    async with aiohttp.ClientSession() as session: 
        tasks = [get_news_data(url, session) for url in df["link"]]
        results = await asyncio.gather(*tasks)
    return results

if __name__ == '__main__':
    df = get_news_list()
    # print(df)
    results = asyncio.run(get_news_detail(df))
    with open('news.txt', 'w', encoding='utf-8') as f:
        f.writelines(results)
        