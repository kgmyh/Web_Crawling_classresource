# 무한 스크롤 처리
from selenium.webdriver import Chrome
import time

url = "https://www.youtube.com/?gl=KR&hl=ko"
driver = Chrome()
driver.get(url)

### 무한스크롤
#  execute_script("자바스크립트 코드") : 자바스크립트 코드. JS 코드에서 return 하는 값을 매개변수로 받을 수 있다.
# Javascript 함수
#  - scrollTo(x, y) : 스크롤바의 위치를 이동시킨다. 상하는 y값만 좌우는 x값만 설정
#  - document.documentElement.scrollHeight: 스크롤패인의 높이를 반환. documentElement 대신 body를 하기도 한다. (크롬은 안됨)

# 현재 스크롤 높이 저장 변수

scrollpane_height = driver.execute_script('return document.documentElement.scrollHeight') # 이동 전 스크롤패인의 높이
print(scrollpane_height)
while True:
    # 스크롤의  스크롤패인의 높이만큼 이동시킨다. (내려간다)
    driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight)')
    # 내려가는 동안 약간의 간격을 줘 기다리게 한다.
    time.sleep(1)
    new_scrollpane_heigh = driver.execute_script('return document.documentElement.scrollHeight') # 이동후 현재 스크롤패인의 높이
    print(new_scrollpane_heigh)
    if scrollpane_height == new_scrollpane_heigh:
        # 스크롤바의 이동이 없었던 것이므로 반복문을 빠져나온다.
        break
    scrollpane_height = new_scrollpane_heigh

