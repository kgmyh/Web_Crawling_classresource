import time

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 

# 댓글 많은 식당을 선택한다.
url = 'https://www.tripadvisor.co.kr/Restaurant_Review-g294197-d3200324-Reviews-Jungsik-Seoul.html'

#options는 headless일때. 아니면 크기 조절은 set_window_size()로 한다.
options = ChromeOptions()
# options.add_argument('headless') #화면 나오지 않게
# options.add_argument('window-size=1920x1080')
# driver = Chrome(options=options)

driver = Chrome()
driver.set_window_size(width=1920, height=1080)
print(driver.get_window_size())

print(driver.get_window_size())
driver.implicitly_wait(3)
driver.get(url)

wc = WebDriverWait(driver, 10)
more_link = wc.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'span.ulBlueLinks'))
    )
more_link[0].click()

#클릭 완료를 기다린다.
time.sleep(0.5)

page = driver.page_source
# driver.quit()

soup = BeautifulSoup(page, 'lxml')
comment_tag_list = soup.select('p.partial_entry')
comment_list = []
for tag in comment_tag_list:
    comment_list.append(tag.get_text())

print(comment_list)
driver.close()
# 읽은 리뷰 CSV 파일에 저장.     
#import pandas as pd
#df = pd.DataFrame({'text':comment_list}).to_csv("리뷰.csv", index=False,encoding='UTF-8')
