# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CoupangCrawlerItem(scrapy.Item):
    
    item_name = scrapy.Field()
    item_link = scrapy.Field()
    item_price = scrapy.Field()
