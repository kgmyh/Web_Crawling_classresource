## 미완성

import os
import requests
from dotenv import load_dotenv


def crawling_without_login():
    webtoon_url = "https://comic.naver.com/api/article/list?titleId=818791&page=1"
    response = requests.get(webtoon_url)
    print(response.status_code)
    data = response.json()
    print(data)

def crawling_with_login():

    load_dotenv()
    id = os.getenv("ID")
    pw = os.getenv("PASSWORD")

    login_url = "https://nid.naver.com/nidlogin.login"

    session = requests.session()
    login_res = session.post(login_url, data={"id": id, "pw": pw})
    print(login_res.status_code)
    if login_res.status_code == 200:
        # 19금 웹툰 중 일부 정보는 로그인 해야만 조회가 된다. 로그인 안된 상태에서는 401 에러 발생.
        ## 
        webtoon_url = "https://comic.naver.com/api/article/list?titleId=818791&page=1"
        session.headers.update({"referer": "https://comic.naver.com/webtoon/list?titleId=818791&tab=sat"})
        response = session.get(webtoon_url)
        print(response.status_code)
        data = response.json()
        print(data)
    else:
        print("로그인 실패")

if __name__ == "__main__":
    # crawling_without_login()
    crawling_with_login()   # 일단 안되네..