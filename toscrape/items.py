# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class imgItem(scrapy.Item):
    # define the fields for your item here like:
    images = scrapy.Field()
    image_urls = scrapy.Field()

