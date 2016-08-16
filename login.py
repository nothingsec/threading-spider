#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author: nothing -*-
# Pw @ 2016-08-06 19:58:42

import requests
import json
import os

s = requests.session()
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'
}
#获取验证码图片
check_url = 'https://login.kongfz.com/index.php?m=Sign&c=Login&a=showCaptcha'
checkcodepath = 'yzm.png'
verify_code = s.get(check_url,headers=headers,stream=True)
data = verify_code.content
print '正在获取验证码。。。请稍后。。。'
code_pic = open(checkcodepath,'wb')
code_pic.write(data)
code_pic.close()
os.system('eog ' + checkcodepath)
check_code = raw_input(u'请输入验证码：')
#开始登陆
sign = s.post('https://login.kongfz.com/index.php?m=Sign&c=Login&a=loginSign',headers=headers,data={'loginPass':'test_sec_123'}).text
sign = json.loads(sign)
sign = sign['data']['sign']

if sign:
    data = {
        'loginPass':'test_sec_123',
        'loginName':'test_sec',
        'checkCode':check_code,
        'sign':sign,
        'autoLogin':'0'
    }
    login = s.post('https://login.kongfz.com/index.php?m=Sign&c=Login&a=loginAuth',data=data,headers=headers).text
    login = json.loads(login)
    if login['status']:
        print '登陆成功。'
    else:
        print login['data']['desc']
#test = s.get('http://shop.kongfz.com/buyer/order/order_list.html',headers=headers)
#print test.content
