# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

# 제목, 관객수, 평점 크롤링
import scrapy


class NaverMovieCrawlerItem(scrapy.Item):
    title = scrapy.Field()
    count = scrapy.Field()
    score = scrapy.Field()
    
