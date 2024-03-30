import scrapy
from coupang_crawler.items import CoupangCrawlerItem
# start_request에서 키워드로 검색한 첫페이지 가져온다. (목록 가져오는 개념)
# parse 에서는 마지막 페이지 번호를 가져와 반복문을 돌리면서 페이지 이동을 하게 한다.
# parse_content 각 페이지의 제품정보를 가져온다.
class CoupanListSpiderSpider(scrapy.Spider):
    name = 'coupang_search'
    allowed_domains = ['coupang.com']
    # start_urls = ['http://coupang.com/']


    # def __init__(self, keyword): self.keyword = keyword
    # scrapy crawl coupang_search -a keyword=coffee  : 실행시 받을 수도 있다.
    # def __init__(self):
    def __init__(self, keyword, test):
        print(keyword, test)
        self.keyword = keyword
        self.url = 'https://www.coupang.com/np/search?q={}&page={}'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'}
    
    # 시작페이지가 검색어 조회이므로 메소드를 쓴다. 
    def start_requests(self):
        # self.keyword = input('키워드: ')
        url = self.url.format(self.keyword, '')  #1을 넣으면 실제 값을 조회할 때 1을 넣으면 중복된 url이라고 크롤링안한다. 그래서 여기선 비움(아님 아래 dont_filter=True로 주고 할 수도 있다.)
        yield scrapy.Request(url=url, callback=self.parse)

#  라스트 페이지를 가져와 그만큼 반복문을 돌려 처리한다.
    def parse(self, response):
        last_page = int(response.css('div.search-pagination > a.btn-last::text').extract_first())
        # for page in range(1, last_page+1):
        for page in range(1,3):
            url = self.url.format(self.keyword, page)
            # print(url)
            # dont_filter=True : 첫번째 페이지는 같은 요청을 다시하는 거라 중복된 url 요청이라고 크롤링안한다. 그래서 준 속성
            yield scrapy.Request(url=url, callback=self.parse_content)#, dont_filter=True) 
    
    def parse_content(self, response):
        # 목록이니까 하나씩 item 만들어서 yield 시킨다.
        item_list = response.css('ul#productList > li.search-product')
        for item in item_list:
            item_name = item.css('div.name::text').get()
            item_link = item.css('a::attr(href)').get()
            item_price = item.css('strong.price-value::text').get()
            
            c_item = CoupangCrawlerItem()
            c_item['item_name'] = item_name
            c_item['item_link'] = item_link
            c_item['item_price'] = item_price
            yield c_item
