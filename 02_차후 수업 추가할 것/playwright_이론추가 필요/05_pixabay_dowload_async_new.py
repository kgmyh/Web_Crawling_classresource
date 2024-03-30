import asyncio
import os
import random
import re
from pathlib import Path
from pprint import pprint

import aiohttp, aiofiles

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
################################ GUIDE #############################################
# aiohttp: https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp
#
####################################################################################
# 1. get_maxpagenum_of_keyword(keyword) : 키워드를 받아서 최대 페이지 번호를 읽어온다. => 동기처리
#      =====> 동기 처리하더라도 async_playwright 사용해야 한다. run()이 asyncio loop에서 돌므로.(playwright._impl._api_types.Error: It looks like you are using Playwright Sync API inside the asyncio loop.)
# 2. get_detail_page_url(): 조회페이지들의 조회결과의 detail page url을 조사한다. => 비동기적 처리
# 3. download_image(): detail 페이지에서 이미지 경로 조회후 다운로드 받는다. => 비동기적 처리


def test():
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page()
        page.goto(f"https://pixabay.com/ko/images/search/drone/")
        result  = page.locator(".photo-result-image")
        print(type(result), len(result.all()), type(result.all()), type(result.all()[0]))
        print(result.all()[0].get_attribute('src'))
        result2 = page.locator("#content > div > div:nth-child(1) > div > div.media_filter > span")
        for r in result2.all():
            print(r.inner_text())

        browser.close()


async def get_maxpagenum_of_keyword(url:str) -> int:
    async with async_playwright() as p:
        browser = await p.firefox.launch()
        page = await browser.new_page()
        await page.goto(url)
        try:
            last_page_elem = page.locator('span#paginator_clone .add_search_params')  # locator는 await 쓰지 않는다. 링크 있는 <form>을 가져온다. 
            next_btn_click_count: int = int(re.sub('[ /]+', '', await last_page_elem.inner_text()))
        except:
            next_btn_click_count = 1
        await browser.close()
        return next_btn_click_count
    

async def get_detail_page_urls(url:str)->list:
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        anchor_tags = page.locator("div.row-masonry.search-results .item > a")
        anchor_tag_list = await anchor_tags.all()
        result_list = []
        for anchor in anchor_tag_list:
            href = f"https://pixabay.com{await anchor.get_attribute('href')}"
            result_list.append(href)

        await browser.close()
        return result_list
    




async def download_image(img_url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as response:
            print("download status code:",response.status)
            if response.status == 200:
                return await response.read()
            else:
                return None
            
async def goto_detail_page_and_download_image(url:str, save_dir:Path):
    try:
        async with async_playwright() as p:
            browser = await p.firefox.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url)
            await page.wait_for_load_state(timeout=10000)
            img_elem = await page.query_selector('#media_container > picture > img')
            src = await img_elem.get_attribute('src')

            save_file_name = src.split('/')[-1]
            path = save_dir / save_file_name
            

            async with aiohttp.ClientSession() as session:
                async with session.get(src) as response:
                    print("download status code:",response.status)
                    if response.status == 200:
                        data = await response.read()
                        if data:
                            async with aiofiles.open(path, "wb") as f:
                                await f.write(data)
                        else:
                            print("\x1b[31m Error downloading image. \x1b[0m")
            
            await browser.close()
    except Exception as e:
        print("=======\x1b[31mError: Fail to download:", url,"\x1b[0m", e)

async def main():
    keyword = input("Keyword:")
    url = f"https://pixabay.com/ko/images/search/{keyword}/"
    max_page_num = await get_maxpagenum_of_keyword(url)
    print("main(): INFO - maxpagenum:",max_page_num)

    search_list_urls = [url+f"?pagi={num}" for num in range(1, max_page_num+1)]
    print(search_list_urls)

    tasks1 = [asyncio.create_task(get_detail_page_urls(url)) for url in search_list_urls]
    r = await asyncio.gather(*tasks1)

    results = []
    for result in r:
        results += result
    
    print("INFO: main - image 개수:", len(results))

    home_path = Path(__file__).parent
    save_root_path = home_path / 'image_path'
    if not save_root_path.is_dir():
        save_root_path.mkdir()

    save_dir = save_root_path / keyword
    if not save_dir.is_dir(): 
        save_dir.mkdir()

    save_dir = save_root_path / keyword
    print(save_dir)
    tasks2 = [asyncio.create_task(goto_detail_page_and_download_image(url, save_dir)) for url in results]
    print(type(tasks2), len(tasks2))
    await asyncio.gather(*tasks2)
    print('완료')

if __name__ == "__main__":
    import time
    s = time.time()
    asyncio.run(main())
    e = time.time()
    print(e-s)
    # test()