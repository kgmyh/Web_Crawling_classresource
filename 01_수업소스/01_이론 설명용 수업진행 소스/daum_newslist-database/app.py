import pymysql
from crawling import get_daum_news_list
from news_list_db import insert_news_list
if __name__ == '__main__':
    host: str = '192.168.0.31'
    user: str = 'playdata'
    password: str = '1111'
    database: str = 'news_list'

    with pymysql.connect(host=host, port=3306, user=user, password=password, database=database) as connection:
        with connection.cursor() as cursor:
            news_list = get_daum_news_list()
            for news in news_list:
                insert_news_list(cursor, news[0], news[1])
            connection.commit()

