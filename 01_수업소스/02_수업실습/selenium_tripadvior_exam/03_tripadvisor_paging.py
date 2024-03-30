import time

from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup 

url = 'https://www.tripadvisor.co.kr/Restaurant_Review-g294197-d3200324-Reviews-Jungsik-Seoul.html'
driver = Chrome()
driver.get(url)

wait = WebDriverWait(driver, 10)
next_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.nav.next.taLnk.ui_button.primary')))
# print(next_btn.text)
next_btn.click()



