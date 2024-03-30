#####################################################
#  다음 뉴스 목록 조회 + 개별 기사 내용 조회 
#####################################################
import os
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
import asyncio
import aiohttp

url = "https://news.daum.net"
######## selector
## 뉴스목록에서 `뉴스제목`, `링크주소` 를 조회.
# 뉴스목록 selector: 뉴스제목: a의 content, 링크주소: a의 href 속성
a_selector = "body > div.container-doc > main > section > div > div.content-article > div.box_g.box_news_issue > ul > li > div > div > strong > a"
# 뉴스 기사 상세 selector
article_selector = "#mArticle > div.news_view.fs_type1 > div.article_view > section > p"

# user-agent: 개발자도구>콘솔: navigator.userAgent, google: my user agent 검색
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'

def get_daum_news_list():
    """
    다음 뉴스 기사 목록을 크롤링하는 함수.
    news.daum.net의 기사 목록에서 "제목", "링크" 들을 수집.

    aguments
    return
        DataFrame: 조회결과들을 담은 DataFrame(표)
    raise
        Exception: 처리 실패시 발생
    """
    # 1. 요청
    res = requests.get(url, headers={"user-agent":user_agent})
    if res.status_code == 200:
        # 2. 응답 결과 html을 BS4 에 넣어서 instance 생성.
        soup = BeautifulSoup(res.text, "lxml")
        # 3. selector를 이용해서 조회
        a_list = soup.select(a_selector)
        # 4. 원하는 값들 추출 (title, link)
        result_list = []  # 조회결과를 담을 list
        for a_tag in a_list:
            title = a_tag.get_text() # 태그의 text내용
            link = a_tag.get("href")  # href 속성 값

            result_list.append([title.strip(), link])
        
        return result_list
    else:
        raise Exception(f"요청 실패. 응답코드: {res.status_code}")


async def get_news(url, session):
    """
    개별 뉴스기사 내용을 조회하는 코루틴.
    Argument:
        url: str - 뉴스기사를 가져올 daum news url
        session: ClientSession - aiohttp session 
    Return:
        str: 조회한 뉴스기사
    """
    async with session.get(url) as res:
        if res.status == 200:
            html = await res.text()
            soup = BeautifulSoup(html, "lxml")
            p_list = soup.select(article_selector)
            article = [] # 뉴스기사 문단들을 저장할 리스트
            for p in p_list:
                article.append(p.get_text())
            # 리스트 안에 문단들을 하나의 string으로 합치기
            # "구분자문자열".join(리스트)
            return '\n'.join(article)
                

async def main(links):
    """
    get_news 코루틴들을 개별 기사 url별로 생성해서 task로 실행.
    Argument:
        links: list - 크롤링할 기사들의 url들.
    Return:
        list: 크롤링한 전체 기사들.
    """
    async with aiohttp.ClientSession(headers={"user-agent":user_agent}) as session:
        result = await asyncio.gather(*[get_news(url, session) for url in links])
    
    return result

if __name__ == "__main__":
    # ROOT 경로 통일
    os.chdir(r'C:\Classes\DA-35\03_Web_crawling_rpa')
    base_dir = os.getcwd()
    ##### 저장할 디렉토리 생성
    save_dir = os.path.join(base_dir,"실습/daum_news_list")
    os.makedirs(save_dir, exist_ok=True)

    ##### 뉴스 기사 목록 조회
    news_list = get_daum_news_list()
    df = pd.DataFrame(news_list, columns=['제목', "링크주소"])
    links = df['링크주소']

    ##### 목록 기사들의 상세 뉴스내용 조회
    result = asyncio.run(main(links))
    df['기사내용'] = result  

    ##### 파일로 저장.
    d = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = f"{save_dir}/{d}.csv"
    # csv 파일로 저장.
    df.to_csv(file_path, index=False)
    print(">>>>>>>>>>>>>완료<<<<<<<<<<<<<")

    print(df.head())