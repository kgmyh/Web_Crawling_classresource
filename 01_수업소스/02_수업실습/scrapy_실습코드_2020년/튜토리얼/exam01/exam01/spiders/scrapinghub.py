import scrapy

class ScrapinghubSpider(scrapy.Spider):
    # spider 이름 - 프로젝트 실행시킬때 사용할 이름.
    name = 'scrapinghub'
    # spider에게 크롤링을 허용할 도메인
    allowed_domains = ['blog.scrapinghub.com']
    # 크롤링할 시작 url
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        print('================================')
        print('headers==>', response.headers)
        print('meta==>', response.meta)
        print('encoding==>', response.encoding)
        print('status==>', response.status)
        print('body===>', response.body)
        print('================================')

