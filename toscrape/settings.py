# Scrapy settings for books project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'toscrape'

SPIDER_MODULES = ['toscrape.spiders']
NEWSPIDER_MODULE = 'toscrape.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'books (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False  #True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'books.middlewares.BooksSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#SELENIUM_DRIVER_NAME = 'firefox'   # 'chrome'
#SELENIUM_DRIVER_EXECUTABLE_PATH = '/home/pp/Projects/geckodriver'  #chromedriver'
#SELENIUM_BROWSER_EXECUTABLE_PATH = '/usr/bin/chromium' 
#SELENIUM_DRIVER_ARGUMENTS = ['user-data-dir"=/home/pp/.cache/chromium/Default']
# g2gf3r19.selen', '-no-remote
#SELENIUM_DRIVER_ARGUMENTS = []
#DOWNLOADER_MIDDLEWARES = {
    # 'books.middlewares.BooksDownloaderMiddleware': 543,    
    #'scrapy_selenium.SeleniumMiddleware': 800,
#    'toscrape.middlewares.FoxMiddleware': 800,
#}

TORPWD = 'jelszo'

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
    
#    'books.pipelines.BooksPipeline': 300,
#}

FEED_EXPORTERS = {
   'lll': 'toscrape.spiders.collect.HeadlessCsvItemExporter'
}
IMAGES_STORE = '/home/pp/Projects/toscrape/downloads'

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
