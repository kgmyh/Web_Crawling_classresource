import scrapy


# 데이터를 여러 사이트에서 가져와야 하는 경우
# ex) 데이터 - 경제뉴스기사, 사이트: 매경, 한경, 머니투데이
# start_urls을 여러사이트 등록 => allowed_domains에도 추가.
# 1. start_urls 에 시작페이지들을 등록 -> parse에서 분기
# 2. start_urls 대신 start_requests() 메소드 이용.

class TestSpider(scrapy.Spider):
    name = 'test_spider'
    allowed_domains = ['naver.com', 'daum.net', 'blog.scrapinghub.com']
    start_urls = ['https://naver.com/', 'https://daum.net', 'https://blog.scrapinghub.com']

    
    def parse(self, response):
        if 'naver' in response.url:
            print('========>네이버 페이지')
        elif 'daum' in response.url:
            print('========>다음 페이지')
        elif 'scrapinghub' in response.url:
            print('========>blog.scrapinghub.com')

# scrapy  crawl  test_spider

# scrapy genspider   test_spider2  naver.com
