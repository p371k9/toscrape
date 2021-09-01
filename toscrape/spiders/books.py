import scrapy
from .control import ControlSpider
from ..items import BookItem

class BooksSpider(ControlSpider):
    name = 'books'
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'toscrape.middlewares.ProxyMiddleware': 800
        }
    };
    
    def __init__(self, lll=None, *args, **kwargs):        
        self.start_urls =  []    
        if lll != None:
            with open(lll) as f:
                content = f.readlines()
            content = [x.strip() for x in content]
            self.start_urls = content
    
    # restore the original start_urls        
    # https://stackoverflow.com/questions/31232098/how-to-call-super-method-from-grandchild-class
    def start_requests(self):
        return scrapy.Spider.start_requests(self)

