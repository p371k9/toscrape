# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class QuoteItem(scrapy.Item):    
    author = scrapy.Field()
    text = scrapy.Field()
    tags = scrapy.Field()
    
class imgItem(scrapy.Item):
    # define the fields for your item here like:
    images = scrapy.Field()
    image_urls = scrapy.Field()
    
class BookItem(scrapy.Item):    
    title = scrapy.Field()
    price = scrapy.Field()
    rating = scrapy.Field()
    availability = scrapy.Field()
    upc = scrapy.Field()
    
        
