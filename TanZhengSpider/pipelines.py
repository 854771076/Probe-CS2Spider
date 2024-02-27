# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .utils import MongoDB
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class TanzhengspiderPipeline:
    def process_item(self, item, spider):
        return item


class DefaultPipeline:

    def open_spider(self, spider):
        # 建立连接
        self.conn = MongoDB(spider.collection, database=settings.get('MONGODB_DB'), host=settings.get('MONGODB_HOST'), port=settings.get('MONGODB_PORT'), username=settings.get('MONGODB_USER'),
                 password=settings.get('MONGODB_PSW'), authSource=settings.get('MONGODB_AUTHSOURCE'))

    def process_item(self, item, spider):
        try:
            self.conn.update_item(item,spider.column)
            
        except Exception as e:
            spider.logger.error(e)

    def close_spider(self, spider):
        self.conn.submit()
        self.conn.close()
