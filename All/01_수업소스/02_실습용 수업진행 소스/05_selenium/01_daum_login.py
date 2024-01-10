from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

driver = Chrome() #맥은 경로 지정해야함.
with open('pwd.txt') as f:
    pwd = f.readline()

url = 'https://logins.daum.net/accounts/signinform.do'
driver.get(url) 

time.sleep(1)
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "inputPwd")))
id_input = driver.find_element_by_id('id')
pwd_input = driver.find_element_by_id('inputPwd')
login_btn = driver.find_element_by_id('loginBtn')

id_input.send_keys('kgmyh')
pwd_input.send_keys(pwd)
login_btn.click()

# 또는 다음과 같이 처리
# import time 

# 여기서 잠깐 멈춰야 한다. 로그인후 메인 페이지가 나오기 전에 아래가 실행되면서 간격이 생기는 듯하다.
time.sleep(1)


mail_url = 'https://mail.daum.net'
driver.get(mail_url)
# WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#mailList ul a.link_subject"))) 
time.sleep(1)
#크롤링할 링크


html_doc = driver.page_source
print(html_doc[:100])
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc)

a_titles = soup.select('div#mailList ul a.link_subject')
for num, a_tag in enumerate(a_titles):
    print(num, a_tag.get_text().strip(), sep='-')

driver.close()