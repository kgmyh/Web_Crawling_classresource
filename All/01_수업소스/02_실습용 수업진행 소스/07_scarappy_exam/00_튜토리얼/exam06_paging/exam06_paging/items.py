# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItems(scrapy.Item):
    # 기사 제목
    title = scrapy.Field()
    # 기사 본문
    article = scrapy.Field()
    # 요청 리스트 페이지
    parent_link = scrapy.Field()
    # 기사 페이지
    article_link = scrapy.Field()
    # 수집 된 시간
    crawled_time = scrapy.Field()

