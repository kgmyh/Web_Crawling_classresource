import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# 웹 드라이버 서비스 설정
service = Service(ChromeDriverManager().install())

# 웹 드라이버 시작
driver = webdriver.Chrome(service=service)

# HTML 파일 열기
driver.get('file:///C:/Documents/★_kgmyh Repo/Web_Crawling_classresource/01_수업소스/03_ing/selenium_selectbox.html')

# <select> 요소 찾기
select_element = driver.find_element(By.ID, 'select_car')

# Select 객체 생성
select = Select(select_element)

time.sleep(1) # 확인하기 위해 2초 대기

# 옵션 변경 (예: 'volvo' 선택)
select.select_by_value('MERCEDES_C_CLASS') # value로 선택
# 옵션 변경 (예: 인덱스로 선택, 첫 번째 옵션 선택)
time.sleep(1)
select.select_by_index(3)
time.sleep(1)

# 선택된 옵션의 텍스트 조회
selected_option = select.first_selected_option
print("Selected option text:", selected_option.text)

# 웹 드라이버 종료
driver.quit()