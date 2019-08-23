#coding:utf-8
import urllib
import urllib2
# import re
import time
# from lxml import etree
from bs4 import BeautifulSoup
# from BeautifulSoup import *


SLEEP_FLAG = 1
SLEEP_INTERVAL = 40
import pandas as pd
import random


HEADERS = {'User-Agent': '''Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36''',
           'Host': 'weibo.cn',
           "cookie": r'''ALF=1569123756; SCF=AisR_kkQv3XsOSavJe9Ka-f3Yik-iI-Q3C6W6ZvA_wm1XlpHu1r3MZoMzzwwTRwqlF-ZMcsCD3owxUfqj1T_OqY.; SUB=_2A25wWxD9DeRhGeNM7lsQ-C_Mzz6IHXVTp7C1rDV6PUNbktANLVPekW1NSaQIXJY1HDMWDLq02p1G4SpQD2aNCof7; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWpJJ1.W2X37czZpe-3o6sg5JpX5KMhUgL.Fo-ESK.p1h27Shz2dJLoIEXLxK-LBo5L12qLxKMLB.-L12-LxKBLBonL12-LxK-LBo5L12qLxKqLB-qL1h-t; SUHB=0bt8Tmfe6BvQfw; SSOLoginState=1566531757; _T_WM=0b6efda74b267a92c885f60fd7fe72f7'''}

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
    # print page_num_div
    page_num = int(page_num_div.find("input", {"name": "mp"})["value"])
    return page_num

# print one_weibo

def get_page_num(user_name):

    url = "https://weibo.cn/%s/profile?hasori=1&haspic=0&starttime=20160101&endtime=20190101&advancedfilter=1&page=%d" % (user_name, 2)
    # print url
    html = Parseurl(url)
    soup = BeautifulSoup(html, "lxml")
    page_num = parse_page_num(soup)
    #         #设置随机休眠时间
    sleeptime_one = random.randint(SLEEP_INTERVAL-10, SLEEP_INTERVAL + 10)
    time.sleep(sleeptime_one)

    return page_num

# -------------------------------------------------------------------------------------------

user_name = "2803301701"

page_num = get_page_num(user_name)

print page_num
# start page from  here....

start = 1

for i in range(page_num):

    if i+1 < start:
        continue
    print "page ", i+1, "/", page_num


    url = "https://weibo.cn/%s/profile?hasori=1&haspic=0&starttime=20160101&endtime=20190101&advancedfilter=1&page=%d" % (user_name, i+1)
    
    print url
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



