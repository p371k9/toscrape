import scrapy
from ..items import QuoteItem
import js2xml

class JsSpider(scrapy.Spider):
    name = 'js'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js']
    #start_urls = ['http://quotes.toscrape.com/js-delayed'] 

    def parse(self, response):
        parsed = js2xml.parse(response.xpath('//script/text()').get()) 
        item = QuoteItem()
        for row in parsed.xpath("//var[@name='data']/array/object"):
            item['author'] = row.xpath("property[@name='author']/object/property[@name='name']/string/text()")[0]
            item['text'] = row.xpath("property[@name='text']/string/text()")[0]
            tags = ''
            for t in row.xpath("property[@name='tags']/array")[0].xpath("string/text()"):
                tags = tags + ' ' + t if len(tags) else t 
            item['tags'] = tags
            yield item
        # copy from login spider
        hh = response.xpath("//li[@class='next']/a/@href").extract()        
        if len(hh):
            self.logger.debug(hh[0])
            u = response.urljoin(hh[0])
            self.logger.debug('*****next url********: ' + u)                    
            # end copy
            yield response.follow(url=u, callback=self.parse)

