import scrapy
from scrapy.http import Request
from time import sleep
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class SteamSpider(scrapy.Spider):
    name = "buff_csgo"
    allowed_domains = ["163.com"]
    pagesize = 80
    page = 1
    collection = 'buff_csgo'
    game = 730
    column = 'market_hash_name'
    start_urls = [
        f"https://buff.163.com/api/market/goods?page_num={page}&page_size={pagesize}&appid={game}"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'TanZhengSpider.pipelines.DefaultPipeline': 300,
        },

        "DEFAULT_REQUEST_HEADERS": settings.get('BUFF_COOKIES'),
        "DOWNLOAD_DELAY": 30,

    }

    def parse(self, response):
        try:
            datas = response.json().get('data', {}).get('items', [])
            self.total_page = int(response.json().get('data', {}).get('total_page', 0))
            if self.total_page==0:
                self.logger.error(f"msg:cookie失效,spider:{self.collection},url:{response.url},resp:{response.json()}")
                return
            self.logger.info(f'msg:爬取开始{self.page}/{self.total_page},spider:{self.collection},url:{response.url}')
            if datas:
                for data in datas:
                    yield data
            else:
                self.logger.error(f"msg:数据为空,spider:{self.collection},url:{response.url},resp:{response.json()}")
            self.logger.info(f'msg:爬取成功{self.page}/{self.total_page},spider:{self.collection},url:{response.url}')
            if self.page < self.total_page:
                self.page += 1
                yield Request(
                    f'https://buff.163.com/api/market/goods?page_num={self.page}&page_size={self.pagesize}&appid={self.game}',
                    callback=self.parse, dont_filter=True)
        except Exception as e:
            self.logger.error(f"msg:请求异常{e},spider:{self.collection},url:{response.url},resp:{response.json()}")
            sleep(60)
            yield Request(
                f'https://buff.163.com/api/market/goods?page_num={self.page}&page_size={self.pagesize}&appid={self.game}',
                callback=self.parse, dont_filter=True)
