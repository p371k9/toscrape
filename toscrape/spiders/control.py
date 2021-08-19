import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import BookItem
from scrapy.shell import inspect_response
import os

class ControlSpider(scrapy.Spider):
    name = 'control'
    allowed_domains = ['books.toscrape.com']        
    start_urls = [
        'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
        'file://'+os.path.abspath(os.getcwd())+'/toscrape/rep.html', # 
        'http://books.toscrape.com/catalogue/soumission_998/index.html']
        # 'http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html',
    
    custom_settings = {
        'SELENIUM_DRIVER_NAME': 'firefox',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': '/usr/local/bin/geckodriver',
        'SELENIUM_DRIVER_ARGUMENTS': ["--width=800", "--height=600"],  # Firefox only
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_selenium.SeleniumMiddleware': 800,
            'toscrape.middlewares.DownloaderControlMiddleware': 900
        },
        'CONTROL_XPATH': 'boolean(//article/div[3]/h2)',
    }        
    
    def start_requests(self):
        for u in self.start_urls:
            yield SeleniumRequest(url=u, callback=self.parse)

    def parse(self, response):
        item = BookItem()
        item['title'] = response.xpath('//h1/text()').get()
        item['price'] = response.xpath('//p[contains(@class,"price_color")]/text()').get()        
        #inspect_response(response, self)
        yield item
        
                
