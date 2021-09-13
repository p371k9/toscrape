import scrapy
from scrapy_selenium import SeleniumRequest
from ..items import BookItem
#from scrapy.shell import inspect_response
import os

class ControlSpider(scrapy.Spider):
    name = 'control'
    allowed_domains = ['books.toscrape.com']        
    start_urls = [
        'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html',
        'file://'+os.path.abspath(os.getcwd())+'/toscrape/rep.html?href=http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html&a=Tipping+the+Velvet', # 
        'http://books.toscrape.com/catalogue/soumission_998/index.html']
        # 'http://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html',
    
    withoutprofile = {  # scrapy_selenium        
        'SELENIUM_DRIVER_NAME': 'firefox',   # chrome | firefox
        'SELENIUM_DRIVER_EXECUTABLE_PATH': '/home/pp/Projects/geckodriver',  # chromedriver | geckodriver
        #'SELENIUM_BROWSER_EXECUTABLE_PATH': '/usr/bin/chromium', 
        'SELENIUM_DRIVER_ARGUMENTS': ["--width=800", "--height=600"],  # Firefox only     
        'DOWNLOADER_MIDDLEWARES': { 
            'scrapy_selenium.SeleniumMiddleware': 800, # It will not work with profiles!
            'toscrape.middlewares.DownloaderControlMiddleware': 900,
        },
        'CONTROL_XPATH': 'boolean(//article/div[3]/h2)',
    }
    withprofile = { # a descendant of scrapy_selenium        
        'LOG_LEVEL': 'INFO',  # Selenium profile copy fillout the console
        'DOWNLOADER_MIDDLEWARES': {
            # settings in FoxMiddleware
            'toscrape.middlewares.FoxMiddleware': 800, ## comment out this line if you want to use the original selenium-scrapy middleware
            'toscrape.middlewares.DownloaderControlMiddleware': 900,
        },
        'CONTROL_XPATH': 'boolean(//article/div[3]/h2)',        
    }
    custom_settings = withoutprofile
    
    def start_requests(self):
        for u in self.start_urls:
            yield SeleniumRequest(url=u, callback=self.parse)

    def parse(self, response):
        item = BookItem()
        item['title'] = response.xpath('//h1/text()').get()
        item['price'] = response.xpath('//p[@class="price_color"]/text()').get()
        dik = response.xpath('//div[@class="col-sm-6 product_main"]/p[3]/@class').get().split()[1]
        Otig = ['One', 'Two', 'Three', 'Four', 'Five']
        item['rating'] = 0
        for i in range(5):
            if Otig[i] == dik:
                item['rating'] = i + 1
                break
        item['upc'] = response.xpath('//th[contains(text(), "UPC")]/following::td[1]/text()').get()
        item['availability'] = response.xpath('//th[contains(text(), "Availability")]/following::td[1]/text()').get()
        #self.logger.info('********* Item values: %s' % item)        
        #inspect_response(response, self)
        yield item
        
                
