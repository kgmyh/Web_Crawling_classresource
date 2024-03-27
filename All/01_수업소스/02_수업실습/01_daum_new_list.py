# 실습\daum_new_list.py
## https://news.daum.net

# pip install requests beautifulsoup4
import requests
from bs4 import BeautifulSoup

## 뉴스목록에서 `뉴스제목`, `링크주소` 를 조회.
url = "https://news.daum.net"
# 뉴스제목: a의 content, 링크주소: a의 href 속성
a_selector = "body > div.container-doc > main > section > div > div.content-article > div.box_g.box_news_issue > ul > li > div > div > strong > a"
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

if __name__ == "__main__":
    result = get_daum_news_list()
    # print(len(result))
    # print(result[0])
    # 저장할 디렉토리를 생성
    import os
    from datetime import datetime
    import pandas as pd
    os.makedirs("daum_news_list", exist_ok=True)
    # 저장할 파일명 - 
    #      특정 주기마다 크롤링 수행할 경우 실행 날짜/시간을 이용해서 만들어 준다.
    d = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    file_path = f"daum_news_list/{d}.csv"
    # DataFrame 생성
    result_df = pd.DataFrame(result, columns=['제목', "링크주소"])
    # csv 파일로 저장.
    result_df.to_csv(file_path, index=False)






# csv 형식 저장
# Comma Separate Value
# 표를 text 파일에 작성.
# 행 (엔터)  열(,)
# 홍길동,20,인천
# 이순신,15,서울
# 강감찬,30,부산
    
# pandas 모듈(라이브러리)를 이용해 조회결과를 csv파일로 저장.
# 설치: pip install pandas
# control + `


