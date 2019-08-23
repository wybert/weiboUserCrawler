#coding:utf-8
import urllib
import urllib2
# import re
import time
# from lxml import etree
from bs4 import BeautifulSoup
SLEEP_FLAG = 1
SLEEP_INTERVAL = 30
import pandas as pd
import random


HEADERS = {'User-Agent': '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36''',
           'Host': 'weibo.cn',
           "cookie": r'''_T_WM=8c43747cae5b063e1534ee86277a6c02; ALF=1569072160; SCF=AkCVman8hkFsJhzV0gu6LcTc6bbP0OT-495b7-fe84otRY2H2h23z2XNCFb4RFnhWvHt9nW6ZXGIoeXeoooQ058.; SUB=_2A25wWudyDeRhGeBN6VYT9CvFzTyIHXVTpIk6rDV6PUNbktBeLXP9kW1NRJrTH2VP8FBAdV924w1XIYLj3KEmvPhy; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5sOEfKX.m6y77jN34pRfbj5JpX5KzhUgL.Foq0eoBESh-4So52dJLoIpySqPL.qP.LxK-LBKBLBKMLxKnLBo2LBK2t; SUHB=0TPFT12oshoIox; SSOLoginState=1566480162'''}

# proxy = {'http': '127.0.0.1:1080'}
# proxy_support = urllib2.ProxyHandler(proxy)
# opener = urllib2.build_opener(proxy_support)
# urllib2.install_opener(opener)



def Parseurl(url):

    req = urllib2.Request(url, headers=HEADERS)
    try:
        
        resp = urllib2.urlopen(req, timeout=12)
        result = resp.read()
        return result
    except Exception,e:
        print e
        print "Error Open %s" % str(url)
        # time.sleep(5)
        return 'None'

## parse one weibo 

def parse_one_weibo(weibo_div):

    one_weibo = {}
    # weibo text
    span = weibo_div.find("span", {"class":"ctt"})
    weibo_text = span.text 
    one_weibo["text"] = weibo_text
    # time 

    span = weibo_div.find("span", {"class": "ct"})
    weibo_time = span.text
    one_weibo["time"] = weibo_time

    # weibo 

    a = weibo_div.findAll("a")

    one_weibo["image_url"] = u"#_#"

    for item in a:
        # print "------"
        # print item.text
        text = item.text

        if u"原图" in text:
            one_weibo["image_url"] = item["href"]
        if u"赞[" in text:
            one_weibo["thumb"] = text.split("[")[-1].strip("]")
        if u"转发[" in text:
            one_weibo["repost"] = text.split("[")[-1].strip("]")
        if u"评论[" in text:
            one_weibo["comment"] = text.split("[")[-1].strip("]")
    return one_weibo

def parse_page_num(soup):

    page_num_div = soup.findAll("div", {"class": "pa"})[0]
    page_num = int(page_num_div.find("input", {"name": "mp"})["value"])
    return page_num

# print one_weibo

def get_page_num(user_name):

    url = "https://weibo.cn/%s?filter=1&page=%d" % (user_name, 1)
    html = Parseurl(url)
    soup = BeautifulSoup(html, "lxml")
    page_num = parse_page_num(soup)
    #         #设置随机休眠时间
    sleeptime_one = random.randint(SLEEP_INTERVAL-10, SLEEP_INTERVAL + 10)
    time.sleep(sleeptime_one)

    return page_num

# -------------------------------------------------------------------------------------------




user_name = "uktimes"

page_num = get_page_num(user_name)


## start page from  here....

start = 1

for i in range(page_num):

    if i+1 < start:
        continue
    print "page ", i+1, "/", page_num


    url = "https://weibo.cn/%s?filter=1&page=%d" % (user_name, i+1)
    html = Parseurl(url)
    soup = BeautifulSoup(html, "lxml")
    ## one page weibos
    weibo_divs = soup.findAll("div", {"class": "c"})[1:-2]

    weibos = []
    for weibo_div in weibo_divs:
        one_weibo = parse_one_weibo(weibo_div)
        weibos.append(one_weibo)
#         #设置随机休眠时间

    df = pd.DataFrame(weibos)

    if i == 0:
        df.to_csv(user_name + '_weibos.csv', mode='a', encoding="utf-8")
    else:
        df.to_csv(user_name + '_weibos.csv', mode='a', header=False, encoding="utf-8")

    sleeptime_one = random.randint(SLEEP_INTERVAL-10, SLEEP_INTERVAL + 10)
    time.sleep(sleeptime_one)


# weibo_divs = soup.findAll("div", {"class": "c"})[1:-2]

# for weibo_div in weibo_divs:
#     one_weibo = parse_one_weibo(weibo_div)


