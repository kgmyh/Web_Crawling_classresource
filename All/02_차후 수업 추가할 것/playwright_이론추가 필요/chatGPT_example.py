import asyncio
from playwright.async_api import async_playwright

async def crawl(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content

async def main():
    urls = ['https://www.example.com', 'https://www.google.com', 'https://www.github.com']
    tasks = [asyncio.create_task(crawl(url)) for url in urls]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(result)

if __name__ == '__main__':
    asyncio.run(main())
