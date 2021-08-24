import scrapy
from ..items import QuoteItem

def authentication_failed(response):
    # TODO: Check the contents of the response and return True if it failed
    # or False if it succeeded.
    print("Auth Oké.")
    return False

from scrapy.shell import inspect_response

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/login']

    def parse(self, response):
        self.logger.info("Login attempt with john:secret account.")
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'john', 'password': 'secret'},
            callback=self.after_login
        )

    def after_login(self, response):
        if authentication_failed(response):
            self.logger.error("Login failed")
            return
        # continue scraping with authenticated session...        
        #inspect_response(response, self)        
        self.logger.debug("This is the parse page func")
        for sect in response.xpath('//div[@class="quote"]'):
            item = QuoteItem()
            item["text"] = sect.xpath('span[@class="text"]/text()').get()
            item["author"] = sect.xpath('span/small[@class="author"]/text()').get()
            yield item
        hh = response.xpath("//li[@class='next']/a/@href").extract()
        self.logger.debug(hh[0])
        if len(hh):
            u = response.urljoin(hh[0])
            self.logger.debug('*****next url********: ' + u)                    
            yield response.follow(url=u, callback=self.after_login)
        else:
            self.logger.info("Logging out...")
            yield response.follow(url='http://quotes.toscrape.com/logout')

