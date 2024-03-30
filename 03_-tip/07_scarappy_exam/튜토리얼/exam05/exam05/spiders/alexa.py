import scrapy
from exam05.items import RankItem

class AlexaSpider(scrapy.Spider):
    name = 'alexa'
    allowed_domains = ['alexa.com']
    start_urls = ['https://www.alexa.com/topsites']

    # 전체 행:   div.tr.site-listing
    # rank:   div.td  -> 첫번째
    # site_name: div.td.DescriptionCell > p > a::text
    # daily_time : div.td.right > p::text   ==> 1번째
    # daily_page_view : div.td.right > p::text   ==> 2번째
    def parse(self, response):
        trs = response.css('div.tr.site-listing')
        for tr in trs:
            rank = int(tr.css('div.td::text').get())
            site_name = tr.css('div.td.DescriptionCell > p > a::text').get()
            info = tr.css('div.td.right > p::text').getall()
            daily_time = info[0]
            daily_page_view = info[1]
            rank_item = RankItem(rank=rank, site_name=site_name
                                , daily_time=daily_time, daily_page_view=daily_page_view)
            yield rank_item

# scrapy   crawl  alexa  -o output/result.jl

# response.css('div.tr.site-listing') => Selector(Tag, WebElement) => SelectorList
# response.css('div.tr.site-listing::text').getall() => 문자열(str) => List



# scrapy shell https://www.alexa.com/topsites

# result = response.css('div.tr.site-listing')
# len(result)

# result[0].css('div.td::text').get()    #Selector
# result[0].css('div.td.DescriptionCell > p > a::text').get()
# result[0].css('div.td.right > p::text').getall()
