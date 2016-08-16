#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author: nothing -*-
# Pw @ 2016-08-09 4:55 PM
import requests
from bs4 import BeautifulSoup
import Queue
import threading
import time
s = requests.Session()

requests.adapters.DEFAULT_RETRIES = 5
#数据存储结构
'''data = {
    'id':_id,
    'name':name,
    'type':_type,
    'level':level,
    'user':user,
    'user_href':user_href,
    'user_account':user_account
}'''
queue1 = Queue.Queue()

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
}
#将所有链接存储到队列中去
for i in range(1,21):
    url = 'http://shop.kongfz.com/shop_list_7_%d.html' % i
    queue1.put(url)

lock = threading.Lock()   #加锁
datas = {}
def spider():
    while True:
        #设定结束条件
        if queue1.empty():
            break
        #用BeautifulSoup解析网页并抓取各项目
        url = queue1.get()
        html = s.get(url,headers = headers).text
        Soup = BeautifulSoup(html,'lxml')
        _ids = Soup.select('#page_book_shop > div:div:nth-of-type(6) > div > table:nth-of-type(2) > tr > td.wd70')
        names = Soup.select('#page_book_shop > div:div:nth-of-type(6) > div > table:nth-of-type(2) > tr > td.wd310 > a')
        _types = Soup.select('#page_book_shop > div:div:nth-of-type(6) > div > table:nth-of-type(2) > tr > td:nth-of-type(3)')
        levels = Soup.select('#page_book_shop > div:div:nth-of-type(6) > div > table:nth-of-type(2) > tr > td:nth-of-type(4) > div')
        users = Soup.select('#page_book_shop > div:div:nth-of-type(6) > div > table:nth-of-type(2) > tr > td.wd200 > div > a:nth-of-type(1)')

        #存储数据
        for _id,name,_type,level,user in zip(_ids,names,_types,levels,users):
            user_href = user.get('href')
            res = s.get(user_href, headers=headers)
            html2 = res.text
            Soup2 = BeautifulSoup(html2, 'lxml')
            user_account = Soup2.select('#page_user_info > div.content > div > table > tr:nth-of-type(2) > td:nth-of-type(2)')
            lock.acquire()
            print user_account[0].get_text()
            lock.release()
            data = {
                'name': name.get_text(),
                'type': _type.get_text(),
                'level': level.get('title'),
                'user': user.get_text(),
                'user_account': user_account[0].get_text()
            }
            datas[int(_id.get_text())] = data
        lock.acquire()
        print 'url : %s 已经爬取完毕！' % url
        lock.release()
    #将数据写入文件
    file = open('dic.txt','wb')
    file.write('id,资金账号，书店主人，类别，书店名,等级\n')
    lock.acquire()
    for (k, v) in datas.items():
        i = 1
        file.write('%5d'%k)
        for (ik, iv) in v.items():
            if i != 5:
                file.write('%20s' %  iv.encode('utf8'))
            else:
                file.write('%20s\n' % iv.encode('utf8'))
            i += 1
    lock.release()
    file.close()



threads = []
for i in range(20):
    t = threading.Thread(target=spider)
    threads.append(t)
    t.start()

for t in threads:
    t.join()
