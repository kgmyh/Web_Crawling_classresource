# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# 파이프라인(pipeline) 컴포넌트
# spider가 반환한 Item을 출력전에 받아서 처리하는 컴포넌트.
# 처리
# - 데이터 검증
# - Database 에 insert
# - SNS 로 전송
# - 메일 전송
#
#  1. 파이프라인 클래스 구현 => 기능당 한개의 클래스를 만드는 것이 좋다.
#  2. settings.py 에 등록

from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
# 파이프라인 진행과정에서 버릴 Item인 경우 발생시킬 예외.
#   process_item()에서 DropItem을 발생시키면(raise) 그 Item은 다음 단계로 넘기지 않는다.

class RankCheckPipeline:
    # spider가 일(크롤링)을 시작할 때 한번 호출된다.
    # 주로 process_item이 계속 사용하는 자원(DB 연결등)을 생성하는 작업을 한다.
    def open_spider(self, spider):
        print("===================")
        print('RankCheckPipeline.open_spider()실행')
        print("===================")

    # spider가 반환한 Item을 처리하는 작업을 한다. 
    # item이 yield 될때 마다 호출 된다.
    # rank가 31위 이상인 것은 출력되지 않도록 막는다.
    def process_item(self, item, spider):

        if item['rank'] > 30:
            # DropItem 을 던지면 그 Item은 파이프라인에서 제거되어 다음으로 넘어가지 않는다. 그러나 Item 정보는 로그에 DropItem 생성시 전달한 문자열과 함께 출력된다.
            raise DropItem('Drop 시킨 item : {}.{}'.format(item['rank'], item['site_name']))

        print("===================")
        print('RankCheckPipeline.process_item()실행: {}'.format(item.get('site_name')))
        print("===================")
        return item

    # spider가 일(크롤링)을 종료할 때 한번 호출 된다.
    # 주로 open_spider() 에서 만든 자원을 반납하는 일을 한다. (연결 끊기)
    def close_spider(self, spider):
        print("===================")
        print('RankCheckPipeline.close_spider()실행')
        print("===================")

# scrapy crawl alexa  -o output/result2.json    


# 디비연동 - sqlite3 (IF EXISTS 구문이 있어 테이블 생성을 프로그램에서 할 수있다. (오라클은 안됨.))
# open_spider() - connection 생성 + cursor() 생성 + DB 테이블 생성
# process_item() - item 을 insert
# close_spider() - cursor(), connection() close
import sqlite3
from datetime import datetime
class SqlitePipeline(object):
    
    def open_spider(self, spider):
        spider.logger.info('NewsSpider Pipeline Stated.')
        # Connection 생성
        self.conn = sqlite3.connect('C:/temp/database.db')#, isolation_level=None) #isolation_level=None : autocommit
        # Cursor 생성
        self.cursor = self.conn.cursor()
        # 테이블 생성 (없으면)
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS TOPRANK(id INTEGER PRIMARY KEY AUTOINCREMENT,\
                                                rank INTEGER, \
                                                site_name text, \
                                                daily_time_site text,\
                                                daily_page_view text,\
                                                crawl_time text)")
    # Item insert
    def process_item(self, item, spider):
        
        # 삽입 시간
        crawled_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 크롤링 시간 필드 추가
        # item['crawled_time'] = crawled_time
        # 데이터 DB 삽입
        try:
            self.cursor.execute('INSERT INTO TOPRANK(rank,\
                                                site_name,\
                                                daily_time_site,\
                                                daily_page_view,\
                                                crawl_time) VALUES (? ,?, ?, ?, ?)',
                                (item.get('rank'), item.get('site_name'), item.get('daily_time_site'),
                                 item.get('daily_page_view'), crawled_time))  
            # 로그
            spider.logger.info('Item to DB Inserted')
            spider.logger.logger.info('-------------------------------------------')
            # 결과 리턴
            return item
        except Exception as e:
            raise DropItem("{}.{} insert 실패. 이유 - {}".format(item.get('rank'), item.get('site_name'), str(e)))
        

    def close_spider(self, spider):
        spider.logger.info('NewsSpider Pipeline Stopped.')
        # 커밋
        self.conn.commit()
        # 연결 해제
        self.cursor.close()
        self.conn.close()

      