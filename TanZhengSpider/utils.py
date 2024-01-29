import pymongo, datetime
import hashlib
import requests

class MongoDB:
    def __init__(self, collection, database, host, port, username,
                 password, authSource):
        self.client = pymongo.MongoClient(host=host, port=port, username=username, password=password,
                                          authSource=authSource)
        self.database = self.client[database]
        self.col = self.database[collection]

    def get_valid_item_ids(self):
        return set([item["item_id"] for item in self.col.find()])

    def get_item(self, buff_id):
        res = self.col.find({"item_id": buff_id})
        if len(list(res.clone())):
            return res[0]
        else:
            return None

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
        res = self.col.replace_one({"item_id": item["item_id"]}, item, upsert=True)
        return res.acknowledged

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
def uuyp_login(username,password):


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
    print(json_data,response.json())
    return response.json().get('Data',{}).get('Token')