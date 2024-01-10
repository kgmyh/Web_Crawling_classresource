import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from naver_movie_comments.items import CommentItem
# 페이지 링크 패턴 : '/movie/point/af/list.nhn?&page=2'  
#
# 평점 - 테이블 구조로 되어있고 한페이지에 10개씩 나온다.
#
# Selector
# - 평점 tr들 : table.list_netizen > tbody > tr
# - 크롤링 대상 (tr의 하위)
#   - 영화제목: td.title > a.movie.color_b::text
#   - 영화링크: td.title > a.movie.color_b::attr(href)  
#       - 형식: href="?st=mcode&sword=185917&target=after"
#       - 절대경로(https:// 로 시작)가 아니라 상대경로로 되어 있다. urljoin 필요
#   - 평점 : td.title > div.list_netizen_score > em::text
#   - 댓글 : td.title::text  체크: 댓글 안쓴 것도 있다. (평점만 넣고.)

import sqlite3

class NaverMovieCommentSpider(CrawlSpider):
    name = 'naver_movie_comment'
    allowed_domains = ['naver.com']
    start_urls = ['https://movie.naver.com/movie/point/af/list.nhn']
    rules = [
        # 추출한 url이 상대경로인 경우 response.urljoin()을 알아서 해준다. 
        # parse 메소드를 만들면 start_urls가 적용되어 실행되고 Rule이 적용이 안된다. parse() 사용하지 말아야 한다.
        Rule(LinkExtractor(allow=r'/movie/point/af/list.nhn\?&page=\d{1,4}$'), callback='parse_comments', follow=True),
    ]


    # 이미 저장된 것은 처리 안되도록 하기 - 그페이지의 크롤링을 멈추다. (return 시킴)
    # 스파이더를 종료하면 안된다. 비동기적으로 실행되므로 아직 크롤링가능한 페이지는 시작안했을 수 있다.
    # from scrapy.project import crawler  #이러면 종료한다는데 테스트는 안해봄.
    # crawler._signal_shutdown(9,0)

    ## 근데 어짜피 1000페이지고 하루에 한번정도만 해도 중복될 일은 없으므로 빼도 될 것 같다.
    def __init__(self):
        super().__init__()
        # 저장된 comment의 nums중 제일 큰 값을 읽어 들인다. 
        # 크롤링 할 때 이미 조회된 것이 있으면 크롤링을 멈추게 하기 위해 
        # csv를 읽어도 되는데 파일이 커지면 부담이 될 것같아 DB에서 조회. csv는 readlines()[-1] 을 읽은 뒤 num값 조회. json 딕셔너리로 읽어도 되고.
        sql = 'SELECT max(num) FROM movie_comments'
        
        # try:
        conn = sqlite3.connect('./database.db')
        cursor = conn.cursor()
        cursor.execute(sql)
        self.num = str(cursor.fetchone()[0])
        print(self.num)
        # print(type(self.num))
        # print(self.num, type(self.num))
        # except Exception as e:
            # self.logger.info('max(num) 조회도중 오류 발생. {}'.format(str(e)))
    def parse_comments(self, response):
        
        comments_trs = response.css('table.list_netizen > tbody > tr')
        if not comments_trs:
            return
        for tr in comments_trs:
            num = tr.css('td:nth-child(1)::text').get().strip()
            if self.num :
                if self.num >= num:  #self.num 이 있고 조회한 num 과 같으면 종료
                    # print('이미 저장된 데이터입니다.{}'.format(num))
                    self.logger.debug('이미 저장된 데이터입니다.{}'.format(num))
                    break # 그 페이지 저장은 하지 않도록 한다. 
                    
            movie_title = tr.css("td.title > a.movie.color_b::text").get()

            # response.urljoin(url) : 응답 받은 url에 매개변수로 넣은 url을 알맞게 처리하여 붙인 url을 만들어 준다.             
            movie_link = response.urljoin(tr.css('td.title > a.movie.color_b::attr(href)').get().strip())
            score = int(tr.css('td.title > div.list_netizen_score > em::text').get().strip())
            # comment는 태그 내에 태그들이 있고 그 중간 중간 문자열들이 있어 getall()으로 읽어야 한다. 
            c_list = tr.css('td.title::text').getall()
            # comment = tr.xpath('./td[@class="title"]/text()').getall()
            comment = ' '.join(c_list).strip()

            yield CommentItem(num=num,movie_title=movie_title, movie_link=movie_link, score=score, comment=comment)
