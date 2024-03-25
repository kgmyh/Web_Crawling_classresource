
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://news.daum.net"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'

def get_news_list():
    """
    daum 뉴스 목록 조회
    조회결과는 pandas의 DataFrame(표) 로 만들어서 반환.
    """
    # 요청
    response = requests.get(url, headers={'User-Agent':user_agent})
    # 상태코드가 200 인지 확인.
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        tag_list = soup.select("ul.list_newsissue > li strong > a")
        print(len(tag_list))
        link_list = []
        title_list = []
        for tag in tag_list:
            link_list.append(tag.get("href"))
            title_list.append(tag.get_text().strip())
            
        return pd.DataFrame({
            "title":title_list,
            "link":link_list
        })
    else:
        print("문제발생:", response.status_code)
        
if __name__ == "__main__":
    from datetime import datetime 
    d = datetime.now().strftime("%Y-%m-%d")  # strftime(): 날짜시간을 원하는 형태의 문자열로 변환.
    file_path = f"daum_new_list_{d}.csv"
    print(file_path)
    result = get_news_list()
    # # csv 파일로 저장
    result.to_csv(file_path, index=False) #utf-8 형식으로 저장.
