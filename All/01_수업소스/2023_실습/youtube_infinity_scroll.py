import time
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
#from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


url = "https://www.youtube.com/?gl=KR&hl=ko"
service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get(url)


#option = webdriver.ChromeOptions()
#option.add_argument("--headless")

######## scroll 길이 조회는 현재 scroll이 표현하는 페이지의 전체 길이를 반환하는 것. 10000을 준다고 10000으로 가는게 아니라 추가된 페이지만큼. 10000은 맨 아래로 가기 위한것이다. (한번움직이는 코드에서)

### 무한스크롤
# ************** 크롬개발자도구에서 자바스크립트 코드를 먼저 실행해본다.
#  execute_script("자바스크립트 코드") : 자바스크립트 코드. JS 코드에서 return 하는 값을 매개변수로 받을 수 있다.
# Javascript 함수
#  - scrollTo(x, y) : 스크롤바의 위치를 이동시킨다. 상하는 y값만 좌우는 x값만 설정
#  - document.documentElement.scrollHeight: 스크롤패인의 높이를 반환. documentElement 대신 body를 하기도 한다. (크롬은 안됨)

# 현재 스크롤 높이 저장 변수
#body = driver.find_element(By.TAG_NAME, 'body')
scroll_pane_height = driver.execute_script('return document.documentElement.scrollHeight') # 이동 전 스크롤패인의 높이
# print(scroll_pane_height)
while True:
    # 스크롤바를 스크롤패인의 높이 만큼 이동시킨다.  ### 이거 대신 body 조회후 end 키를 입력 (body.send_keys(Keys.END)) 해도됨.
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight)')
    # body.send_keys(Keys.END) # 이거 보다 위의 것이 더 빠르게 이동한다. scrollHeight 만큼 늘어나므로.

    # 밑에 붙일 내용을 요청해서 화면을 만들때 까지 약간의 시간차를 둔다.
    time.sleep(0.5)
    new_scroll_pane_height = driver.execute_script('return document.documentElement.scrollHeight')
#     print(scroll_pane_height, new_scroll_pane_height)
    #이동전의 높이와 이동후 높이가 같으면 반복문을 빠져나온다.
    if scroll_pane_height == new_scroll_pane_height:
        break
    scroll_pane_height = new_scroll_pane_height