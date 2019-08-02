# -*- coding: utf-8 -*- 
# @Author : Zhy

'''

通过selenium+Chrome驱动实现自动登录并存储cookie到配置文件中供持续使用
根据redis数据库存储的公司名爬取指定公司的工商信息
清洗后的数据发送到指定接口，交互使用AES加密方式

'''

import configparser
import redis
import os
from datetime import date
from hashlib import sha512
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import hmac
import requests
import json
from urllib import request,parse
import json
from fontTools.ttLib import TTFont
import traceback
import time
import urllib
from scrapy import Selector
import requests
import pymysql
import random
from ctypes import *
from ctypes.wintypes import DWORD
import sqlite3
import platform
import getpass
import re
from Crypto.Cipher import AES
import base64
import datetime
import logging
import shutil

proxyHost = "http-dyn.abuyun.com"
proxyPort = "9020"
# 代理隧道验证信息
proxyUser = "user"
proxyPass = "password"
proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
proxy_handler = request.ProxyHandler({
    "http": proxyMeta,
    "https": proxyMeta,
})
proxies = {
    "http": proxyMeta,
    "https": proxyMeta,
}
opener = request.build_opener(proxy_handler)
request.install_opener(opener)
user_agent_li = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',]
# com_port='http://*******/yrapp/hzk'
com_port='http://*******/note/hzk'    # 数据储存接口

REDIS_HOST = '********'
REDIS_PORT = 6379
REDIS_PASSWORD = '********'
REDIS_KEY = 'spider:start_urls'
REDIS_KEY_JK = 'jike:companies'
NEW_REDIS_KEY='spider:finish_status'

filedir = os.getcwd() + os.sep + 'logging'
filelog = os.getcwd() + os.sep + 'logging' + os.sep + 'logging.log'


if not os.path.exists(filedir):
    os.makedirs(filedir)
else:
    shutil.rmtree(filedir)
    os.makedirs(filedir)
    pass

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s : %(message)s',
    datefmt='%Y-%m-%d %A %H:%M:%S',
    filename=filelog,
    filemode='a')

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)

def AES_Encrypt(data):
    vi = 'uacfHwFTdaRlKk74'
    key = 'uacfHwFTdaRlKk74'

    pad = lambda s: s + (16 - len(s.encode('utf-8'))%16) * chr(16 - len(s.encode('utf-8'))%16)
    data = pad(data)
    # 字符串补位
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    # # 加密后得到的是bytes类型的数据
    # encodestrs = base64.b64encode(encryptedbytes)
    # # 使用Base64进行编码,返回byte字符串
    # enctext = encryptedbytes.decode('utf8')
    # 对byte字符串按utf-8进行解码
    return encryptedbytes
def AES_Decrypt(data):
    vi = 'uacfHwFTdaRlKk74'
    key = 'uacfHwFTdaRlKk74'
    # data = data.encode('utf8')
    # encodebytes = base64.decodebytes(data)
    # 将加密数据转换位bytes类型数据
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    text_decrypted = cipher.decrypt(data)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    # 去补位
    text_decrypted = text_decrypted.decode('utf8')
    return text_decrypted
def get_companyname():
    timestamp=str(datetime.datetime.today())[:19]
    data={
        "getComps": {
            "timestamp": timestamp,
        }
    }
    data = json.dumps(data)
    data = AES_Encrypt(data)
    a = requests.post(url=com_port, data=data).content
    data_com = AES_Decrypt(a)
    data_com=data_com.replace('"','').split('[')[1].split('], hasNext')[0]
    data_com=data_com.split(',')
    return data_com
def func_1(url, cookie):
    data = json.dumps({}, separators=(',', ':'))
    api = (url.split('www.qixin.com')[1].strip()).lower()
    s = {'codes': {0: "y", 1: "1", 2: "A", 3: "H", 4: "A", 5: "P", 6: "m", 7: "s", 8: "y", 9: "C", 10: "x", 11: "R",
                   12: "M", 13: "Q", 14: "D", 15: "c", 16: "y", 17: "C", 18: "V", 19: "S"}, 'n': 20}
    string = ''
    for key, value in enumerate(api * 2):
        string += s['codes'].get(ord(value) % s['n'])
    secret = string.encode('utf-8')
    a = hmac.new(secret, api.encode('utf-8'), sha512).hexdigest()
    a = a[10: 30]
    b = hmac.new(secret,'{api}{data}'.format(api=api*2, data=data).encode('utf-8'), sha512).hexdigest()
    headers = {
        a: b,
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.get(url=url, headers=headers)
    # response = requests.get(url=url, headers=headers,proxies=proxies)
    # response = requests.post(url=url, headers=headers, data=data,proxies=proxies)
    return response.text
def func(data, cookie):
    api = '/api/enterprise/getannualreport'
    s = {'codes': {0: "y", 1: "1", 2: "A", 3: "H", 4: "A", 5: "P", 6: "m", 7: "s", 8: "y", 9: "C", 10: "x", 11: "R",
                   12: "M", 13: "Q", 14: "D", 15: "c", 16: "y", 17: "C", 18: "V", 19: "S"}, 'n': 20}
    string = ''
    for key, value in enumerate(api * 2):
        string += s['codes'].get(ord(value) % s['n'])

    secret = string.encode('utf-8')
    a = hmac.new(secret, '/api/enterprise/getannualreport'.encode('utf-8'), sha512).hexdigest()
    a = a[10: 30]

    b = hmac.new(secret, '/api/enterprise/getannualreport/api/enterprise/getannualreport{data}'.format(data=data).encode('utf-8'), sha512).hexdigest()
    url = 'https://www.qixin.com/api/enterprise/getAnnualReport'
    headers = {
        a: b,
        'Cookie': cookie,
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        'Content-Type': 'application/json;charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.post(url=url, headers=headers, data=data)
    # response = requests.post(url=url, headers=headers, data=data,proxies=proxies)
    return response.text
def get_info_qxb(source_text):
    font_convert_dic = {48: '0', 49: '1', 50: '2', 51: '3', 52: '4', 53: '5', 54: '6', 55: '7', 56: '8', 57: '9', 65: 'A', 66: 'B', 67: 'C', 68: 'D', 69: 'E', 70: 'F', 71: 'G', 72: 'H', 73: 'I', 74: 'J', 75: 'K', 76: 'L', 77: 'M', 78: 'N', 79: 'O', 80: 'P', 81: 'Q', 82: 'R', 83: 'S', 84: 'T', 85: 'U', 86: 'V', 87: 'W', 88: 'X', 89: 'Y', 90: 'Z', 97: 'a', 98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g', 104: 'h', 105: 'i', 106: 'j', 107: 'k', 108: 'l', 109: 'm', 110: 'n', 111: 'o', 112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u', 118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z'}
    re_css = re.search('href="//cache.qixin.com/pcweb/common.(.+?).css', source_text).group()
    font_css_url = 'https:' + re_css.split('"')[1]
    font_css_url = font_css_url.replace('.css', '-partial1.css')
    file_css = 'test.css'
    urllib.request.urlretrieve(font_css_url, file_css)
    urllib.request.urlretrieve(font_css_url, file_css)
    woff2_url = ''
    with open(file_css, 'r') as f_css:
        try:
            css_content = f_css.read()
            if 'transform: translate(0)' in css_content:
                woff2_url_re = re.findall('format[(]"(.+?)"[)],url[(]//cache.qixin.com/pcweb/(.+?).woff2', css_content)
                for i in woff2_url_re:
                    if 'halfling' not in i[1]:
                        woff2_url = 'https://cache.qixin.com/pcweb/' + i[1] + '.woff2'
        except:
            pass

    if woff2_url:
        fontwoff_name = 'test.woff2'
        fontxml_name = 'test_1.woff'
        urllib.request.urlretrieve(woff2_url, fontwoff_name)
        font = TTFont(fontwoff_name)
        font.saveXML(fontxml_name)
        camp_list = font.getBestCmap()
        font_qxb_dic = {}
        for camp_k, camp_v in camp_list.items():
            try:
                convert_k = camp_v.split('_')[-1]
                # print('{}-----{}'.format(convert_k, font_convert_dic[camp_k]))
                font_qxb_dic[font_convert_dic[camp_k]] = convert_k
            except:
                # traceback.print_exc()
                pass
        re_qxb_num = r'(?=class="qxb-num").+?[>]+?(.+?)<'
        patt_qxb_num = re.compile(re_qxb_num)
        sub_text = patt_qxb_num.findall(source_text)
        for sub_text_1 in sub_text:
            sub_text_2 = []
            for i in sub_text_1:
                if str(i) in ['8', '3', '5', '2', '0', '9', '1', '4', '7', '6']:
                    sub_text_2.append(str(font_qxb_dic[i]))
                else:
                    sub_text_2.append(str(i))
            sub_text_2 = ''.join(sub_text_2)
            source_text = source_text.replace(sub_text_1, sub_text_2)
        return source_text
    else:
        return 'font_false'
def qxb_jx(dict_xinxi):
    #print(dict_xinxi)
    dict_1 = {}
    dict_1['compCrawlSucc'] = {}
    dict_1['compCrawlSucc']['basicInfo'] = {}
    dict_1['compCrawlSucc']['businessInfo'] = {}
    dict_1['compCrawlSucc']['memberInfo'] = []
    dict_1['compCrawlSucc']['sharehInfo'] = []
    dict_1['compCrawlSucc']['investInfo'] = []    #对外投资
    dict_1['compCrawlSucc']['icpInfo'] = []       #ICP备案信息

    '''基础信息'''
    # try:
    #     if '市' in dict_xinxi['data']['address']:
    #         dict_1['compCrawlSucc']['basicInfo']['area'] = dict_xinxi['data']['belong_org'].split('市')[0]
    #     elif '市' in dict_xinxi['data']['belong_org']:
    #         dict_1['compCrawlSucc']['basicInfo']['area'] = dict_xinxi['data']['belong_org'].split('市')[0]
    #     else:
    #         dict_1['compCrawlSucc']['basicInfo']['area'] = ''
    # except:
    #     dict_1['compCrawlSucc']['basicInfo']['area'] = ''
    #     pass
    dict_1['compCrawlSucc']['basicInfo']['legalRepl'] = dict_xinxi['data']['oper_name']
    compState=dict_xinxi['data']['status']
    dict_1['compCrawlSucc']['basicInfo']['compState'] = ''
    list_state=['在营', '存续', '在业', '开业', '正常', '登记成立']

    try:
        for status in list_state:
            if status in compState:
                dict_1['compCrawlSucc']['basicInfo']['compState'] = '在营(存续)'
        if '注销'in compState:
            dict_1['compCrawlSucc']['basicInfo']['compState'] = '注销'
        elif '吊销'in compState:
            dict_1['compCrawlSucc']['basicInfo']['compState'] = '吊销'
        elif '迁出' in compState:
            dict_1['compCrawlSucc']['basicInfo']['compState'] = '迁出'
    except:
        pass
    try:
        start_time = dict_xinxi['data']['start_date']
        time_tuple = datetime.datetime.strptime(start_time, '%Y-%m-%d')
        dict_1['compCrawlSucc']['basicInfo']['registerDate'] = start_time
    except:
        dict_1['compCrawlSucc']['basicInfo']['registerDate'] =''

    dict_1['compCrawlSucc']['basicInfo']['registerMoney'] = dict_xinxi['data']['regist_capi']
    dict_1['compCrawlSucc']['basicInfo']['compPhone'] = ''
    dict_1['compCrawlSucc']['basicInfo']['compEmail'] = ''
    dict_1['compCrawlSucc']['basicInfo']['compAddr']=''
    dict_1['compCrawlSucc']['basicInfo']['compDesc'] = ''
    try:
        dict_1['compCrawlSucc']['basicInfo']['compPhone'] = dict_xinxi['data']['contact']['telephone']
    except:
        pass
    try:
        dict_1['compCrawlSucc']['basicInfo']['compEmail'] = dict_xinxi['data']['contact']['email']
    except:
        pass

    try:
        # 网址
        dict_1['compCrawlSucc']['basicInfo']['compWebsite'] = dict_xinxi['data']['websites'][0]['web_url']
    except:
        dict_1['compCrawlSucc']['basicInfo']['compWebsite'] = ''
        pass
    try:
        #地址
        dict_1['compCrawlSucc']['basicInfo']['compAddr'] = dict_xinxi['data']['address']
    except:
        dict_1['compCrawlSucc']['basicInfo']['compAddr'] = dict_xinxi['data']['contact']['address']
        pass

    '''工商信息'''
    dict_1['compCrawlSucc']['businessInfo']['bizRegNo'] = dict_xinxi['data']['reg_no']
    dict_1['compCrawlSucc']['businessInfo']['creditCode'] = dict_xinxi['data']['credit_no']
    dict_1['compCrawlSucc']['businessInfo']['compType'] = dict_xinxi['data']['econ_kind']
    # dict_1['compCrawlSucc']['businessInfo']['trade'] = ''
    dict_1['compCrawlSucc']['businessInfo']['businessBegin'] = dict_xinxi['data']['term_start']
    dict_1['compCrawlSucc']['businessInfo']['businessEnd'] = dict_xinxi['data']['term_end']
    dict_1['compCrawlSucc']['businessInfo']['approvalDate'] = dict_xinxi['data']['check_date']
    dict_1['compCrawlSucc']['businessInfo']['paidMoney'] = ''
    dict_1['compCrawlSucc']['businessInfo']['insuredCount'] = ''
    dict_1['compCrawlSucc']['businessInfo']['manScale'] = ''
    dict_1['compCrawlSucc']['businessInfo']['regOrg'] = dict_xinxi['data']['belong_org']
    dict_1['compCrawlSucc']['businessInfo']['operateScope'] = dict_xinxi['data']['scope']
    # try:
    #     dict_1['compCrawlSucc']['businessInfo']['trade'] = dict_xinxi['data']['domains'][0]
    # except:
    #     pass
    '''主要成员'''
    try:
        for index, employee in enumerate(dict_xinxi['data']['employees']):
            dict_employee = {}
            dict_employee['orderNumber'] = int(index + 1)
            dict_employee['name'] = employee['name']
            dict_employee['job'] = employee['job_title']
            dict_1['compCrawlSucc']['memberInfo'].append(dict_employee)
    except:
        dict_1['compCrawlSucc']['memberInfo']=[]
        traceback.print_exc()
        pass

    '''股东信息'''
    try:
        total_amount = float(dict_1['compCrawlSucc']['basicInfo']['registerMoney'].replace('万', '').replace('美元', '').replace('人民币', '').replace(' ', ''))
        for index, partner in enumerate(dict_xinxi['data']['partners']):
            dict_partner = {}
            dict_partner['orderNumber'] = str(index + 1)
            dict_partner['name'] = partner['name']
            try:
                if partner['should_capi_items'] ==[] or '-'in str(partner['should_capi_items']):
                    dict_partner['paidMoney']=''
                    dict_partner['paidScale']=''
                else:
                    dict_partner['paidMoney'] = partner['should_capi_items'][0]['shoud_capi']
                    paid_amount = float(dict_partner['paidMoney'].replace('万', '').replace('美元', '').replace('人民币', '').replace(' ', ''))
                    dict_partner['paidScale'] = str((paid_amount / total_amount) * 100)[0:5] + '%'
                dict_1['compCrawlSucc']['sharehInfo'].append(dict_partner)
            except:
                traceback.print_exc()
                pass
    except:
        dict_1['compCrawlSucc']['sharehInfo'] = []
        pass

    return dict_1
#更新cookie
def login(num):
    conf = configparser.RawConfigParser()
    ini_p = os.getcwd() + os.sep +'qxb_acount.ini'
    # if r'\\' in ini_p:
    #     ini_p = ini_p.replace(r'\\', '/')
    # print(ini_p)
    conf.read(ini_p, encoding='utf-8')  # 文件路径
    phone_num=conf.get(num, "phone_num")
    password=conf.get(num, "password")
    path_chr = os.getcwd() + os.sep + 'chromedriver.exe'
    browser = webdriver.Chrome(executable_path=path_chr)  # executable_path:谷歌驱动所在的位置
    browser.get('https://www.qixin.com/auth/login?return_url=%2F')
    browser.maximize_window()
    browser.find_element_by_xpath("//div[@class='col-sm-24 col-xs-24 padding-r-2x']/div[1]/input").send_keys(phone_num)
    time.sleep(1.5)
    browser.find_element_by_xpath("//div[@class='col-sm-24 col-xs-24 padding-r-2x']/div[2]/input").send_keys(password)
    ENTER = '\ue007'  # 回车键
    time.sleep(random.uniform(2, 3))
    browser.find_element_by_xpath("//div[@class='col-sm-24 col-xs-24 padding-r-2x']/div[2]/input").send_keys(Keys.ENTER)
    # print(browser.get_cookies())
    time.sleep(5)
    cookie = ''
    for i in browser.get_cookies():
        if cookie == '':
            cookie=i["name"]+':'+i["value"]
        else:
            cookie=cookie +'; '+i["name"]+'='+i["value"]
    browser.quit()
    conf.set(num, 'cookie_str', cookie)
    conf.write(open(ini_p, "w"))
    return cookie
def get_info_aqxb(name,new_name,cookie):
    time.sleep(random.uniform(2, 4))
    url_1='https://www.qixin.com/api/search/suggestion?'+parse.urlencode({'key': name})
    response_text=func_1(url_1,cookie)
    list_1 = json.loads(response_text)
    # print(list_1)
    list_2 = []
    if list_1==[]:
        url_sy='https://www.qixin.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4094.1 Safari/537.36',
            'Cookie': cookie,
            'Host': 'www.qixin.com',
            'Upgrade-Insecure-Requests': '1',
            }
        text_1 = requests.get(url=url_sy, headers=headers).text
        if '请登录' in text_1:
            return 'cook_invalid'
        else:
            return 'no_info'
        pass
    else:
        for xinxi in list_1:
            if xinxi['name']==name:
                eid=xinxi['eid']
                list_2.append(eid)
                print(eid)
        if list_2 == []:
            return 'no_info'
    try:
        url_2='http://api.qixin.com/APITestService/enterprise/getDetailAndContactById?appkey=ada44bd0070711e6b8a865678b483fde&id={}'.format(eid)
        header_1={
            'Host': 'api.qixin.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
        }
        html_1=requests.get(url=url_2,headers=header_1,proxies=proxies).text
        dict_xinxi = json.loads(html_1)
        dict_1=qxb_jx(dict_xinxi)
        dict_1['compCrawlSucc']['timestamp']=str(datetime.datetime.today())[:19]
        dict_1['compCrawlSucc']['compName']=new_name
        return dict_1
    except:
        traceback.print_exc()
        return 'false'
def main():
    conf = configparser.RawConfigParser()
    ini_p = os.getcwd() + os.sep + 'qxb_acount.ini'
    conf.read(ini_p, encoding='utf-8')
    account_id=0
    account_num=48    #账号数量
    while True:
        try:
            state=False
            time.sleep(random.uniform(0.5,1))
            if r.llen(REDIS_KEY) == 0:
                r.hset('spider:finish_status', 'finish1', 'true')

            value = r.blpop(REDIS_KEY, timeout=60)
            if value:
                value = value[1].decode('utf-8')  # 队列有值则取，没有则堵塞
            else:
                continue
            com_name = value.split('?key=')[1]
            logging.info('公司名称：{}'.format(com_name))
            if com_name.startswith('PRE-'):
                com_name=com_name.split('PRE-')[1].replace(' ','')
                state=True
            new_name=com_name.replace('(','（').replace(')','）')
            time.sleep(random.uniform(1,2))
            account_id = account_id + 1 if account_id < account_num else 1
            cookie = conf.get(str(account_id), "cookie_str")
            data_get_qxb = get_info_aqxb(com_name,new_name,cookie)
            if 'cook_invalid' in data_get_qxb:
                #cookie失效
                new_cookie = login(str(account_id))
                logging.info('更新cookie：{}'.format(new_cookie))
                try:
                    data_get_qxb = get_info_aqxb(com_name, new_name,new_cookie)
                except:
                    traceback.print_exc()
                    pass
            list_state=['no_info','false','cook_invalid']
            if data_get_qxb in list_state :
                #未能查询到信息
                data_get_qxb={}
                data_get_qxb['compCrawlFail']={}
                data_get_qxb['compCrawlFail']['timestamp']=str(datetime.datetime.today())[:19]
                data_get_qxb['compCrawlFail']['compName']=com_name
            logging.info('工商信息：{}'.format(data_get_qxb))
            data_get_qxb_1 = json.dumps(data_get_qxb, cls=DateEncoder,ensure_ascii=False)
            data_get_qxb_1 = AES_Encrypt(data_get_qxb_1)
        except:
            traceback.print_exc()
            continue
            pass
        try:
            a = requests.post(url=com_port, data=data_get_qxb_1).content
            data_re= AES_Decrypt(a)
            logging.info('返回状态：{}'.format(data_re))
            if '成功' in str(data_re)  and  'compCrawlSucc' in data_get_qxb :
                logging.info('工商信息爬取成功：{}'.format(data_re))
                if state:
                    com_name='PRE-'+com_name
                    r.lpush(REDIS_KEY_JK, com_name)
                else:
                    r.rpush(REDIS_KEY_JK, com_name)
            else:
                logging.info('工商信息爬取失败：{}'.format(data_re))
        except:
            traceback.print_exc()
            continue
            pass


if __name__ == '__main__':
     main()
  




