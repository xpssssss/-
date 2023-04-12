import requests
import json

base_url = 'https://bj.meituan.com/ptapi/recommends?limit=10'



uuid = "cf32f91085b44b87955c.1679756420.1.0.0" # 你的uuid，登录后在开发者模式获取
userid = "3682664218" # 你的userid，登录后在开发者模式获取

key = '大盘鸡'

page = 1
# 设置请求参数
parameters = {
    'uuid': uuid, # 你的uuid，登录后在开发者模式获取
    'userid': userid, # 你的userid，登录后在开发者模式获取
    'limit':32, # 每页的 店铺信息数
    'offset':32*(page - 1), # 当前 偏移量，第1页为0，第2页为 (2-1)*limit
    'cateId':-1, #
    'q': key, # 搜索的关键字
    }
# 设置请求头
header = {
    "Accept-Encoding": "Gzip",  # 使用gzip压缩传输数据让访问更快
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0",
    }

re = requests.get(base_url, headers = header, params=parameters)

text = re.text
# 由于是json格式的字符串，用json.load()方法格式化
print(text)
js = json.loads(text)  #<class 'list'>返回一个字典


# 需要用到的数据在 js['data']中
# data = js['data']
# searchResult = data['searchResult'] # 结果列表

