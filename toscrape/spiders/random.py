import scrapy
from ..items import QuoteItem

from scrapy.shell import inspect_response

class RandomSpider(scrapy.Spider):
    name = 'random'
    custom_settings = {
        'ITEM_PIPELINES': {
            'toscrape.pipelines.RandomPipeline': 1
        },
    }   
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/random']
    cont = True
    attempt = 0
    
    def parse(self, response):
        item = QuoteItem()
        item['author'] = response.xpath('//span/small[@class="author"]/text()').get()
        item['text'] = response.xpath('//span[@class="text"]/text()').get()
        tags = ''
        for t in response.xpath('//a[@class="tag"]/text()').extract():
            tags = tags + ' ' + t if len(tags) else t
        item['tags'] =  tags
        self.attempt += 1
        self.logger.info("=== ALL scrap: %s", self.attempt) # another log format https://docs.python.org/3/howto/logging.html#formatters
        #inspect_response(response, self)
        yield item
        if self.cont:
            yield response.follow(url='http://quotes.toscrape.com/random', dont_filter=True)  # off the dupefilter
