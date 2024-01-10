# pixabay 첫 페이지의 링크 이미지들을 다운로드 한다.
from pathlib import Path
import time

import selenium
import webdriver_manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

print("selenium version:", selenium.__version__)
print("webdriver_manager version:", webdriver_manager.__version__)
# selenium version: 4.7.2
# webdriver_manager version: 3.8.5


root_path = Path('./image_path')

def make_save_dir(subdir:str)->Path:
    """
    이미지를 저장할 디렉토리를 생성
    root_path에 매개변수로 받은 경로를 생성한다.

    Args:
        subdir (str): 생성할 이미지 저장 디렉토리
    Returns:
        Path: 생성한 디렉토리 
    """
    path = root_path / subdir
    path.mkdir(exist_ok=True)
    return path

def get_driver(headless:bool=False)->WebDriver:
    """
    Chrome WebDriver를 생성해서 반환한다.

    Args:
        headless (bool, optional): headless 여부. True: headless, False: non-headless. Defaults to False.

    Returns:
        WebDriver: Chrome Webdriver
    """
    options = None
    if headless:
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
    
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver



def image_download(driver:WebDriver, keyword:str, path: Path)->None:
    """전달받은 키워드로 pixabay.com에서 조회한 결과 이미지를 다운받는다.

    Args:
        driver(WebDriver): WebDriver
        keyword (str): 다운받을 이미지 검색 키워드
        path(Path): 이미지를 저장할 경로
    """
    url = f'https://pixabay.com/images/search/{keyword}'
    driver.get(url)
    # 페이지를 맨 아래로 이동시킨다. (감춰진 image는 black 이미지로 초기화 되어있고 스크롤을 내려 나오면 그때 실제 이미지로 src가 변경된다.)
    # 이건 무한스크롤 할 필요없이 `end` 키를 누른다. (페이지는 다 떠있는 상태에서 맨 아래로 이동하면된다.)
    # end key 타이핑 => body 요소에 send_key()로 
    body_elem = driver.find_element(By.TAG_NAME, "body")
    body_elem.send_keys(Keys.END)
    time.sleep(1)  #스크립트가 실행되어 이미지가 생성되도록 기다려야 한다.
    # 이미지 태그들 조회
    img_elem_list = driver.find_elements(By.CSS_SELECTOR, "div.row-masonry.search-results .item > a > img")
    for img_elem in img_elem_list:
        src = img_elem.get_attribute('src')
        fname = src.split('/')[-1]
        import requests
        response = requests.get(src)
        print(response.status_code)
        if response.status_code == 200:
            with open(path / fname, 'wb') as f:
                f.write(response.content)#binary는 content로 읽는다.

if __name__ == '__main__':
    keyword = input("Keyword:")
    try:
        save_path = make_save_dir(keyword)
        driver = get_driver()
        driver.maximize_window()
        driver.implicitly_wait(5) #암시적 대기 설정
      
        image_download(driver, keyword, save_path)
        
    except Exception as e:
        print(e)
    driver.close()
