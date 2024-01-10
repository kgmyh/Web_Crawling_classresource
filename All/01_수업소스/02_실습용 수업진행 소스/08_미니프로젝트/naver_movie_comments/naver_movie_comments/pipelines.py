
import sqlite3
from datetime import datetime
from naver_movie_comments.items import CommentItem
from scrapy.exceptions import DropItem
class DatabaseSqlitePipeline:
    

       
    def open_spider(self, spider):
        spider.logger.info('NewsSpider Pipeline Stated.')
        # Connection 생성
        self.conn = sqlite3.connect('./database.db')#, isolation_level=None) #isolation_level=None : autocommit
        # Cursor 생성
        self.cursor = self.conn.cursor()
        # 테이블 생성 (없으면)
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS movie_comments( num integer PRIMARY KEY,\
                                                        movie_title text, \
                                                        movie_link text,\
                                                        score integer,\
                                                        comment,\
                                                        crawled_time text)")
    # Item insert
    def process_item(self, item, spider):
        
        # # 삽입 시간
        crawled_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 크롤링 시간 필드 추가
        # 데이터 DB 삽입
        try:
            self.cursor.execute('INSERT INTO movie_comments(num,\
                                                movie_title,\
                                                movie_link,\
                                                score,\
                                                comment,\
                                                crawled_time) VALUES (?, ?, ?, ?, ?, ?)',
                                [item.get('num'),
                                 item.get('movie_title'), 
                                 item.get('movie_link'), 
                                 item.get('score'), 
                                 item.get('comment'),
                                 crawled_time])
            # 로그
            spider.logger.info('Item to DB Inserted')
            spider.logger.logger.info('-------------------------------------------')
            # 결과 리턴
            return item
        except Exception as e:
            raise DropItem("insert 실패. 이유 - {}".format(str(e)))
        

    def close_spider(self, spider):
        spider.logger.info('Comments Pipeline Stopped.')
        # 커밋
        self.conn.commit()
        # 연결 해제
        self.cursor.close()
        self.conn.close()
