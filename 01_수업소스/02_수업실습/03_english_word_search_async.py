# english_word_search_async.py
########################
#import 
##########################
import asyncio
import aiohttp 
import time

async def get_word(url, session):
    async with session.get(url) as response:
        if response.status == 200:
            return await response.text()

async def main(url_list):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
    headers = {
        "User-Agent":user_agent
    }
    async with aiohttp.ClientSession(headers=headers) as session:
        result_list = await asyncio.gather(*[get_word(url, session) for url in url_list])
        return result_list

if __name__ == '__main__':        

    base_url = 'https://www.macmillandictionary.com/us/dictionary/american/{keyword}'
    keywords = ['hi', 'apple', 'banana', 'call', 'feel',
                'hello', 'bye', 'like', 'love', 'environmental',
                'buzz', 'ambition', 'determine'] 
    url_list = [base_url.format(keyword=word) for word in keywords]
    # print(url_list)
    start = time.time()
    result = asyncio.run(main(url_list))
    end = time.time()
    print(len(result))
    print(result[0])
    print("걸린시간:",end-start, "초")

