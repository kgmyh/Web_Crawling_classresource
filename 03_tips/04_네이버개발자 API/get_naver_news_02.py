# %load get_naver_news_02.py
# paging을 이용해 조회

# 요청파라미터
#  - start : 시작기사 (1 ~ 1000 까지 가능)
#  - display: 한번에 가져올 검색 개수 (1 ~ 100 까지 가능)
import requests
import time
from datetime import datetime
import pickle  #이번엔 피클로 저장

# 01 복습 및 start display를 이용해 여러개 가져오기
with open('./account.txt') as f:
    client_id = f.readline().strip()
    client_secret = f.readline().strip()

#요청파라미터
#start: 검색 시작 위치로 최대 1000까지 가능
#display: 1 ~100
def get_news(keyword, start=1, display=100):
    """뉴스 검색 함수
    
    Arguments:
        keyword {str} -- [검색할 검색어]
    
    Keyword Arguments:
        start {int} -- [가져올 뉴스의 시작 번째, 1 ~ 1000] (default: {1})
        display {int} -- [한번에 가져올 개수. 1 ~ 100] (default: {100})
    """
    url = "https://openapi.naver.com/v1/search/news.json"
    headers = {
        "X-Naver-Client-Id":'gcGsZyq_7t0yY5z9NLLw',
        "X-Naver-Client-Secret":'bgFjG8GN7G'
    }
    news_link_list = [] #뉴스 링크들을 저장할 리스트
    # 1000까지 가능하므로
    while start <= 1000: 
        params = {
            'query':keyword,
            'start':start,
            'display':display 
        }
        res = requests.get(url, headers=headers, params=params)

        if(res.status_code==200):
            result = res.json()
            items = result['items']

            for item in items:
                link = item['link']
                if 'news.naver.com' in link:
                    news_link_list.append(link)
            # print(start)        
            start = start + display #start값 증가해서 다음 100개 가져오기 

            # 초당 10번 호출만 가능. 그래서 시간간격을 약간준다.
            time.sleep(0.1) 
        else:
            print("Error Code:%d" % res.status_code)
            print(res.text)
            raise Exception(res.text)

    # 파일로 저장 - pickle이용.
    filename = '{}_news_list_{}.pkl'.format(keyword, datetime.now().strftime('%Y-%m-%d-%H'))
    print(filename)
    with open(filename, 'wb') as f:
        pickle.dump(news_link_list, f)   
if __name__ == '__main__':
    get_news('인공지능')
