# 03에서 만든 리스트(csv) 를 가지고 목록의 뉴스를 내용을 크롤링 한다.

import os
import requests
from urllib import parse
from bs4 import BeautifulSoup
import pickle as pkl
import pandas as pd 
from datetime import datetime

def save_news_links(type='popular'):
    """리스트 페이지에서 각 뉴스의 링크를 크롤링해서 List로 저장)
    파일명은 news_link_실행날짜.plk
    Keyword Arguments:
        type {str} -- [랭킹 종류] (default: {'popular(많이본순)'}, kkomkkom(열독률), bestreply(댓글순), age(연령별), empathy(실시간공감) )

    Return value: 
        None
    """

    # 뉴스 랭킹에 type을 붙여 url을 만든다.
    base_url = 'https://media.daum.net/ranking/'  #주의 '/' 로 안끝나면 자원으로 보고 join시 뺀다 (ranking 으로 끝나면 ranking은 빠진다. )
    url = parse.urljoin(base_url, type)
    
    # 목록 저장할 디렉토리 만들기
    path = './news_lists'
    if not os.path.isdir(path):
        os.mkdir(path) #있으면 만들지 말고 없으면 만들어라. (있다고 에러내지 말아라.)
    
    res = requests.get(url)
    
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')
        news_list = soup.select('ul.list_news2 > li > div.cont_thumb')
        
        news_links = [] #링크를 저장할 리스트
        for div in news_list:
            link = div.select_one('strong.tit_thumb > a').get('href').strip()
            
            news_links.append(link)
        
        print(len(news_links))
        print(news_links[:2])
        # 리스트를 pickle로 저장 (파일명: news_links_실행일.pkl)
        curr_date = datetime.now().strftime('%Y-%m-%d')
        with open('./news_lists/news_links_%s.pkl' % curr_date, 'wb') as f:
            pkl.dump(news_links, f)
    else:
        raise Exception("오류: "+res.status_code)

# Guide: 02_GetDaumNews.py 의 카피 (숫자로 시작해서 import 가 안된다. 흠 _ 붙일까?) - 수업중엔 만들게.
def get_daum_news(url):
    '''다음 뉴스 news_code 받아 뉴스의 작성일, 수정일, 작성기자, 제목, 내용을 반환
    매개변수
        url: str 뉴스 url
    반환값
        tuple: (제목, 기자이름, 작성일시,수정일시, 내용))
    '''     
    
    res = requests.get(url)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, 'lxml')

            # 가져오기
        title_tag = soup.select_one('h3.tit_view')
        info1_tag = soup.select_one('span.info_view > span.txt_info:nth-child(1)')
        info2_tag = soup.select_one('span.info_view > span.txt_info:nth-child(2)')
        info3_tag = soup.select_one('span.info_view > span.txt_info:nth-child(3)')
        news_tag = soup.select_one('div.news_view')

        title = title_tag.text.strip() if title_tag else None
        news = news_tag.text.strip() if news_tag else None
        reporter= None
        write_date=None
        modify_date = None
        
        # info1이 기자명 또는 입력일 인 경우가 있다.
        # 그래서 info1,2,3 다있으면 기자명,입력일,수정일 다 넣고 둘만 있으면 기자명, 입력일, 하나만 있으면 입력으로 시작하면 입력일 아니면 기자명을 설정
        if info1_tag and info2_tag and info3_tag:
            reporter = info1_tag.text.strip()
            write_date = info2_tag.text.strip() 
            modify_date = info3_tag.text.strip()
        elif info1_tag and info2_tag and info3_tag==None:
            reporter = info1_tag.text.strip()
            write_date = info2_tag.text.strip()
        elif info1_tag and info2_tag==None and info3_tag==None:
            if info1_tag.text.startswith("입력"):
                write_date = info1_tag.text.strip()
            else:
                reporter = info1_tag.text.strip()
                    
        return (title, reporter, write_date, modify_date, news)
    else:
        raise Exception("요청 결과를 가져오지 못함. %d" % res.status_code)

def get_news(new_link_file):
    # 뉴스를 저장할 경로
    path = './news_lists/news/'
    if not os.path.isdir(path):
        os.makedirs(path)
    
    # pickle에서 읽어온 뉴스 링크를 저장할 경로
    news_links = None
    # 링크 리스트 읽어오기 - TODO: 나중에 다돌리는 것으로 개선
    with open(new_link_file, 'rb') as f:
        news_links = pkl.load(f)
    
    news_list = []
    for link in news_links:
        # 튜플로 반환된 뉴스 정보 리스트에 저장
        news_list.append(get_daum_news(link))
    df = pd.DataFrame(news_list, columns=['제목', '기자이름', '작성일시','수정일시', '내용'])
    curr = datetime.now().strftime('%Y-%m-%d')
    df.to_csv('%s/news_contents-%s.csv' % (path, curr), index=False)

def get_all_newslist():
    """pkl로 저장된 모든 파일의 파일 경로를 읽어서 dataframe으로 반환
    """
    link_path = './news_lists'
    # pkl 파일만 조회 - ./news_list에서
    file_list = [pkl_file for pkl_file in os.listdir(link_path) if os.path.isfile(os.path.join(link_path,pkl_file)) and pkl_file.endswith('.pkl')]
    news_links = []
    for file_name in file_list:
        r_path = os.path.join(link_path, file_name)
        with open(r_path, 'rb') as f:
            news_links.extend(pkl.load(f))

    # 링크중 중복된 것 있으면 제거 (set으로 변환)
    news_links = set(news_links)
    news_list = []
    news_path = link_path+"/news/"
    for link in news_links:
        # 튜플로 반환된 뉴스 정보 리스트에 저장
        news_list.append(get_daum_news(link))
    df = pd.DataFrame(news_list, columns=['제목', '기자이름', '작성일시','수정일시', '내용'])
    curr = datetime.now().strftime('%Y-%m-%d')
    df.to_csv('%s/news_contents-%s.csv' % (news_path, curr), index=False)
    

if __name__ == '__main__':
    # save_news_links()
    # get_news('./news_lists/news_links_2019-10-26.pkl')
    get_all_newslist()