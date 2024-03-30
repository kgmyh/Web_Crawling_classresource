import scrapy
from naver_movie_crawler.items import NaverMovieCrawlerItem

# 네이버영화 > 상영작/개봉작 리스트
# 1. 각 영화 링크
# 2. 링크로 들어가 영화의 제목, 관객수, 평점 을 크롤링
class NaverMovieSpider(scrapy.Spider):
    name = "NaverMovie"
    allow_domain = ['https://movie.naver.com']
    start_urls = ['https://movie.naver.com/movie/running/current.nhn'] #상영작/개봉작 리스트

    def parse(self, response):
        """
        response: start_urls의 요청결과: TextResponse
        link xpath : //*[@id="content"]/div[1]/div[1]/div[3]/ul/li/dl/dt/a/@href
        """
        links = response.xpath('//*[@id="content"]/div[1]/div[1]/div[3]/ul/li/dl/dt/a/@href').extract()
        for link in links:
            # 조회된 link는 상대경로(/movie/bi/mi/basic.nhn?code=185917) 이므로 절대 경로로 합친다. (/로 시작이므로 port를 base로 해서 합쳐준다.)
            link = response.urljoin(link)
            yield scrapy.Request(link, callback=self.parse_page_contents)
    
    def parse_page_contents(self, response):
        item = NaverMovieCrawlerItem()
        item['title'] = response.xpath('//*[@id="content"]/div[1]/div[2]/div[1]/h3/a[1]/text()').extract()[0]
        # 관객수 (예정작의 경우 관객수가 없다. (날짜가 오늘 이후의 것을 확인.)) => extract()는 조회결과가 없으면 [] 리스트 반환(예외발생안함.) extract()[0] 에서 Index Outof Bounds 예외 발생
        try:
            item['count'] = response.xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[5]/div/p[2]/text()').extract()[0]
        except:
            item['count'] = "0명"
        # item['count'] = response.xpath('//*[@id="content"]/div[1]/div[2]/div[1]/dl/dd[5]/div/p[2]/text()').extract()[0]
        # 평점이 8.6의 경우  <em>8</em><em>.</em><em>6</em> 식임 em아래 text()들을 가져와 합친다.
        # TODO: 평점이 없는 경우도 있다. (관람객 평점 없는 경우) 이때 Na로 들어간다. 흠.. 예외 발생 안하나?
        # TODO 답:  extract()는 조회결과가 없으면 [] 리스트 반환(예외발생안함.) 
        #           extract()[0] 에서 Index Outof Bounds 예외 발생하는 것이다.
        #           여기서는 index로조회 안하므로 예외발생하지 않는다. 관객 평점이 없는 경우 경우 "" 이된다. pandas에서 csv로 읽으면 NA로 들어간다.
        score = response.xpath('//*[@id="actualPointPersentBasic"]/div/em/text()').extract() 
        item['score'] = ''.join(score)
        # item['score'] = "".join(response.xpath('//*[@id="actualPointPersentBasic"]/div/em').extract())
        yield item

