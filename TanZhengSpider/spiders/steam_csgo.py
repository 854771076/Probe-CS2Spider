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
        f"https://steamcommunity.com/market/search/render/?query=&start={(page - 1) * pagesize}&count={pagesize}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid={game}&norender=1&country=HK"]
    custom_settings = {
        "ITEM_PIPELINES": {
            'TanZhengSpider.pipelines.DefaultPipeline': 300,
        },

        "DEFAULT_REQUEST_HEADERS": {
             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                # Requests sorts cookies= alphabetically
                # 'Cookie': 'timezoneOffset=28800,0; browserid=2918958891933564199; steamLoginSecure=76561198979917651%7C%7CeyAidHlwIjogIkpXVCIsICJhbGciOiAiRWREU0EiIH0.eyAiaXNzIjogInI6MERFMV8yMzk5NTQ0QV9FRDY0MiIsICJzdWIiOiAiNzY1NjExOTg5Nzk5MTc2NTEiLCAiYXVkIjogWyAid2ViOmNvbW11bml0eSIgXSwgImV4cCI6IDE3MDk1NjQyNDksICJuYmYiOiAxNzAwODM2NDcwLCAiaWF0IjogMTcwOTQ3NjQ3MCwgImp0aSI6ICIwRUM4XzI0MDgxOEM1XzBCRTZFIiwgIm9hdCI6IDE3MDE5NDI5MzQsICJydF9leHAiOiAxNzE5Nzk3MTgyLCAicGVyIjogMCwgImlwX3N1YmplY3QiOiAiMTAxLjQ0LjgxLjEwNSIsICJpcF9jb25maXJtZXIiOiAiMTA2LjgzLjAuMTA4IiB9.q3Cp4z2EqXfHBTE_BXOj2LDYCd3UySnbyMQ_7dbbHQj0USh8VR_VPRGIbYkWKMoZYDZQuafcFn_WitjwrYvsDw; strInventoryLastContext=753_6; sessionid=0c36cebe0f73bc66f0188662',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
                'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
        },
        "DOWNLOAD_DELAY": 15,

    }
    def getUSD2CNY(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
        }
        url = "https://www.xe.com/zh-CN/currencyconverter/convert/?Amount=1&From=USD&To=CNY"
        response = requests.get(url, headers=headers)
        TREE = etree.HTML(response.text)
        self.USD2CNY=float(''.join(TREE.xpath('/html/body/div[1]/div[4]/div[2]/section/div[2]/div/main/div/div[2]/div[1]/div/p[2]//text()')[:2]))

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
                    data['sale_price'] = round((float(data.get('sale_price_text', '').split(' ')[0].replace("$",'').replace(",",'')) ) * self.USD2CNY, 2)
                    data['asset_description']['icon_url']='https://steamcommunity-a.akamaihd.net/economy/image/'+data['asset_description']['icon_url']
                    yield data
            else:
                self.logger.error(f"msg:数据为空,spider:{self.collection},url:{response.url},resp:{response.json()}")
            self.logger.info(f'msg:爬取成功{self.page}/{self.total_page},spider:{self.collection},url:{response.url}')
            if self.page < self.total_page:
                self.page += 1
                yield Request(
                    f'https://steamcommunity.com/market/search/render/?query=&start={(self.page - 1) * self.pagesize}&count={self.pagesize}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid={self.game}&norender=1&country=HK',
                    callback=self.parse, dont_filter=True)
        except Exception as e:
            self.logger.error(f"msg:请求异常{e},spider:{self.collection},url:{response.url},resp:{response.json()}")
            sleep(60)
            yield Request(
                f'https://steamcommunity.com/market/search/render/?query=&start={(self.page - 1) * self.pagesize}&count={self.pagesize}&search_descriptions=0&sort_column=popular&sort_dir=desc&appid={self.game}&norender=1&country=HK',
                callback=self.parse, dont_filter=True)
