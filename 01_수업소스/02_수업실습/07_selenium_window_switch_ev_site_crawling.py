# 새창 다루기 옵션

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Chrome 옵션 설정
chrome_options = Options()
# chrome_options.add_argument("--start-maximized")  # 브라우저 최대화
# chrome_options.add_argument("--window-size=1920,1080")  # 윈도우 크기 설정
# chrome_options.add_argument("--headless")  # 브라우저를 헤드리스 모드로 실행
chrome_options.add_argument("--disable-gpu")  # GPU 사용 안 함. headless 모드일 때 필요
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 제어 기능 비활성화
# Chrome 드라이버 초기화 (webdriver-manager 사용)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # 지정된 URL로 이동
    driver.get("https://ev.or.kr/nportal/buySupprt/initSubsidyPaymentCheckAction.do")
    
    # 페이지 로딩 대기
    wait = WebDriverWait(driver, 10)  # 최대 10초 대기
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#btnLocalCarPrc")))

    # 버튼 클릭
    button.click()

    # 현재 윈도우(창) 핸들들 저장 (윈도우 핸들이란 윈도우(창)를 구분하는 식별자)
    original_window = driver.current_window_handle
    print(driver.window_handles)

    # 새 창이 열릴 때까지 대기
    # wait.until(EC.new_window_is_opened(driver.window_handles))
    time.sleep(1)
    # 새 창으로 전환
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            # 새 창에서 버튼 클릭
            buttons = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "body > form > div > table > tbody td.tr_car_btn > a")))

            result_dict = {}  #key: 지자차, value: [] - 차종별 지원 비용

            for button in buttons:
                button.click()
                # 새 창이 열릴 때까지 대기
                time.sleep(1)
                # 새 창으로 전환 (orig, 첫번째 창이 아니면.)
                new_window_handle = [handle for handle in driver.window_handles if handle != original_window and handle != window_handle][0]
                driver.switch_to.window(new_window_handle)

                # "body > form > div > h4" 태그의 텍스트 추출
                local_government = driver.find_element(By.CSS_SELECTOR, "body > form > div > h4").text

                # 테이블 요소 찾기
                table = driver.find_element(By.CSS_SELECTOR, "body > form > div > table")
                rows = table.find_elements(By.TAG_NAME, "tr")

                # 테이블 데이터를 저장할 딕셔너리 초기화
                table_data = []

                # 테이블의 각 행을 순회하며 데이터 추출
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    row_data = [cell.text for cell in cells]
                    table_data.append(row_data)

                result_dict[local_government] = table_data

                # 새 창 닫기
                driver.close()
                # 원래 창으로 전환
                driver.switch_to.window(window_handle)
                # break
            print(result_dict)

finally:
    # 드라이버 종료
    driver.quit()


