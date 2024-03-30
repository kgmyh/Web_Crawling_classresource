class CrawlerPipeline:
    
    # item-크롤링한 item
    # return item은 최종 프린트되는 곳으로 넘겨준다.
    def process_item(self, item, spider):
        print('='*50)
        print(item['sales_price'])
        print('='*50)
        if int(item['sales_price'] ) >= 50000: #50000이상만 저장
            with open('high_price.txt', 'at') as f: # append 모드로.
                f.write(item['title']+" - "+item['sales_price']+'\n')
        return item

import cx_Oracle
# !pip install cx_Oracle
class DatabasePipeline:

    # DB connection 생성 - 생성자에서 대도 될 듯
    def open_spider(self, spider):
        dsn = cx_Oracle.makedsn('localhost', 1521, 'XE')
        conn = cx_Oracle.connect('scott', 'tiger', dsn)
        self.conn = conn

    # Item DB에 insert 
    # process_item: return-item
    def process_item(self, item, spider):
        print('********************************')
        print(item['title'],int(item['sales_price']), int(item['original_price']), item['link'], item['discount_rate'])
        print('********************************')
        insertSQL = 'INSERT INTO gmarket_items VALUES (gmarket_sequence.nextval, :1, :2, :3, :4, :5)'
        with self.conn.cursor() as cursor:
            cursor.execute(insertSQL, [item['title'], int(item['sales_price']), int(item['original_price']), item['discount_rate'], item['link']])
        self.conn.commit()
        return item

    # connection close
    def close_spider(self, spider):
        self.conn.close()





# 테이블
if False:    
    """
    create sequence gmarket_sequence;
    create table gmarket_items(
        num number primary key,
        title nvarchar2(2000),
        sales_price number,
        original_price number,
        discount_rate number,
        link varchar2(1000)
    )
    """    