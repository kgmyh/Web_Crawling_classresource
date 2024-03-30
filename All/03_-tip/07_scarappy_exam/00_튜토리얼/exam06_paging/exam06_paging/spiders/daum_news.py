import scrapy

# 링크 크롤링 예제(중요)
# 사이트 요구에 맞는 환경 설정 세팅(중요)


import re
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from exam06_paging.items import ArticleItems

# CrawlSpider: 링크를 추출해 탐색하는 기능 (웹크롤링의 기능을 구체화)
# XMLFeedSpider: xml 노드들 크롤링
# CSVFeedSpider: 행단위 크롤링

class DaumNewsSpider(CrawlSpider):
    name = 'daum_news'
    allowed_domains = ['daum.net']
    start_urls = ['https://news.daum.net/breakingnews/digital']  #IT 뉴스 : 이유 적어서.
    
    # 환경설정 - 이 spider에만 적용할 환경설정
    # custom_settings = {
    #     'ROBOTSTXT_OBEY' : True,
    #     'DOWNLOAD_DELAY' : 1
    # }

    # 링크 크롤링 규칙(정규표현식 사용 추천)
    # 정규식 쓸때 꼭 $ 로 끝나야 하는 것 아니다. 시작도 마찮가지고. 그 패턴의 것을 찾는 것이므로..
	# rules : Rule 리스트 
	#         Rule() - 추출할 링크 패턴과 callback 메소드등 크롤링 방식(어떻게 일할지)을 지정
	#           - callback="응답처리할 callback메소드"
    #           - follow=True - 응답받은 페이지에서도 url추출해 요청 할 것인지 여부
    #         LinkExtractor() - 페이지에서 추출할 url 패턴을 정규 표현식으로 지정한다.(아래는 / 로 시작해서 상대경로로 잡는다.)
	#   - cf) 중복 url은 요청하지 않는다.

    # ****rules 변수 (sssss)
    #  ? 앞에 \?  조심.
    rules = [
        # page=\d$ or page=\d+$ : 2자리수 페이지 크롤링
        # follow=True > 여기서 추출한 페이지(Response에서도 찾을 것인지 지정. 무조건 지정한다고 생각하면 된다. (여기선 10까진 첫페이지에 링크가 있어서되는데 11페이지 부터는 그 다음에 있으므로 해줘야 한다.)
        # 동일한 url은 요청하지 않는다.
        # parse 를 호출하지 않는다.

        # GUIDE : 여기 예제에서 끝에 $를 안하면 모든 페이지 다가져온다. \d로 끝나면 1, 11, 111 다 적용되므로. 
        # 상세를 가져올 때는 \d$ 해서 1 ~ 10 만 가져온다.
        # 시작페이지는 1페이지이다. 그리고 1페이지 링크는 없어서 1페이지 요청은 안한다. (상관은없다. follow=True하면 거기에 1페이지가 있으므로 요청한다.)
        Rule(LinkExtractor(allow=r'/breakingnews/digital\?page=\d$'), callback='parse_headline', follow=True),
    ]
    # Rule() cf)
    #    - 추출한 url이 상대경로인 경우 response.urljoin()을 알아서 해준다. 
    #    - parse 메소드를 만들면 start_urls가 적용되어 실행되고 Rule이 적용이 안된다. parse() 사용하지 말아야 한다.
   

    def parse_headline(self, response):
        # URL 로깅
        self.logger.info('Response URL : %s' % response.url)

        # 페이지내 신문 상세 요청
        for url in response.css('ul.list_news2.list_allnews strong.tit_thumb a.link_txt::attr(href)').getall():
            # 신문 기사 URL
            # article_url = url.css('strong > a::attr(href)').extract_first().strip()
            # 요청 
            self.logger.info('--------=====> url : {}'.format(url))
            yield scrapy.Request(url, self.parse_article, meta={'parent_url': response.url})

    def parse_article(self, response):
        # 부모, 자식 수신 정보 로깅 - response.urljoin() response의 domain에 붙인다.
        self.logger.info('-------------------------------------------')
        self.logger.info('Response From Parent URL : %s' % response.meta['parent_url'])
        self.logger.info('Child Response URL : %s' % response.url)
        self.logger.info('Child Response Status : %s' % response.status)
        self.logger.info('-------------------------------------------')

        #기사제목
        title = response.css('h3.tit_view::text').get()
        #기사내용
        p_list = response.css('div.article_view p::text').getall()
        # 리스트 -> 문자열 변경
        article = ''.join(p_list).strip()

        # print(article)      

        yield ArticleItems(title=title, article=article,
                           parent_link=response.meta['parent_url'],
                           article_link=response.url)

# scrapy crawl  daum_news  --nolog
# scrapy crawl  daum_news  --logfile=log.log