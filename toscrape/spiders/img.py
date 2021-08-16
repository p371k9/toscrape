import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import imgItem 

from scrapy.shell import inspect_response

class ImgSpider(CrawlSpider):
    name = 'img'
    allowed_domains = ['books.toscrape.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            #'scrapy.pipelines.images.ImagesPipeline': 1
            'toscrape.pipelines.imgPipeline': 1
        },
    }        
    
    start_urls =  ['http://books.toscrape.com/catalogue/category/books/mystery_3/index.html']  # Only images from books in the mystical category will be downloaded.  
    # start_urls = ['http://books.toscrape.com/']    # All images will be downloaded. 1000 pieces.
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths=r'//li[contains(@class, "next")]'), callback='parse_catalogue', follow=True),
        Rule(LinkExtractor(allow=r'index.html', deny=[r'category', r'//books.toscrape.com/index.html']), callback='parse_book', follow=False),    
    )    
    bookUrls = list()
    
    def parse_catalogue(self, response):
        self.logger.info('*********')
        self.logger.info(response.xpath('//title/text()').get())        
        for h in response.xpath('//h3/a/@href').extract():            
            self.bookUrls.append(response.urljoin(h))            
        self.logger.info(self.bookUrls)        
        #inspect_response(response, self)        
        
    def parse_start_url(self, response):
        return self.parse_catalogue(response)    

    def parse_book(self, response):
        self.logger.info('==========')
        self.logger.info(response.xpath('//title/text()').get())
        item = imgItem()
        item["image_urls"] = [response.urljoin(response.css("div.item.active > img::attr(src)").extract_first())]
        item["images"] = ['{:04d}.jpg'.format(self.bookUrls.index(response.request.url) + 1)]
        #inspect_response(response, self)        
        return item
