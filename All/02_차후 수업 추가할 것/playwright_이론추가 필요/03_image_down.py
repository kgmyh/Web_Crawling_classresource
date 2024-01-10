import os

import requests

from playwright.sync_api import sync_playwright


# 픽사베이 이미지 페이지(리스트에서 클릭하고 들어간 페이지)에서 이미지 다운받아 저장
# playwrigth에서는 image의 src 속성값을 조회하고 다운은 requests로 한다.
def main(save_dir):

    with sync_playwright() as p:

        chrome = p.chromium.launch(headless=False)
        page = chrome.new_page()
        page.goto('https://pixabay.com/ko/photos/%ea%b0%80%ec%9d%b4%ec%95%84-%ec%a3%bc-%eb%82%98%ec%84%a0%ed%98%95-%ea%b3%84%eb%8b%a8-7844381/')

       
        page.wait_for_timeout(1000)
        img = page.query_selector('#media_container > picture > img')
        print(type(img))
        src = img.get_attribute('src')
        print(src.split('/')[-1])
        save_file_name = src.split('/')[-1]
        path = os.path.join(save_dir, save_file_name)
        response = requests.get(src, stream=True)
        if response.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in response:
                    f.write(chunk)

if __name__ == "__main__":
    img_path = 'img_path'
    os.makedirs(img_path, exist_ok=True)
    main(img_path)        