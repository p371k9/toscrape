# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

# https://doc.scrapy.org/en/latest/topics/media-pipeline.html#module-scrapy.pipelines.files
class imgPipeline(ImagesPipeline):    
    def file_path(self, request, response=None, info=None, *, item=None):
        return 'files/' + item['images'][0]

#from IPython import embed

class RandomPipeline:
    # https://stackoverflow.com/questions/46749659/force-spider-to-stop-in-scrapy
    def __init__(self):
        self.texts_seen = set()

    def process_item(self, item, spider):
        def log():
            spider.logger.info(f"*** UNIQUE: {len(self.texts_seen)}")   # a log format
        def size_control():            
            if len(self.texts_seen) >= 100 : # sum 100 quotes stored in website
                spider.logger.debug("******** stop yielding in spider ******")
                spider.cont = False

        adapter = ItemAdapter(item)
        #embed()
        if adapter['text'] in self.texts_seen:
            log()
            raise DropItem(f"Duplicate item found: {item!r}")
        else:            
            self.texts_seen.add(adapter['text'])
            log()
            size_control()
            return item

