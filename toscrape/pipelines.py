# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#from itemadapter import ItemAdapter

import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

from itemadapter import ItemAdapter

# https://doc.scrapy.org/en/latest/topics/media-pipeline.html#module-scrapy.pipelines.files
class imgPipeline(ImagesPipeline):    
    def file_path(self, request, response=None, info=None, *, item=None):
        return 'files/' + item['images'][0]

class BooksPipeline:
    def process_item(self, item, spider):
        return item

