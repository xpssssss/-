import requests
import re
import json


def start():
    for w in range(0, 1600, 32):
        try:
            url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/1?' \
                  'uuid=xxx&userid=-1&' \
                  'limit=32&' \
                  'offset='+str(w)+'&cateId=-1&q=%E7%81%AB%E9%94%85'
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
            }
            response = requests.get(url, headers=headers)
            titles = re.findall('","title":"(.*?)","address":"', response.text)
            addresses = re.findall(',"address":"(.*?)",', response.text)
            avgprices = re.findall(',"avgprice":(.*?),', response.text)
            avgscores = re.findall(',"avgscore":(.*?),',response.text)
            comments = re.findall(',"comments":(.*?),',response.text)
            print(len(titles), len(addresses), len(avgprices), len(avgscores), len(comments))
            for o in range(len(titles)):
                title = titles[o]
                address = addresses[o]
                avgprice = avgprices[o]
                avgscore = avgscores[o]
                comment = comments[o]
                #写入本地文件
                file_data(title, address, avgprice, avgscore, comment)

        except:
            continue

#文件写入方法
def file_data(title, address, avgprice, avgscore, comment):
    data = {
        '店铺名称': title,
        '店铺地址': address,
        '平均消费价格': avgprice,
        '店铺评分': avgscore,
        '评价人数': comment
    }
    with open('美团美食.txt', 'a', encoding='utf-8')as fb:
        fb.write(json.dumps(data, ensure_ascii=False) + '\n')
        #ensure_ascii=False必须加因为json.dumps方法不关闭转码会导致出现乱码情况

if __name__ == '__main__':
    start()
