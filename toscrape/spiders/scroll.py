import scrapy
import json
from ..items import QuoteItem

class ScrollSpider(scrapy.Spider):
    name = 'scroll'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):        
        data = json.loads(response.body.decode("utf-8"))
        for quote in data['quotes']:
            item = QuoteItem()
            item["author"] = quote['author']['name']
            item["text"] = quote['text']
            yield item
        if data['has_next']:        
            u = 'http://quotes.toscrape.com/api/quotes?page={}'.format(data['page'] + 1)
            yield response.follow(url=u, callback=self.parse)
            
"""
Infinite scroll-al operáló weblap lekaparása. Az API-t kell kibontani! Ami jelen esetben JSON formátumú. Elég egyszerű ez.

Scrape a web page that works with an infinite scroll. The API needs to be extracted! Which in this case is in JSON format. It's pretty simple.
"""        
