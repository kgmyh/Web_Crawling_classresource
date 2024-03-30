# 셀의 내용을 파일에 출력(덮어쓰기) 매직 커맨드는 첫줄에
import scrapy

# scrapy.Item 상속해서 만든다. 클래스 이름은 상관없다.
class CrawlerItem(scrapy.Item):
    title = scrapy.Field()
    sales_price = scrapy.Field()
    original_price = scrapy.Field()
    discount_rate = scrapy.Field()
    link  = scrapy.Field()

   

