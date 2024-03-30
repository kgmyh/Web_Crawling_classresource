# 셀레늄 우회
# https://pythondocs.net/selenium/%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81-%EB%B4%87-%ED%83%90%EC%A7%80-%EC%9A%B0%ED%9A%8C/#google_vignette

# 옐프(Yelp)는 미국 여행 필수 앱으로, 미국 내외의 맛집, 로컬 서비스, 관광지 정보를 제공한다. 중국의 Dianping과 유사하며, 사용자 리뷰와 평점이 많아 도움이 되며, 현재 시간과 위치에 기반한 영업 중인 곳을 손쉽게 찾을 수 있다. 주소, 전화번호, 가격대 등 필요한 모든 정보를 한눈에 볼 수 있는 실용적인 앱이다.

# https://www.yelp.com/biz/in-n-out-burger-san-francisco?osq=in+n+out
# 댓글 조회


# 댓글 selector: #reviews > section > div.css-1qn0b6x > ul > li > div > div > p > span
# 별점 selector: #reviews > section > div.css-1qn0b6x > ul > li > div > div> div > div:nth-child(1) > span > div 의 aria-label  속성.

import time
from bs4 import BeautifulSoup

from webdriver_manager.chrome import ChromeDriverManager

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

url = "https://www.yelp.com/biz/in-n-out-burger-san-francisco?osq=in+n+out"
# browser 생성 및 url 이동
service = Service(executable_path=ChromeDriverManager().install())
browser = webdriver.Chrome(service=service)
browser.get(url)

time.sleep(2)  # 뜰 때까지 시간이 걸림. 댓글은 처음 부터 뜨는 게 아니라 ajax처리 됨.

comment_elements = WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located(
        (
            By.CSS_SELECTOR,
            "#reviews > section > div.css-1qn0b6x > ul > li > div > div > p > span",
        )
    )
)


star_elements = WebDriverWait(browser, 10).until(
    EC.presence_of_all_elements_located(
        (
            By.CSS_SELECTOR,
            "#reviews > section > div.css-1qn0b6x > ul > li > div > div> div > div:nth-child(1) > span > div",
        )
    )
)
soup.select()

print(len(comment_elements), len(star_elements))

# time.sleep(3)
# browser.close()
