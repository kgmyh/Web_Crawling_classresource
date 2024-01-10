from selenium.webdriver import Chrome

driver = Chrome()
url = 'http://www.youtube.com'
driver.get(url)

driver.execute_script('window.scrollTo(0,10000)')
a = driver.execute_script('return document.title')
height = driver.execute_script('return document.body.scrollHeight')
print(height)