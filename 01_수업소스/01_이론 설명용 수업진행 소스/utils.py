# driver 생성 함수
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


def get_driver(headless=False):
    # Create Chromeoptions instance
    options = webdriver.ChromeOptions()

    # Adding argument to disable the AutomationControlled flag ==> navigator.webdriver = False (개발자 도구 콘솔에서 확인) => 테스트도구가 아니라고 속인다.
    options.add_argument("--disable-blink-features=AutomationControlled")

    if headless:
        options.add_argument("--headless")
    driver = ChromeDriverManager().install()
    service = Service(executable_path=driver)
    driver = webdriver.Chrome(service=service, options=options)
    return driver
