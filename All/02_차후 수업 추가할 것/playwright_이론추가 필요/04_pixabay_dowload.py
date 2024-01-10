import os
import random
import re
from pathlib import Path
from pprint import pprint

import requests

from playwright.sync_api import sync_playwright


def search_keyword(page, keyword='image'):
    """
    키워드로 목록페이지 조회후 조회된 이미지의 상세페이지 경로를 추출해서 파일로 저장
    """
    # 검색결과 페이지로 이동
    url = f"https://pixabay.com/ko/images/search/{keyword}/"
    print(url)
    page.goto(url)
    page.wait_for_load_state()   # headless일때는 기다리는 코드를 꼭 넣어준다. => default: load

    # 마지막 페이지번호 조회 => 몇페이지까지 다음버튼을 누를지 알아야 하므로
    try:
        last_page_elem = page.wait_for_selector('#paginator_clone > div > form', timeout=3000)  # 링크 있는 <form>을 가져온다. 
        next_btn_click_count = int(re.sub('[ /]+', '', last_page_elem.inner_text()))  # 현재 1page이므로 다음페이지 클릭은 마지막 페이지 번호 -1 만큼만 하면된다.
    except:
        next_btn_click_count = 1  # 검색결과가 1페이지 인 경우 찾는 것이 없다.(경회루로 조회) 
    detail_page_url_list = []
    current_page = 1

    for i in range(next_btn_click_count):
        anchor_tag_list = page.query_selector_all("div.row-masonry.search-results .item > a")
        for anchor in anchor_tag_list:
            href = f"https://pixabay.com{anchor.get_attribute('href')}\n"
            detail_page_url_list.append(href)

        print(f'Logger: {current_page} 상세페이지 링크 조회완료')
        # 다음버튼 클릭
        
        if current_page == next_btn_click_count:  # 처리한 페이지가 마지막 페이지 이면 break.
            break
        # 다음페이지로 이동 
        # 현재페이지번호를 1 증가 시키고 다음페이지 버튼 클릭
        current_page += 1 
        next_btn = page.wait_for_selector('#content > div > a', timeout=3000)
        next_btn.click()  
        

    # 리스트의 내용 파일로 저장
    fname = f"{keyword}_detail_page.txt"
    print("총 저장한 상세페이지 링크개수:",len(detail_page_url_list))
    with open(fname, 'wt') as f:
        f.writelines(detail_page_url_list)

    return fname





def search_image_url(detail_page_file_path, save_dir, page):
    """
    이미지 상세페이지에서 이미지파일을 다운받을 수 있는 이미지 경로를 조회해서 파일로 저장
    """
    with open(detail_page_file_path, 'rt') as fr:
        detail_page_url_list = fr.readlines()
        print("detailpage 링크 개수:", len(detail_page_url_list))
    
    image_link_list = []
    for url in detail_page_url_list:
        try:
            page.goto(url)
            page.wait_for_load_state()
            
            img_elem = page.wait_for_selector('#media_container > picture > img', timeout=10000)
            src = img_elem.get_attribute('src')  # <image src 속성 조회>

            # src 이미지 다운로드
            ## 파일명
            save_file_name = src.split('/')[-1]
            ## 저장경로
            path = os.path.join(save_dir, save_file_name)
            ## request 요청
            response = requests.get(src, stream=True)
            if response.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in response:
                        f.write(chunk)
            else:
                print("Error - Download Faile, status code: ", response.status_code)
            image_link_list.append(src+'\n')
        except:
            print(f"search_image_url(): {url} 처리도중 오류 발생")

    fname = detail_page_file_path.split('_')[0]+"_image_url.txt"
    with open(fname, 'wt') as f:
        f.writelines(image_link_list)


# def download_images(image_url_filepath, save_dir_path):
#     """
#     이미지들을 다운받는다. ==> 403 (따로 하니 403 권한 문제 발생.)
#     """
#     with open(image_url_filepath, 'rt') as f:
#         url_list = f.readlines()

#     for url in url_list:
#         save_file_name = url.split('/')[-1]
#         path = os.path.join(save_dir_path, save_file_name)
#         response = requests.get(url, stream=True)
#         if response.status_code == 200:
#             with open(path, 'wb') as f:
#                 for chunk in response:
#                     f.write(chunk)
#         else:
#             print("Error: download fail - request status code:", response.status_code)

def run():
    # 이미지 저장할 root 경로
    home_path = Path(__file__).parent
    save_root_path = home_path / 'image_path'
    if not save_root_path.is_dir():
        save_root_path.mkdir()

    import pyautogui
    # keyword = input("Image Keyword:")
    keyword = pyautogui.prompt("다운받을 이미지 키워드")

    # 키워드별로 저장할 디렉토리.
    save_dir = save_root_path / keyword
    if not save_dir.is_dir():
        save_dir.mkdir()

    with sync_playwright() as p:
        # browser = p.chromium.launch(headless=True)   # True이면 왜 안되지? 음.. 
        
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()
        detail_pages_file = search_keyword(page, keyword)
        # print(detail_pages_file)
        image_file = search_image_url(detail_pages_file, save_dir, page)
        

if __name__ == '__main__':
    import time
    s = time.time()
    run()
    e = time.time()
    print('다운로드 걸린 시간:', (e-s))

# headless모드 걸린 시간       : 452.20351219177246
# 다운로드 걸린 시간(경회루-24): 43.919832944869995

# headless=False 모드 걸린 시간: 377.0280349254608
# 다운로드 걸린 시간(경복궁-260): 613.496134519577
# 다운로드 걸린 시간(경회루-24): 53.39862275123596


######
# headless=False로 해서 띄우면 되고 headless 모드로 접근하면 elements를 못찾는다. 
# stackoverflow 에서 찾은 것(https://stackoverflow.com/questions/71687642/playwright-headless-chromium-cant-find-selector-but-finds-it-in-ui-mode)
# 크롬을 다 끄고 하면 된다고 했는데 일단은 안되었다.
# 그래서 firefox로 바꾼뒤 하니 된다. 시간은 비슷하게 걸리는 것 같다.