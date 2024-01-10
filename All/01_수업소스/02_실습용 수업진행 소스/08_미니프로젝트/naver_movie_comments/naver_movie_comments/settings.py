# Scrapy settings for naver_movie_comments project
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'naver_movie_comments'

SPIDER_MODULES = ['naver_movie_comments.spiders']
NEWSPIDER_MODULE = 'naver_movie_comments.spiders'



USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 0.5

ITEM_PIPELINES = {
   'naver_movie_comments.pipelines.DatabaseSqlitePipeline': 300,
}

# key: feed_uri(파일명) value: 각 feed 속성
# https://docs.scrapy.org/en/latest/topics/feed-exports.html#feeds
FEEDS = {
   './output/result.json':{
      'format':'json',
      'encoding':'utf8',
      'indent':4,
   },
   './output/ result.csv':{
      'format':'csv',
      'encoding':'utf8'
   }
}
# # 출력 파일 관련 설정  -o 파일명
# # 파일경로
# FEED_URI = "output/result.json"
# # 파일 형식  -t 파일형식 : json, jsonlines, csv, xml, pickle, marshal
# FEED_FORMAT = 'json'
# # 출력 인코딩 설정
# FEED_EXPORT_ENCODING = 'utf-8'
# # 들여쓰기 간격
# FEED_EXPORT_INTENT = 4

###############################################################
# https://docs.scrapy.org/en/latest/topics/settings.html#log-enabled
# 로그관련 설정 - 처음에는 하지말자. 터미널에 로그가 안나온다.
import logging
LOG_FILE = 'logs/logfile.log'
LOG_LEVEL = logging.DEBUG

# # 로그 찍는 시간을 지정한 포멧으로 한다. (로그내용에 logger.info() 한것 출력할 때 (스크래피 자체로그 포함) 시간)
LOG_DATEFORMAT = '%Y-%m-%d_%H-%M-%S'

# 이걸 True로 하면 print() 로 출력하는 것도 로그파일에 저장된다.
# LOG_STDOUT=True

# 로그 레벨
# 1. logging.CRITICAL : for critical errors 
# 2. logging.ERROR : for regular errors 
# 3. logging.WARNING : for warning messages 
# 4. logging.INFO : for informational messages 
# 5. logging.DEBUG : for debugging messages