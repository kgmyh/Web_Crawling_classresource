import scrapy


# 블로그 내용 : div.section.post-body > span > *::text
#         //div[class="section post-body"]/span/*/text()

class ScrapinghubSpider(scrapy.Spider):
    name = 'scrapinghub'
    allowed_domains = ['blog.scrapinghub.com']
    start_urls = ['http://blog.scrapinghub.com/']

    # 메인페이지의 링크를 크롤링
    # 링크 - div.post-header > h2 > a::attr(href)
    def parse(self, response):
        for url in response.css("div.post-header > h2 > a::attr(href)").getall():
            #  Request() 요청 객체 - 1. url, 2. 응답처리할 callback 메소드
            yield scrapy.Request(url, self.parse_blog)
                

    # 블로그 하나하나를 크롤링.
    def parse_blog(self, response):
        contents = response.css('div.section.post-body > span > *::text').getall()
        blog_contents = " ".join(contents)
        yield {
            'blog_contents':blog_contents
        }
