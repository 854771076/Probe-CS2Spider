import scrapy
from scrapy.http import Request
from time import sleep
from math import ceil
import json


class SteamSpider(scrapy.Spider):
    name = "c5_csgo"
    allowed_domains = ["c5game.com"]
    pagesize = 500
    page = 1
    collection = 'c5_csgo'
    game = 730
    column = 'marketHashName'
    types = ["CSGO_Type_Knife", "CSGO_Type_Pistol", "CSGO_Type_Rifle", "CSGO_Type_SMG", "CSGO_Type_Shotgun",
             "CSGO_Type_Machinegun", "Type_Hands", "CSGO_Type_Other", "CSGO_Tool_Sticker"]
    type_id = 0
    start_urls = [
        f"https://www.c5game.com/napi/trade/search/v2/items/730/search?limit={pagesize}&appId={game}&page={page}&sort=0&type={types[0]}"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'TanZhengSpider.pipelines.DefaultPipeline': 300,
        },

        "DEFAULT_REQUEST_HEADERS": {
            'Referer': 'https://www.c5game.com/csgo?appId=730&page=1&limit=42&sort=0&type=CSGO_Tool_Sticker',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
        },
        "DOWNLOAD_DELAY": 10,

    }



    def parse(self, response):
        try:
            datas = response.json().get('data', {}).get('list',[])
            self.total_page = int(response.json().get('data', {}).get('pages', 0))
            self.logger.info(
                f'msg:{self.types[self.type_id]}爬取开始{self.page}/{self.total_page},spider:{self.collection},url:{response.url}')
            if datas:
                for data in datas:
                    yield data
            else:
                self.logger.error(
                    f"msg:{self.types[self.type_id]}数据为空,spider:{self.collection},url:{response.url},resp:{response.json()}")
            self.logger.info(
                f'msg:{self.types[self.type_id]}爬取成功{self.page}/{self.total_page},spider:{self.collection},url:{response.url}')
            if self.page < self.total_page:
                self.page += 1

                yield Request(
                    f'https://www.c5game.com/napi/trade/search/v2/items/730/search?limit={self.pagesize}&appId={self.game}&page={self.page}&sort=0&type={self.types[self.type_id]}',
                    callback=self.parse, dont_filter=True)
            elif self.page >= self.total_page and self.type_id < len(self.types) - 1:
                self.page = 1
                self.type_id += 1

                yield Request(
                    f'https://www.c5game.com/napi/trade/search/v2/items/730/search?limit={self.pagesize}&appId={self.game}&page={self.page}&sort=0&type={self.types[self.type_id]}',
                    callback=self.parse, dont_filter=True)

        except Exception as e:
            self.logger.error(
                f"msg:{self.types[self.type_id]}请求异常{e},spider:{self.collection},url:{response.url},resp:{response.json()}")
            sleep(60)
            d = {
                "filterMap": {
                    "Type": [f"{self.types[self.type_id]}_Unlimited"]
                },
                "gameId": self.game,
                "listSortType": 0,
                "listType": 10,
                "pageIndex": self.page,
                "pageSize": self.pagesize,
                "sortType": 0,
                "stickerAbrade": 0,
                "stickersIsSort": False,
            }
            json_data = json.dumps(d)
            yield Request(
                f'https://www.c5game.com/napi/trade/search/v2/items/730/search?limit={self.pagesize}&appId={self.game}&page={self.page}&sort=0&type={self.types[self.type_id]}',
                callback=self.parse, dont_filter=True)
