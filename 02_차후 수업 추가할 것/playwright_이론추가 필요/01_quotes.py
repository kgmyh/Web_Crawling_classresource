################################################### 
# 설치 : pip install playwright
# 웹브라우져 다운: playwright  install 
#    webkit(사파리), chrome, firefox 지원 => playwright에서 사용할 browser 다운로드
################################################### 
# 동기 api
from playwright.sync_api import sync_playwright   # 컨택스트 매니져 생성 함수


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # browser 실행  #with절 나가면 close() => 브라우져 종료
        page = browser.new_page() # 페이지 객체 생성
        page.goto("https://quotes.toscrape.com/")  #이동
        # query_selector() 1개 조회, query_selector_all() 다수 조회
        title_elm = page.query_selector('body > div > div.row.header-box > div.col-md-8 > h1 > a')  #selector로 조회: css selector/xpath 둘다 사용가능. 
        print(type(title_elm), title_elm.inner_text())
        login = page.query_selector('body > div > div.row.header-box > div.col-md-4 > p > a')
        login.click() # 버튼 클릭
        user_input = page.query_selector('[id="username"]')
        user_input.type('username')
        password_input = page.query_selector('[id="password"]')
        password_input.type('password')

        submit_btn = page.query_selector('[type="submit"]')
        submit_btn.click()


        logout_btn = page.query_selector('[href="/logout"]')
        print(logout_btn.inner_text())
        logout_btn.click()
        page.wait_for_timeout(3000)  # 3초 기다린다.
        
    
if __name__ == '__main__':
    main()
