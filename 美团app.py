# https://bj.meituan.com/
import requests
import re
from bs4 import BeautifulSoup
import json
from urllib.request import urlopen, quote
import pandas as pd
import numpy as np
from pylab import *


def getHTMLText(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36",
        "Cookie": "__mta=20871943.1625705574088.1625810520459.1625813097008.16; _lxsdk_cuid=17a839a3528c8-070f1da58fbd21-6373264-144000-17a839a3529c8; ci=1; rvct=1; mtcdn=K; uuid=5226c694e07949bdb828.1625725143.1.0.0; mt_c_token=xR1aknv_B8Yiio_ZWzUmVSFo2koAAAAACw4AAIkyH5SSt867G_XkxBIcCNINlemXinZVHTQDkWGAFQukS3HrBbqc_BktISzd7MhPvw; lsu=; iuuid=C72B4FEF3403F5A0924DEFB4DF9C9FFEC17E5FC35B2B4D6CF55632ABF4817904; isid=xR1aknv_B8Yiio_ZWzUmVSFo2koAAAAACw4AAIkyH5SSt867G_XkxBIcCNINlemXinZVHTQDkWGAFQukS3HrBbqc_BktISzd7MhPvw; logintype=normal; cityname=%E5%8C%97%E4%BA%AC; _lxsdk=C72B4FEF3403F5A0924DEFB4DF9C9FFEC17E5FC35B2B4D6CF55632ABF4817904; webp=1; i_extend=H__a100002__b1; latlng=39.830516,116.290895,1625725257685; __utma=74597006.798321478.1625725258.1625725258.1625725258.1; __utmz=74597006.1625725258.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; lt=fYaN6SmjIjuKuNSbDGgqCDbdjQgAAAAACw4AABKyZyfS3ZbSub8odXTK9CKxaHAOvtIkpz464sfHyJcIfPPYbpw2Vh_Rnd3Mr5B24A; u=583093909; n=%E9%A5%95%E9%A4%AEzzzzz; token2=fYaN6SmjIjuKuNSbDGgqCDbdjQgAAAAACw4AABKyZyfS3ZbSub8odXTK9CKxaHAOvtIkpz464sfHyJcIfPPYbpw2Vh_Rnd3Mr5B24A; unc=%E9%A5%95%E9%A4%AEzzzzz; __mta=20871943.1625705574088.1625810319319.1625810340857.13; firstTime=1625813095796; _lxsdk_s=17a89d8b4fc-08e-6c7-641%7C%7C48"}
    try:
        r = requests.get(url, headers=headers, timeout=100)
        r.raise_for_status()
        r.encoding = r.apparent_encoding  # 对文本中使用的编码替换整体的编码
        return r.text
    except:
        return "失败"


# 将数据写入csv文件中
def file_data(title, address, avgprice, avgscore, comment):
    data = {
        '店铺名称': title,
        '店铺地址': address,
        '平均消费价格': avgprice,
        '店铺评分': avgscore,
        '评价人数': comment
    }
    with open('..美团大盘鸡店铺数据4.csv', 'a', encoding='utf-8-sig') as fb:
        fb.write(json.dumps(data, ensure_ascii=False) + '\n')


def main():
    goods = '大盘鸡'  # 检索词
    depth = 49  # 设置爬取的深度，一共50页
    start_url = 'https://bj.meituan.com/s/' + goods

    # 以下采用for循环对每个页面URL进行访问
    i = 0
    for i in range(depth):
        try:
            url = start_url + '&offset=' + str(32 * i)
            # url = start_url +  str(32*i)
            html = getHTMLText(url)
            titles = re.findall('","title":"(.*?)","address":"', html)
            addresses = re.findall(',"address":"(.*?)",', html)
            avgprices = re.findall(',"avgprice":(.*?),', html)
            avgscores = re.findall(',"avgscore":(.*?),', html)
            comments = re.findall(',"comments":(.*?),', html)

            print(titles)
            print(addresses)
            print(avgprices)
            print(avgscores)
            print(comments)
            # 输出当前返回数据的长度
            print(len(titles), len(addresses), len(avgprices), len(avgscores), len(comments))
            # 将每个店铺的信息通过循环写入文件
            for j in range(len(titles)):
                title = titles[j]
                address = addresses[j]
                avgprice = avgprices[j]
                avgscore = avgscores[j]
                comment = comments[j]
                # file_data(title,address,avgprice,avgscore,comment)

        except:
            continue
    # printGoodsList(infoList)


main()