import requests
from pprint import pprint
import csv

# 创建文件
f = open('烤肉.csv', mode='a', encoding='utf-8', newline='')
csv_writer = csv.DictWriter(f, fieldnames=[
    '店名',
    '评分',
    '评论',
    '店铺类型',
    '商圈',
    '人均',
    '最低消费',
    '经度',
    '纬度',
    '详情页',
])
csv_writer.writeheader()

url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/70?uuid=1191c166b23545adaef7.1679637144.1.0.0&userid=266252179&limit=32&offset=32&cateId=-1&q=%E7%83%A4%E8%82%89&token=AgEcI8MGJ-mKhr9oT4VY_zjPV_oFYDXfbo9sEAaWhz5Ud0ZxeKhBNbm--AOvOEMZfMX1X8atA5u22QAAAABsFwAA631DsS1KNwy05foi_83hOjAmFHyzNkrbtWhFRpR9MOAObuDNmNMpKOe8SdRaRJ_n'

headers = {
    'Referer': 'https://chs.meituan.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36'
}

response = requests.get(url=url, headers=headers)
print(response)
pprint(index)
 # for循环遍历, 把列表里面元素一个一个提取出来
for index in response.json()['data']['searchResult']:
    # 详情页
    link = f'https://www.meituan.com/meishi/{index["id"]}/'
    dit = {
        '店名': index['title'],
        '评分': index['avgscore'],
        '评论': index['comments'],
        '店铺类型': index['backCateName'],
        '商圈': index['areaname'],
        '人均': index['avgprice'],
        '最低消费': index['lowestprice'],
        '经度': index['longitude'],
        '纬度': index['latitude'],
        '详情页': link,
    }
    csv_writer.writerow(dit)
    print(dit1\
          12