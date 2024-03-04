import scrapy
from scrapy.http import Request
from time import sleep
from math import ceil
import requests
from lxml import etree
class SteamSpider(scrapy.Spider):
    name = "steam_csgo"
    allowed_domains = ["steamcommunity.com"]
    pagesize = 100
    page = 1
    collection = 'steam_csgo'
    game = 730
    column = 'hash_name'
    USD2CNY=None
    start_urls = [
        f"https://steamcommunity.com/market/search/render/?query=&start={(page - 1) * pagesize}&count={pagesize}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid={game}&norender=1"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'TanZhengSpider.pipelines.DefaultPipeline': 300,
        },

        "DEFAULT_REQUEST_HEADERS": {
            'Accept': 'application/json',
            'Cookie': 'timezoneOffset=28800,0; browserid=2918958891933564199; sessionid=4519ade0c66f30f4c7c0c541; steamCountry=HK%7C47ecf4469157e9f83687510744f179a0; steamLoginSecure=76561198979917651%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MERFMV8yMzk5NTQ0QV9FRDY0MiIsICJzdWIiOiAiNzY1NjExOTg5Nzk5MTc2NTEiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MDYyNjEyMjMsICJuYmYiOiAxNjk3NTM0NDgyLCAiaWF0IjogMTcwNjE3NDQ4MiwgImp0aSI6ICIwRTNCXzIzRDlFRjg2XzU0NDZBIiwgIm9hdCI6IDE3MDE5NDI5MzQsICJydF9leHAiOiAxNzE5Nzk3MTgyLCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiMTAxLjQ0LjgxLjEwNSIsICJpcF9jb25maXJtZXIiOiAiMTA2LjgzLjAuMTA4IiB9.owwJLGynqe3v3qUxvi9ivziZ_Eam4QPWHTXY48fRS0TqyVdATdDxr04Hagyts0r2QZ_G5Cb-an-hIlV-UDbJCQ; webTradeEligibility=%7B%22allowed%22%3A1%2C%22allowed_at_time%22%3A0%2C%22steamguard_required_days%22%3A15%2C%22new_device_cooldown_days%22%3A0%2C%22time_checked%22%3A1706174483%7D',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Mobile Safari/537.36',
        },
        "DOWNLOAD_DELAY": 5,

    }
    def getUSD2CNY(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        }
        url = "https://www.xe.com/zh-CN/currencyconverter/convert/?Amount=1&From=USD&To=CNY"
        response = requests.get(url, headers=headers)
        TREE = etree.HTML(response.text)
        self.USD2CNY=float(''.join(TREE.xpath('//*[@class="result__BigRate-sc-1bsijpp-1 dPdXSB"]//text()')[:2]))

    def parse(self, response):
        try:
            if not self.USD2CNY:
                self.getUSD2CNY()

            self.logger.info(f"USD2CNY:{self.USD2CNY}")
            print(f"USD2CNY:{self.USD2CNY}")
            datas = response.json().get('results', [])
            self.total_page = ceil(int(response.json().get('total_count', 0)) / self.pagesize)
            self.logger.info(f'msg:爬取开始{self.page}/{self.total_page},spider:{self.collection},url:{response.url}')
            if datas:
                for data in datas:
                    data['sell_price']=round(float(data.get('sell_price',0)/100)*self.USD2CNY,2)
                    data['asset_description']['icon_url']='https://steamcommunity-a.akamaihd.net/economy/image/'+data['asset_description']['icon_url']
                    yield data
            else:
                self.logger.error(f"msg:数据为空,spider:{self.collection},url:{response.url},resp:{response.json()}")
            self.logger.info(f'msg:爬取成功{self.page}/{self.total_page},spider:{self.collection},url:{response.url}')
            if self.page < self.total_page:
                self.page += 1
                yield Request(
                    f'https://steamcommunity.com/market/search/render/?query=&start={(self.page - 1) * self.pagesize}&count={self.pagesize}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid={self.game}&norender=1',
                    callback=self.parse, dont_filter=True)
        except Exception as e:
            self.logger.error(f"msg:请求异常{e},spider:{self.collection},url:{response.url},resp:{response.json()}")
            sleep(60)
            yield Request(
                f'https://steamcommunity.com/market/search/render/?query=&start={(self.page - 1) * self.pagesize}&count={self.pagesize}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid={self.game}&norender=1',
                callback=self.parse, dont_filter=True)
