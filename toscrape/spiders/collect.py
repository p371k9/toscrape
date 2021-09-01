import scrapy
from scrapy.shell import inspect_response

#https://stackoverflow.com/questions/34485789/scrapy-csv-output-without-header

from scrapy.exporters import CsvItemExporter
# Adding .lll file ext.  = headless .csv , see: settings.py! custom_settings problematic. Seems not working without predefinition in seettings.py
class HeadlessCsvItemExporter(CsvItemExporter):
    def __init__(self, *args, **kwargs):
        kwargs['include_headers_line'] = False
        super(HeadlessCsvItemExporter, self).__init__(*args, **kwargs)

class CollectSpider(scrapy.Spider):
    name = 'collect'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/catalogue/page-46.html']
    #start_urls = ['http://books.toscrape.com']

    def parse(self, response):
        #inspect_response(response, self)
        for h in response.xpath('//h3/a/@href').extract():                        
            yield {
                'url': response.urljoin(h)
            }
        # copy from login and js spider
        hh = response.xpath("//li[@class='next']/a/@href").extract()        
        if len(hh):
            self.logger.debug(hh[0])
            u = response.urljoin(hh[0])
            self.logger.debug('***** next url ********: ' + u)  
            # end copy                  
            yield response.follow(url=u, callback=self.parse)
