# Scrapy settings for exam06_paging project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'exam06_paging'

SPIDER_MODULES = ['exam06_paging.spiders']
NEWSPIDER_MODULE = 'exam06_paging.spiders'

# 출력 파일 관련 설정  -o 파일명
# 파일경로
FEED_URI = "output/result.json"
# 파일 형식  -t 파일형식 : json, jsonlines, csv, xml, pickle, marshal
FEED_FORMAT = 'json'
# 출력 인코딩 설정
FEED_EXPORT_ENCODING = 'utf-8'
# 들여쓰기 간격
FEED_EXPORT_INTENT = 4

# 저장소, 저장형식 관련 세팅은 레퍼런스 참조
# https://docs.scrapy.org/en/latest/topics/feed-exports.html#feed-storages

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

ITEM_PIPELINES = {
   'exam06_paging.pipelines.DatabaseSqlitePipeline': 300,
}

# 로그관련 설정 - 처음에는 하지말자. 터미널에 로그가 안나온다.
import logging
LOG_FILE = 'logfile.log'
LOG_LEVEL = logging.DEBUG

# 로그 레벨
# 1. logging.CRITICAL : for critical errors 
# 2. logging.ERROR : for regular errors 
# 3. logging.WARNING : for warning messages 
# 4. logging.INFO : for informational messages 
# 5. logging.DEBUG : for debugging messages




