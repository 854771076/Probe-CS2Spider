import pymongo, datetime
import hashlib
import requests
import pymongo,datetime


class MongoDB:
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

    def __init__(self, collection, database, host, port, username,
                 password, authSource):
        self.client = pymongo.MongoClient(host=host, port=port, username=username, password=password,
                                          authSource=authSource)
        self.database = self.client[database]
        self.col = self.database[collection]
        self.write_list = []

    def get_valid_item_ids(self):
        return set([item["item_id"] for item in self.col.find()])

    def get_item(self, buff_id):
        res = self.col.find({"item_id": buff_id})
        if len(list(res.clone())):
            return res[0]
        else:
            return None

    def archive(self, collections: dict, logger=None):
        time = datetime.datetime.today()
        target_date = time - datetime.timedelta(days=365)
        for key in collections.keys():
            logger.info(f'msg:开始归档,collection:{key}_archive,time:{time.date()}')
            deleted_count = self.database[f'{key}_archive'].delete_many(
                {'archive_time': {'$lt': str(target_date.date())}}).deleted_count
            logger.info(f'msg:开始删档,collection:{key}_archive,count:{deleted_count},time:{target_date.date()}')
            data_list = []
            column_old = list(collections.get(key).values())
            column_new = list(collections.get(key).keys())
            for data in self.database[key].find({}, {i: 1 for i in column_old}):
                data.pop("_id")
                for j in range(len(column_old)):


                    data[column_new[j]] = 0 if not data.get(column_old[j]) else data.get(column_old[j])
                data['archive_time'] = str(time.date())
                data['source'] = key
                data_list.append(data)
            count = len(self.database[f'{key}_archive'].insert_many(data_list).inserted_ids)
            logger.info(f'msg:归档成功,collection:{key}_archive,count:{count},time:{time.date()}')

    def insert_item(self, item):

        res = self.col.insert_one(item)
        return res.acknowledged

    def delete_item(self, buff_id):
        res = self.col.delete_one({"item_id": buff_id})
        return res.acknowledged

    def update_item(self, item, column):
        # 创建 MD5 对象
        md5 = hashlib.md5()
        # 更新 MD5 对象以处理要加密的字符串
        md5.update(item[column].encode('utf-8'))
        # 获取加密后的结果
        md5_str = md5.hexdigest()
        item["item_id"] = md5_str
        item['update_time'] = datetime.datetime.now()
        self.write_list.append(pymongo.UpdateOne({"item_id": item["item_id"]}, {"$set": item}, upsert=True))

    def submit(self):
        self.col.bulk_write(self.write_list)

    def get_all_items(self, rule=None):
        if rule is None:
            rule = {}
        return self.col.find(rule)

    def get_sorted_items(self, sort, rule=None, limit=0):
        if rule is None:
            rule = {}
        return self.col.find(rule).sort(sort, pymongo.ASCENDING).limit(limit)

    def close(self):
        self.client.close()

    def _clear(self):
        return self.col.delete_many({})

    def get_size(self):
        return self.col.estimated_document_count()
    def price_contrast_1day(self, col,item_id, logger=None):
        if col in self.collections.keys():
            time = datetime.datetime.today()
            data1=self.database[col+'_archive'].find_one({'archive_time':str(time.date()),'item_id':item_id})
            data2=self.database[col].find_one({'item_id':item_id})
            price1=float(data1.get('price') if data1.get('price') else 0)
            price2=float(data2.get(self.collections[col]['price']) if data2.get(self.collections[col]['price']) else 0)
            price3=round((price2-price1)/price1,4)
            return price3>0,price3,f'{price3*100}%'
        else:
            logger.error(f'没有集合:{col}')
            return False,0


def uuyp_login(username, password):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',

    }

    json_data = {
        'UserName': username,
        'UserPwd': password,
        'SessionId': '',
        'Code': '',
        'TenDay': 1,
    }

    response = requests.post('https://api.youpin898.com/api/user/Auth/PwdSignIn', headers=headers, json=json_data)
    return response.json().get('Data', {}).get('Token')
