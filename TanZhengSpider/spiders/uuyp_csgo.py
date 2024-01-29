import scrapy
from scrapy.http import Request
from time import sleep
from math import ceil
import json
from ..utils import uuyp_login
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class SteamSpider(scrapy.Spider):
    name = "uuyp_csgo"
    allowed_domains = ["youpin898.com"]
    pagesize = 100
    page = 1
    collection = 'uuyp_csgo'
    game = 730
    column = 'CommodityHashName'
    types = ["CSGO_Type_Knife", "CSGO_Type_Pistol", "CSGO_Type_Rifle", "CSGO_Type_SMG", "CSGO_Type_Shotgun",
             "CSGO_Type_Machinegun", "Type_Hands", "Other", "CSGO_Tool_Sticker"]
    type_id = 0
    start_urls = [
        f"https://api.youpin898.com/api/homepage/new/es/template/GetCsGoPagedList"]
    headers={
        'Host': 'api.youpin898.com',
        'api-version': '1.0',
        'devicetoken': 'ZbISDDmnxKoDAPbqsU4D8Z4T',
        'deviceid': 'ZbISDDmnxKoDAPbqsU4D8Z4T',
        'requesttag': '6FF91C311B14109AA9C60CBCBED3AE4E',
        'devicetype': '3',
        'platform': 'android',
        'package-type': 'uuyp',
        'app-version': '5.12.1',
        'device-info': '{"deviceId":"ZbISDDmnxKoDAPbqsU4D8Z4T","deviceType":"V2218A","hasSteamApp":0,"requestTag":"6FF91C311B14109AA9C60CBCBED3AE4E","systemName ":"Android","systemVersion":"12"}',
        'apptype': '7',
        'authorization': uuyp_login(settings.get('UUYP_USERNAME'),settings.get('UUYP_PASSWORD')),
        'content-type': 'application/json; charset=utf-8',
        'user-agent': 'okhttp/3.14.9',
    }
    custom_settings = {
        "ITEM_PIPELINES": {
            'TanZhengSpider.pipelines.DefaultPipeline': 300,
        },
        "DOWNLOAD_DELAY": 10,

    }

    def start_requests(self):
        url = self.start_urls[0]
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
        yield scrapy.Request(url=url, method='POST', body=json_data, callback=self.parse,headers=self.headers)
    def refrash_token(self):
        self.headers = {
            'Host': 'api.youpin898.com',
            'api-version': '1.0',
            'devicetoken': 'ZbISDDmnxKoDAPbqsU4D8Z4T',
            'deviceid': 'ZbISDDmnxKoDAPbqsU4D8Z4T',
            'requesttag': '6FF91C311B14109AA9C60CBCBED3AE4E',
            'devicetype': '3',
            'platform': 'android',
            'package-type': 'uuyp',
            'app-version': '5.12.1',
            'device-info': '{"deviceId":"ZbISDDmnxKoDAPbqsU4D8Z4T","deviceType":"V2218A","hasSteamApp":0,"requestTag":"6FF91C311B14109AA9C60CBCBED3AE4E","systemName ":"Android","systemVersion":"12"}',
            'apptype': '7',
            'authorization': uuyp_login(settings.get('UUYP_USERNAME'), settings.get('UUYP_PASSWORD')),
            'content-type': 'application/json; charset=utf-8',
            'user-agent': 'okhttp/3.14.9',
        }
    def parse(self, response):
        try:
            datas = response.json().get('Data', [])
            self.total_page = ceil(int(response.json().get('TotalCount', 0)) / self.pagesize)
            self.logger.info(
                f'msg:{self.types[self.type_id]}爬取开始{self.page}/{self.total_page},spider:{self.collection},url:{response.url}')
            if datas:
                for data in datas:
                    yield data
            else:
                self.logger.error(
                    f"msg:{self.types[self.type_id]}数据为空,spider:{self.collection},url:{response.url},resp:{response.json()}")
                headers={

                }
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
                self.refrash_token()
                yield Request(
                    self.start_urls[0], method='POST', body=json_data,
                    callback=self.parse, dont_filter=True,headers=self.headers)

            self.logger.info(
                f'msg:{self.types[self.type_id]}爬取成功{self.page}/{self.total_page},spider:{self.collection},url:{response.url}')
            if self.page < self.total_page:
                self.page += 1
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
                    self.start_urls[0], method='POST', body=json_data,
                    callback=self.parse, dont_filter=True,headers=self.headers)
            elif self.page >= self.total_page and self.type_id < len(self.types) - 1:
                self.page = 1
                self.type_id += 1
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
                    self.start_urls[0], method='POST', body=json_data,
                    callback=self.parse, dont_filter=True,headers=self.headers)

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
            self.refrash_token()
            yield Request(
                self.start_urls[0], method='POST', body=json_data,
                callback=self.parse, dont_filter=True,headers=self.headers)
