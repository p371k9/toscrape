# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
# from IPython import embed
from requests import get 
from .basictor import BasicTor
# https://www.khalidalnajjar.com/stealthy-crawling-using-scrapy-tor-and-privoxy/
class TorMiddleware(BasicTor):
    def __init__(self, tor_control_port, tor_pwd, tor_proxies, log_level_string):
        self.tor_proxies = tor_proxies
        super().__init__(tor_control_port, tor_pwd, log_level_string)

    @classmethod
    def from_crawler(cls, crawler):
        """Initialize the middleware with the crawler settings"""        
        tor_control_port = crawler.settings.get('TORCTRL')   # control port        
        tor_pwd = crawler.settings.get('TORPWD') # password ()
        tor_proxies = crawler.settings.get('TORPROXIES') # tor port
        #embed()
        log_level_string = crawler.settings.get('LOG_LEVEL')
        if tor_proxies is None:
            tor_proxies = {
                'http': 'socks5://127.0.0.1:9050',
                'https': 'socks5://127.0.0.1:9050'
            }

        if tor_control_port is None:
            tor_control_port = 9051
            
        middleware = cls(
            tor_control_port = tor_control_port,
            tor_pwd = tor_pwd,
            tor_proxies = tor_proxies,
            log_level_string = log_level_string             
        )
        
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)

        return middleware
    
    def new_tor_identity(self, spider):       
        super().new_tor_identity()   
        spider.logger.info("=== IP of the Exit node: " + get('http://icanhazip.com', proxies = self.tor_proxies).text.strip())
        
    def process_request(self, request, spider):        
        spider.logger.debug("*** url: %s", request.url)
        # Allways change IP. - simplest but least effective :/
        self.new_tor_identity(spider)  
        
        resp = get(request.url, proxies = self.tor_proxies)
        hr = HtmlResponse(
            url = resp.url,
            status = resp.status_code,
            #headers = resp.headers,            
            body=resp.text,
            encoding='utf-8',
            request=request
        )
        # embed()        
        return hr
        
    def process_response(self, request, response, spider):
        # Get a new identity depending on the response
        if response.status != 200:
            spider.logger.warning("http code NOT 200")
            self.new_tor_identity(spider)
            return request
        return response
        
    def spider_closed(self):
        """Shutdown Tor when spider is closed"""
        pass
              
from selenium import webdriver
from scrapy_selenium import SeleniumMiddleware

class FoxMiddleware(SeleniumMiddleware):
    def __init__(self):        
        myprofile = webdriver.FirefoxProfile('/home/pp/.mozilla/firefox/g2gf3r19.selen')
        driver_path = r'/home/pp/Projects/geckodriver'
        self.driver = webdriver.Firefox(firefox_profile=myprofile, executable_path=driver_path )
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(800, 600)

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_closed, signals.spider_closed)
        return middleware

import os
class DownloaderControlMiddleware:        
    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        print('***')        
        spider.logger.info('CONTROL_XPATH: %s' % spider.settings.get('CONTROL_XPATH'))
        # https://stackoverflow.com/questions/45183588/using-functions-like-boolean-and-count-with-scrapy-and-xpath
        if bool(int(response.xpath(spider.settings.get('CONTROL_XPATH')).get())) :
            spider.logger.info('xpath ---- CONTROL ---- OK')
            return response
        else:
            # os.system("beep -f 555 -l 1600") # Linux only, beep sys func must be installend. Like: apt get install beep
            input("Press Enter to continue...")
            self.driver = response.request.meta['driver']
            
            # Copied from https://github.com/clemfromspace/scrapy-selenium/blob/develop/scrapy_selenium/middlewares.py /process_response :
            for cookie_name, cookie_value in request.cookies.items():
                self.driver.add_cookie(
                    {
                        'name': cookie_name,
                        'value': cookie_value
                    }
                )

            # wait_until section not copied, not needed
            
            # More copy from https://github.com/clemfromspace/scrapy-selenium/blob/develop/scrapy_selenium/middlewares.py /process_response :            
            
            if request.screenshot:
                request.meta['screenshot'] = self.driver.get_screenshot_as_png()

            if request.script:
                self.driver.execute_script(request.script)

            body = str.encode(self.driver.page_source)

            # Expose the driver via the "meta" attribute
            request.meta.update({'driver': self.driver})            

            return HtmlResponse(
                self.driver.current_url,
                body=body,
                encoding='utf-8',
                request=request
            )
            # end of copy
            
