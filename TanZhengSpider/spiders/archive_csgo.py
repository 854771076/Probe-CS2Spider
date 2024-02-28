import scrapy
from scrapy.http import Request
from time import sleep
from ..utils import MongoDB, getRedisConnection
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class SteamSpider(scrapy.Spider):
    name = "archive_csgo"
    allowed_domains = ["163.com"]

    start_urls = [
        f"https://buff.163.com"]
    custom_settings = {
        "ITEM_PIPELINES": {
            # 'TanZhengSpider.pipelines.DefaultPipeline': 300,
        },

    }
    collection = 'buff_csgo'
    collections = {
        'buff_csgo':
            {
                'item_id': 'item_id',
                'name': 'name',
                'price': 'quick_price',
                'sell_num': 'sell_num',
                'sell_min_price': 'sell_min_price',
                'buy_max_price': 'buy_max_price',
                'buy_num': 'buy_num'
            }
        ,
        'uuyp_csgo':
            {
                'item_id': 'item_id',
                'name': 'CommodityName',
                'price': 'Price',
                'sell_num': 'OnSaleCount',
                'lease_deposit': 'LeaseDeposit',
                'long_lease_price': 'LongLeaseUnitPrice',
                'lease_price': 'LeaseUnitPrice',
                'lease_num': 'OnLeaseCount',
                'rent': 'Rent'
            },
        'steam_csgo':
            {
                'item_id': 'item_id',
                'name': 'name',
                'price': 'sell_price',
                'sell_num': 'sell_listings',
                'sell_min_price': 'sale_price',

            },
        'c5_csgo':
            {
                'item_id': 'item_id',
                'name': 'itemName',
                'price': 'cnyPrice',
                'sell_num': 'quantity',
                'sell_min_price': 'cnyPrice',

            }
        ,
        'igxe_csgo':
            {
                'item_id': 'item_id',
                'name': 'market_name',
                'price': 'reference_price',
                'sell_num': 'sale_count',
                'sell_min_price': 'ags_manual_min_price',
                'buy_max_price': 'purchase_max_price',
                'buy_num': 'purchase_count',
                'lease_deposit': 'lease_sale_count',
                'long_lease_price': 'lease_min_price',
                'lease_num': 'lease_min_short_price'

            }
    }

    def parse(self, response):
        try:
            DB = MongoDB(self.collection, database=settings.get('MONGODB_DB'), host=settings.get('MONGODB_HOST'),
                         port=settings.get('MONGODB_PORT'), username=settings.get('MONGODB_USER'),
                         password=settings.get('MONGODB_PSW'), authSource=settings.get('MONGODB_AUTHSOURCE'))
            DB.archive(self.collections, self.logger)
            # r = getRedisConnection(settings.get('REDIS_HOST'), settings.get('REDIS_PORT'), settings.get('REDIS_PSW'),
            #                        settings.get('REDIS_DB'))
            # for i in self.collections:
            #     data = {j.get('item_id'): j.get(self.collections.get(i).get('price')) for j in DB.database[i+"_archive"].find({})}
            #     r.hmset(i, data)
        except Exception as e:
            self.logger.error(f"msg:异常{e}")
