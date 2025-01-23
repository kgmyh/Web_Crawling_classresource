# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
# Scrapy Item
# 장점 
# 1. 수집 데이터를 일관성있게 관리 가능
# 2. 데이터를 사전형(Dict)로 관리, 오타 방지
# 3. 추후 가공 및 DB 저장 용이
import scrapy


class BlogItem(scrapy.Item):
    # define the fields for your item here like:
    
    title = scrapy.Field()
    write_date = scrapy.Field()
    writer = scrapy.Field()
    comment_cnt = scrapy.Field()
    blog_contents = scrapy.Field()


