import time

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
# WaitWebDriver는 처음 로딩후에만 사용한다. 이미 있는 element에 내용만 들어가는 경우는 내용이 나올때 까지기다리지 않으므로 결국 time.sleep()을 사용해야 할 것 같다.
url = 'https://www.tripadvisor.co.kr/Restaurant_Review-g294197-d3200324-Reviews-or50-Jungsik-Seoul.html'

# options = ChromeOptions()
# options.add_argument('headless')
# options.add_argument('window-size=1920x1080')

# driver = Chrome(options=options)

url = 'https://www.tripadvisor.co.kr/Restaurant_Review-g294197-d3200324-Reviews-or50-Jungsik-Seoul.html'

options = ChromeOptions()

options = ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
options.add_argument("User-Agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")

options.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
options.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함

service = Service(executable_path=ChromeDriverManager().install()) 

driver = Chrome(service=service, options=options)
driver.get(url)
wait = WebDriverWait(driver, 10)

#마지막 페이지 번호 - div.pageNumbers > a:last-child
a_tag = wait.until(EC.presence_of_element_located([By.CSS_SELECTOR,'div.pageNumbers > a:last-child']))
print(a_tag.text)

last_page = int(a_tag.text.strip())
#댓글들을 저장할 리스트
comment_list = []
for i in range(last_page-1):
    
    # 더보기 링크 클릭
    attempt = 0
    while attempt != 3:  #최대시도횟수
        try:
            more_btn = wait.until(EC.presence_of_all_elements_located([By.CSS_SELECTOR, 'span.taLnk.ulBlueLinks']))
            more_btn[0].click()
            break  #클릭을 정상처리한 경우 더 시도 하지 않고 반복문 나온다.
        except:
            #클릭실패 - 잠시 기다렸다 다시 시도.
            time.sleep(0.5)
            print("더보기 클릭 시도 횟수:", attempt)
            attempt += 1
    
    # 댓글 조회
    time.sleep(1) #댓글 내용이 모두 나오길 기다린다.
    comment_tag_list = driver.find_elements_by_css_selector('p.partial_entry')
    for tag in comment_tag_list:
        comment_list.append(tag.text)  #댓글 텍스트 조회
    
    # 다음 버튼 클릭 : a.nav.next.taLnk.ui_button.primary
    next_btn = driver.find_element_by_css_selector('a.nav.next.taLnk.ui_button.primary')
    next_btn.click()
    
    print(i, end=' ')
    time.sleep(1) #다음 페이지로 이동할 때 까지의 기다린다.

#for문 종료
# driver.close()    


print(len(comment_list))
for i in range(10):
    print(comment_list[i])