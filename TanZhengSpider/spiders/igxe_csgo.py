import scrapy
from scrapy.http import Request
from time import sleep
from math import ceil


class SteamSpider(scrapy.Spider):
    name = "igxe_csgo"
    allowed_domains = ["igxe.cn"]
    pagesize = 20000
    page = 1
    collection = 'igxe_csgo'
    game = 730
    column = 'market_hash_name'
    start_urls = [
        f"https://www.igxe.cn/api/v2/product/search/730?page_size={pagesize}&page_no={page}&app_id={game}"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'TanZhengSpider.pipelines.DefaultPipeline': 300,
        },

        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Client-Type': 'web',
            'Connection': 'keep-alive',
            'Pragma': 'no-cache',
            'Random-String': 'd5b9e02bf792b38a800fcae43dea389b',
            'Referer': 'https://www.igxe.cn/market/csgo?quality_id=614&page_no=3&page_size=20',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'Timestamp': '3412986096',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'X-Requested-with': 'XMLHttpRequest',
            'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        },
        "DOWNLOAD_DELAY": 10,

    }

    def parse(self, response):
        try:
            datas = response.json().get('data', {}).get('data',[])
            self.total_page = int(response.json().get('data',{}).get('page',{}).get('page_count',1))
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
                    f"https://www.igxe.cn/api/v2/product/search/730?page_size={self.pagesize}&page_no={self.page}&app_id={self.game}",
                    callback=self.parse, dont_filter=True)
        except Exception as e:
            self.logger.error(f"msg:请求异常{e},spider:{self.collection},url:{response.url}")
            sleep(60)
            yield Request(
                f"https://www.igxe.cn/api/v2/product/search/730?page_size={self.pagesize}&page_no={self.page}&app_id={self.game}",
                callback=self.parse, dont_filter=True)
