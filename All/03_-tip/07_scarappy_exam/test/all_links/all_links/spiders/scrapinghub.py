import scrapy


class ScrapinghubSpider(scrapy.Spider):
    name = 'scrapinghub'
    allowed_domains = ['blog.scrapinghub.com']
    start_urls = ['https://blog.scrapinghub.com/']

    def parse(self, response):
        for link in response.css('a::attr(href)').extract():
        
            yield scrapy.Request(link, self.parse_link)

    def parse_link(self, response):
        yield {
            'url':response.url,
            'body':response.body
        }
        # for link in response.css('a::attr(href)'):
            # if link == 'https://blog.scrapinghub.com/' or link == 'https://blog.scrapinghub.com':
            #     continue
            # yield scrapy.Request(response.urljoin(link), self.parse_link)
        

