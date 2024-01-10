# search_words_async.py

import time
import asyncio
# aiohttp 설치 필요
import aiohttp
from bs4 import BeautifulSoup


async def get_word(url, session):  # 코루틴 정의
    print(f'Send request to ... {url}')

    async with session.get(url) as res:
        text = await res.text()
    soup = BeautifulSoup(text, 'lxml')
    tag_list = soup.select('span.DEFINITION')
    result = [t.text for t in tag_list]
    return result


async def main(url_list):
    base_url = 'https://www.macmillandictionary.com/us/dictionary/american/{keyword}'
    keywords = ['hi', 'apple', 'banana', 'call', 'feel',
                'hello', 'bye', 'like', 'love', 'environmental',
                'buzz', 'ambition', 'determine', 'tiger','cat','routine','main','function','go','get','take','run','fruite','zoo','camel']
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    async with aiohttp.ClientSession(headers={"User-Agent":ua}) as sess: 
        tasks = [get_word(base_url.format(keyword=keyword), sess) for keyword in keywords]
        result  = await asyncio.gather(*tasks)
        return result

if __name__ == '__main__':
        

    base_url = 'https://www.macmillandictionary.com/us/dictionary/american/{keyword}'
    keywords = ['hi', 'apple', 'banana', 'call', 'feel',
                'hello', 'bye', 'like', 'love', 'environmental',
                'buzz', 'ambition', 'determine'] 
    url_list = [base_url.format(keyword=word) for word in keywords]

    start = time.perf_counter()
    result = asyncio.run(main(url_list))
    print(len(result))
    print(result[0])
    end = time.perf_counter()
    print(f'time taken: {end-start}')