# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommentItem(scrapy.Item):
    num = scrapy.Field() #댓글 번호
    movie_title = scrapy.Field()
    movie_link = scrapy.Field()
    score = scrapy.Field()
    comment = scrapy.Field()
