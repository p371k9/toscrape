# toscrape

## img crawler

Download images from books.toscrape.com using the Images pipeline.
The name of the downloaded images is a serial number that corresponds to their position in the catalog. Like: 0001.jpg, 0002.jpg ...
You can change where the download starts, so how many images are downloaded, by rewriting the start_urls = variable. See: toscrape/spiders/img.py

To run, enter:


`` `
scrapy crawl img
`` `

The download location will be the downloads/files folder. (settings.py)


