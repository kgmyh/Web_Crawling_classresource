import scrapy
from crawler.items import CrawlerItem  #item import

class Spider(scrapy.Spider):
    name = "GmarketBestSellers" #실행시킬 이름
    allow_domain = ['gmarket.co.kr'] # 이 도메인 내의 내용만 크롤링 하겠다.
    start_urls = ['http://corners.gmarket.co.kr/Bestsellers'] #최초에 크롤링할 페이지의 url. 여러개 등록 가능. 여러 url이면 동시에 여러개가 실행된다.
    
    # request에 대한 response를 받아 이 메소드가 실행된다.
    def parse(self, response):
        # 목록의 링크들 가져와서 반복문 돌린다.
        links = links = response.xpath('//*[@id="gBestWrap"]/div/div[3]/div[2]/ul/li/div[1]/a/@href').extract()
        # 하나의 링크를 가져와 요청한뒤 그 response를 callback 에게 전달한다.
        for link in links[:10]:
            yield scrapy.Request(link, callback=self.page_content)
    
    # 상세페이지의 response를 받아서 원하는 처리를 하면된다.
    def page_content(self, response):
        item = CrawlerItem()
        item['title'] =  response.xpath('//*[@id="itemcase_basic"]/h1/text()')[0].extract()
        item['sales_price'] = response.xpath('//*[@id="itemcase_basic"]/p/span/strong/text()')[0].extract().replace(',','')
        try:
        # 오리지날 가격이 없는 경우 element가 없어서 예외 발생한다. 이런 경우 sales_price를 넣는다.
            item['original_price'] = response.xpath('//*[@id="itemcase_basic"]/p/span/span/text()')[0].extract().replace(',','')
        except:
            item['original_price'] = item['sales_price']
        # item['discount_rate'] = str(round(1-int(item['sales_price'])/int(item['original_price']), 2)*100) + '%'
        item['discount_rate'] = int(round(1-int(item['sales_price'])/int(item['original_price']), 2)*100)
        item['link'] = response.url # 요청한 url을 받을 수 있다. 
        yield item
