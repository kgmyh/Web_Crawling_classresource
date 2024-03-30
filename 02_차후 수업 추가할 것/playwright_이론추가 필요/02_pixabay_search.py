import re
import time

from playwright.sync_api import sync_playwright


# pixabay keyword로 조회한 뒤 마지막 페이지 번호 조회 후 마지막 페이지 까지 클릭하여 이동하기
def main(keyword='사진'):

    with sync_playwright() as p:
        
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(f"https://pixabay.com/ko/images/search/{keyword}/")
        # page.wait_for_timeout(1000)
        #keyword 결과의 마지막페이지 번호 조회
        last_page_elem = page.query_selector('#paginator_clone > div > form')
        # print(last_page_elem)
        last_pagenum = re.sub('[ /]+', '', last_page_elem.inner_text())
        print(int(last_pagenum))
        current_page = 0
        for i in range(int(last_pagenum)):
            print(current_page+1, "page")
            # next button
            next_btn = page.wait_for_selector('#content > div > a', timeout=3000)
            next_btn.click()  
            current_page += 1
          
        
        # page.wait_for_timeout(3000)
# #

if __name__ == '__main__':
    main("tiger")