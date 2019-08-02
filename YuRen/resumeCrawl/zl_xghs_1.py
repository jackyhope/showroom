# -*- coding: utf-8 -*-：

import traceback
import requests,datetime
from urllib import parse
import json
import time
import logging
from settings import *
import execjs
import random
from ctypes import *
from ctypes.wintypes import DWORD
import sqlite3
import configparser
import os
import platform
import getpass

wu_jl_url = CLEAN_RESUME_URL
wu_jlxw_url = SEARCH_STATUS_URL

def get_cook_str(hostKey, cook_yb):
    ini_p = os.getcwd() + '/Mod_Pyth/pyth/conf.ini'
    if r'\\' in ini_p:
        ini_p = ini_p.replace(r'\\', '/')
    conf = configparser.ConfigParser(strict=False, allow_no_value=True)
    conf.read(ini_p, encoding='utf-8')  # 文件路径
    cookfile = conf.get('config', 'pro1')

    cookieFile = cookfile
    LocalFree = windll.kernel32.LocalFree
    memcpy = cdll.msvcrt.memcpy
    CryptProtectData = windll.crypt32.CryptProtectData
    CryptUnprotectData = windll.crypt32.CryptUnprotectData
    CRYPTPROTECT_UI_FORBIDDEN = 0x01

    class DATA_BLOB(Structure):
        _fields_ = [("cbData", DWORD), ("pbData", POINTER(c_char))]

    def getData(blobOut):
        cbData = int(blobOut.cbData)
        pbData = blobOut.pbData
        buffer = c_buffer(cbData)
        memcpy(buffer, pbData, cbData)
        LocalFree(pbData)
        return buffer.raw

    def encrypt(plainText):
        bufferIn = c_buffer(plainText, len(plainText))
        blobIn = DATA_BLOB(len(plainText), bufferIn)
        blobOut = DATA_BLOB()

        if CryptProtectData(byref(blobIn), u"python_data", None,
                            None, None, CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
            return getData(blobOut)
        else:
            raise Exception("Failed to encrypt data")

    def decrypt(cipherText):
        bufferIn = c_buffer(cipherText, len(cipherText))
        blobIn = DATA_BLOB(len(cipherText), bufferIn)
        blobOut = DATA_BLOB()

        if CryptUnprotectData(byref(blobIn), None, None, None, None,
                              CRYPTPROTECT_UI_FORBIDDEN, byref(blobOut)):
            return getData(blobOut)
        else:
            raise Exception("Failed to decrypt data")

    # 获取cookies，此处cookies需要保存在本地
    conn = sqlite3.connect(cookieFile)
    c = conn.cursor()
    sql = "select host_key, name, value, path,encrypted_value from cookies where host_key like \'%" + hostKey + "%\'"
    c.execute(sql)
    cookies = c.fetchall()
    # print(cookies)
    # print(len(cookies))
    c.close()
    # 加工cookies成字符串
    cookies_list = []
    cookies_all_list = []
    cookies_name_list = []
    cookies_str_zl = cook_yb
    cookies_list0 = cookies_str_zl.split(';')

    for cookie in cookies_list0:
        cookies_name = cookie.split('=')[0].strip()
        cookies_name_list.append(cookies_name)

    cookies_str_list = []
    for row in cookies:
        dc = decrypt(row[4])
        cookie_one2 = str(row[1]) + '=' + str(dc, encoding='utf-8')
        cookies_all_list.append(cookie_one2)
        if str(row[1]) in cookies_name_list:
            cookies_dict = {}
            cookies_dict['domain'] = str(row[0])
            cookies_dict['name'] = str(row[1])
            cookies_dict['value'] = str(dc, encoding='utf-8')
            cookies_dict['path'] = '/'
            cookies_dict['httpOnly'] = False
            cookies_dict['HostOnly'] = False
            cookies_dict['Secure'] = False
            str_cook = str(row[1]) + '=' + str(dc, encoding='utf-8')
            cookies_str_list.append(str_cook)
    cookies_str = '; '.join(cookies_str_list)
    return cookies_str
def get_useragent():
    USER_AGENTS = [
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/531.21.8 (KHTML, like Gecko) Version/4.0.4 Safari/531.21.10",
        "Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/533.17.8 (KHTML, like Gecko) Version/5.0.1 Safari/533.17.8",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.19.4 (KHTML, like Gecko) Version/5.0.2 Safari/533.18.5",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.1.17) Gecko/20110123 (like Firefox/3.x) SeaMonkey/2.0.12",
        "Mozilla/5.0 (Windows NT 5.2; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 SeaMonkey/2.7.1",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_8; en-US) AppleWebKit/532.8 (KHTML, like Gecko) Chrome/4.0.302.2 Safari/532.8",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_5; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.15 Safari/534.13",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.186 Safari/535.1",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.36 Safari/535.7",
        "Mozilla/5.0 (Macintosh; U; Mac OS X Mach-O; en-US; rv:2.0a) Gecko/20040614 Firefox/3.0.0 ",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.0.3) Gecko/2008092414 Firefox/3.0.3",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.5; en-US; rv:1.9.1) Gecko/20090624 Firefox/3.5",
        "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; en-US; rv:1.9.2.14) Gecko/20110218 AlexaToolbar/alxf-2.0 Firefox/3.6.14",
        "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    ]
    user_agent = random.choice(USER_AGENTS)
    return user_agent
def get_date(days):
    return datetime.datetime.now() - datetime.timedelta(days=days)

#判断是否登录,获取到指定参数
def login_judge_zl(cookie):
    headers={
    'User-Agent':get_useragent(),
    # 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    # # 'Accept-Encoding':'gzip, deflate, br',
    # 'Accept-Language':'zh-CN,zh;q=0.8',
    # 'Connection':'keep-alive',
    # 'Content-Type':'text/plain',
    # 'Cookie':'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
    'Cookie':cookie,
    # 'Upgrade - Insecure - Requests': '1',
    # 'Host':'rdapi.zhaopin.com',
    }
    url_zy="https://rd5.zhaopin.com/"
    response_zy = requests.get(url=url_zy, headers=headers).text
    # print(response_zy)

    # print(response_zy)
    # print(type(response_zy))
    # print(response_zy)
    # sel=Selector(text=response_zy)
    # html_zy = sel.xpath('string(//script)').extract()[0].strip()
    uid=response_zy.replace('"','').split('userId:')[1].split(",")[0]
    orgid=response_zy.replace('"','').split('orgId:')[1].split(",")[0]
    meta= "uid="+uid+",orgid="+orgid
    company_name=response_zy.replace('"','').split('businessLicenceName:')[1].split(",")[0]
    # print(meta,company_name)
    return meta,company_name
#职位剩余刷新次数
def zw_sx_cs(cookie,meta):
    now_time=str(int(time.time()*1000))
    headers={
    'User-Agent':get_useragent(),
    'Accept':'application/json, text/javascript, */*; q=0.01',
    # 'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Content-Length':'15',
    'Content-Type':'text/plain',
    'Cookie':cookie,
    # 'Cookie':'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
    'Host':'rdapi.zhaopin.com',
    'Origin':'https://rd5.zhaopin.com',
    'Referer':'https://rd5.zhaopin.com/job/manage',
    'zp-route-meta':meta
    }
    url_sx="https://rdapi.zhaopin.com/rd/assets/balance?_="+now_time
    pay_load={'assetType':'7'}
    response_sx = requests.post(url=url_sx, headers=headers, data=json.dumps(pay_load)).text
    str_response=str(response_sx)
    sx_cs=str_response.replace('"',"").split("data:")[1].split(",")[0]
    return sx_cs
#职位刷新
def zw_shua_xi(cookie,meta,job_num):
    now_time=str(int(time.time()*1000))
    headers={
    'User-Agent':get_useragent(),
    'Accept':'application/json, text/javascript, */*; q=0.01',
    # 'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Connection':'keep-alive',
    'Content-Length':'92',
    'Content-Type':'text/plain',
    'Cookie':cookie,
    # 'Cookie':'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
    'Host':'rdapi.zhaopin.com',
    'Origin':'https://rd5.zhaopin.com',
    'Referer':'https://rd5.zhaopin.com/job/manage',
    'zp-route-meta':meta
    }
    url_sx="https://rdapi.zhaopin.com/rd/job/refresh?_="+now_time
    pay_load={'coupons':[],'dataList':[{'type': "1", 'jobNumber': job_num}],'payType':"1"}
    response_sx = requests.post(url=url_sx, headers=headers, data=json.dumps(pay_load)).text
    print(response_sx)
    return response_sx
def get_reqid(str_1):
    ctx = execjs.compile(
        """
        function req_id() {
            var zpPageRequestId = "######-" + (new Date()).valueOf() + "-" + parseInt(Math.random() * 1000000);
            return zpPageRequestId;
        }
        """.replace('######', str_1)
    )
    req_id_str = ctx.call('req_id',)
    return req_id_str
#判断简历ID是否存在,当jl_total等于0时不存在
def jx_idcz(cookie,meta,company_name,jl_id):
    headers_sy = {
        'User-Agent': get_useragent(),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'text/plain',
        'Cookie': cookie,
        # 'Cookie':'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
        'Host': 'rdapi.zhaopin.com',
        'Origin': 'https://rd5.zhaopin.com',
        'Referer': 'https://passport.zhaopin.com',
        'zp-route-meta': meta
    }

    response_sy = requests.get(url='https://rd5.zhaopin.com/', headers=headers_sy, timeout=5)
    # str_response = str(response_sy)
    get_request_id = response_sy.headers.get('x-zp-request-id')
    # company_name="浙江中恩通信技术有限公司"
    # jl_id="Sj44dSm)xWMF(mfYcxSq)Q"
    now_time=str(int(time.time()*1000))

    headers_1 = {
        'User-Agent': get_useragent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        # 'Cookie':'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
        'Host': 'rd5.zhaopin.com',
    }

    request_id = get_reqid(get_request_id)
    urlxxx = 'https://rd5.zhaopin.com/api/rd/assets/summary?_={}&isNewList=true&x-zp-page-request-id={}'.format(now_time, request_id)
    url_id = "https://rd5.zhaopin.com/api/rd/assets/balance?_={}&x-zp-page-request-id={}".format(now_time, request_id)
    xz_cs_url = 'https://rd5.zhaopin.com/api/rd/assets/balance/download?_={}&x-zp-page-request-id={}'.format(now_time, request_id)
    print(urlxxx)
    response_sx = requests.get(url=urlxxx, headers=headers_1, timeout=5).text
    str_response = str(response_sx)
    dianshu_dic = json.loads(str_response)
    # 下载次数， 智联币
    print(dianshu_dic['data']['assets']['normalDownload'], dianshu_dic['data']['coins']['balance'])

    # return 1,2,3
#通过id搜索进行简历下载
def jl_xiazai(cookie,meta,resumeNumber,pay_type):
    now_time=str(int(time.time()*1000))
    headers = {
        'User-Agent': get_useragent(),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Length': '176',
        'Content-Type': 'text/plain',
        'Cookie': cookie,
        # 'Cookie':'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
        'Host': 'rdapi.zhaopin.com',
        'Origin': 'https://rd5.zhaopin.com',
        'Referer': 'https://rd5.zhaopin.com/search/result',
        'zp-route-meta': meta
    }
    url_xz="https://rdapi.zhaopin.com/rd/resume/download?_="+now_time
    pay_load={
        'coupons':"",
        'downloadType':"2",
        'paymentType':pay_type,
        'resumeDownType':'0',
        'resumeFolderId':'101424766',
        'resumeItems':[{'lang': 1, 'resumeNumber': resumeNumber, 'version': '1'}]
    }
    time.sleep(random.uniform(1, 2))
    response_sx = requests.post(url=url_xz, headers=headers, data=json.dumps(pay_load)).text
    # print(response_sx)
    return response_sx
#对通过ID搜索得到后的简历进行解析
def id_jl_jx(cookie,meta,response_sx,orgid):
    now_time=str(int(time.time()*1000))
    #转为字典格式
    dict_xinxi = json.loads(response_sx)
    dict_data = dict_xinxi["data"]
    dict_jl = dict_data["dataList"][0]
    # print(dict_jl)
    id_num=dict_jl["id"]
    d_pos = {"id": id_num}
    postdata_str = str(parse.urlencode(d_pos).encode('utf-8'))
    jl_id = postdata_str.split("id=")[1].split("&")[0].replace("'", "")
    resumeNo = jl_id + "_1_1%3B" + dict_jl["k"] + "%3B" + dict_jl["t"]
    url_jl = "https://rd5.zhaopin.com/resume/detail?"  + "&resumeNo=" + resumeNo
    # 获取简历页面的json文件
    headers_jl = {
        'User-Agent': get_useragent(),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        # 'Cookie': 'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
        'Host': 'rdapi.zhaopin.com',
        'Origin': 'https://rd5.zhaopin.com',
        'Referer': url_jl,
        'zp-route-meta': meta
    }
    url_json = "https://rdapi.zhaopin.com/rd/resume/detail?_=" + now_time + "&resumeNo=" + resumeNo
    # print(url_json)
    time.sleep(random.uniform(1, 3))
    response_json = requests.get(url=url_json, headers=headers_jl).text
    # print(response_json)
    # orgid = meta.split('orgid=')[1].replace(" ", "")
    data=jl_jiexi(xinxi=dict_jl, text_json=response_json,org_id=orgid,job_id="",resume_type=2)
    return data
#简历下载剩余次数
def jx_xz_cs(cookie,meta,city_id,province_id):

    now_time=str(int(time.time()*1000))
    headers = {
        'User-Agent': get_useragent(),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '77',
        'Content-Type': 'text/plain',
        'Cookie': cookie,
        # 'Cookie': 'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
        'Host': 'rdapi.zhaopin.com',
        'Origin': 'https://rd5.zhaopin.com',
        'Referer': 'https://rd5.zhaopin.com/search/result',
        'zp-route-meta': meta
    }
    url_id="https://rdapi.zhaopin.com/rd/assets/balance/download?_="+now_time
    pay_load={
        'candidates':[{'cityId': city_id, 'provinceId': province_id}]}
    response_sx = requests.post(url=url_id, headers=headers,data=json.dumps(pay_load)).text
    # print(response_sx)
    str_response = str(response_sx)
    xz_cs = str_response.replace('"', "").split("dotCount:")[1].split(",")[0]

    return xz_cs
#智联币剩余数量
def jx_zlb_sl(cookie,meta):
    headers_sy = {
        'User-Agent': get_useragent(),
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'text/plain',
        'Cookie': cookie,
        # 'Cookie':'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
        'Host': 'rdapi.zhaopin.com',
        'Origin': 'https://rd5.zhaopin.com',
        'Referer': 'https://passport.zhaopin.com',
        'zp-route-meta': meta
    }

    response_sy = requests.get(url='https://rd5.zhaopin.com/', headers=headers_sy, timeout=5)
    # str_response = str(response_sy)
    get_request_id = response_sy.headers.get('x-zp-request-id')
    # company_name="浙江中恩通信技术有限公司"
    # jl_id="Sj44dSm)xWMF(mfYcxSq)Q"
    now_time = str(int(time.time() * 1000))

    headers_1 = {
        'User-Agent': get_useragent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        # 'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': cookie,
        # 'Cookie':'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
        'Host': 'rd5.zhaopin.com',
    }

    request_id = get_reqid(get_request_id)
    urlxxx = 'https://rd5.zhaopin.com/api/rd/assets/summary?_={}&isNewList=true&x-zp-page-request-id={}'.format(
        now_time, request_id)
    url_id = "https://rd5.zhaopin.com/api/rd/assets/balance?_={}&x-zp-page-request-id={}".format(now_time, request_id)
    xz_cs_url = 'https://rd5.zhaopin.com/api/rd/assets/balance/download?_={}&x-zp-page-request-id={}'.format(now_time,
                                                                                                             request_id)
    print(urlxxx)
    response_sx = requests.get(url=urlxxx, headers=headers_1, timeout=5).text
    str_response = str(response_sx)
    dianshu_dic = json.loads(str_response)
    # 下载次数， 智联币
    print(dianshu_dic['data']['assets']['normalDownload'], dianshu_dic['data']['coins']['balance'])
    return zlb_sl


#询问函数
def ask_new(jls, orgid, jobid):
    flag = True
    today=str(datetime.date.today())
    resp_li_all = []
    now_num = len(jls)
    # print(now_num)
    if now_num == 0:
        flag = False
    # 余数
    ys = now_num % 10
    if ys != 0:
        cs = int(now_num / 10) + 1
    else:
        cs = int(now_num / 10)
    # print(cs)
    # 每个页面，询问次数
    for i in range(1, cs + 1):
        if i == 1 and flag:
            pos = []
            Towu_jl = []
            jl_d = 1
            if now_num >= 10:
                li_en = jls[0:i * 10]
            else:
                li_en = jls
            for jl in li_en:
                try:
                    modifyDate = "20" + jl["modifyDate"]
                    if modifyDate == today:
                        content = {}
                        content['orgId'] = orgid   # 企业id
                        content['jobId'] = jobid
                        content['channel'] = 1
                        # content['channelUpdateTime'] = td_date
                        content['channelResumeId'] = jl["id"]
                        content['downloadStatus'] = 0
                        content['resumeType'] = 2
                        Towu_jl.append(content)
                    else:
                        flag = False
                except:
                        pos.append(len(Towu_jl))
                        content = {}
                        content['orgId'] = orgid
                        content['jobId'] = '000'
                        content['channel'] = 1
                        content['channelUpdateTime'] = '2018-01-01'
                        content['channelResumeId'] = '111111'
                        content['downloadStatus'] = 1
                        content['resumeType'] = 1
                        Towu_jl.append(content)

            #print(Towu_jl)
            # 将dict类型的数据转成str
            data = json.dumps(Towu_jl)
            data = data.encode('utf-8')
            resp_page = requests.post(url=wu_jlxw_url, data=data)
        elif 1 < i < cs and flag:
            pos = []
            jl_d = i
            Towu_jl = []
            for jl in jls[(i - 1) * 10:i * 10]:
                try:

                    modifyDate = "20" + jl["modifyDate"]
                    if modifyDate == today:
                        content = {}
                        content['orgId'] = orgid
                        content['jobId'] = jobid
                        content['channel'] = 1
    #                     content['channelUpdateTime'] = td_date
                        content['channelResumeId'] = jl["id"]
                        content['downloadStatus'] = 0
                        content['resumeType'] = 2
                        Towu_jl.append(content)
                    else:
                        flag = False
                except:
                    pos.append(len(Towu_jl))
                    content = {}
                    content['orgId'] = orgid
                    content['jobId'] = '000'
                    content['channel'] = 1
                    content['channelUpdateTime'] = '2018-01-01'
                    content['channelResumeId'] = '111111'
                    content['downloadStatus'] = 1
                    content['resumeType'] = 1
                    Towu_jl.append(content)
                # print(Towu_jl)
                # 将dict类型的数据转成str
            data = json.dumps(Towu_jl)
            data = data.encode('utf-8')
            resp_page = requests.post(url=wu_jlxw_url, data=data)
        elif i == cs and flag:
            pos = []
            jl_d = i
            Towu_jl = []
            for jl in jls[(i - 1) * 10:]:
                try:
                    # info_ele = jl.xpath('./td[@class="Common_list_table-id-text"]/span/@id')[0]
                    # chanl_id = info_ele.split('spanB')[1]
                    # td_date = jl.xpath('./td[9]/text()')[0]
                    modifyDate = "20" + jl["modifyDate"]
                    if modifyDate == today:
                        content = {}
                        content['orgId'] = orgid
                        content['jobId'] = jobid
                        content['channel'] = 1
                        # content['channelUpdateTime'] = today
                        content['channelResumeId'] = jl["id"]
                        content['downloadStatus'] = 0
                        content['resumeType'] = 2
                        Towu_jl.append(content)
                    else:
                        flag = False
                except:
                    pos.append(len(Towu_jl))
                    content = {}
                    content['orgId'] = orgid
                    content['jobId'] = '000'
                    content['channel'] = 1
                    content['channelUpdateTime'] = '2018-01-01'
                    content['channelResumeId'] = '111111'
                    content['downloadStatus'] = 1
                    content['resumeType'] = 1
                    Towu_jl.append(content)
    #             # print(Towu_jl)
    #             # 将dict类型的数据转成str
            data = json.dumps(Towu_jl)
            data = data.encode('utf-8')
            resp_page = requests.post(url=wu_jlxw_url, data=data)
        # resp_page = [1]
        xd = resp_page.text
            # print(xd)
            # print(Towu_jl)
        xxx = xd.replace(', ', '-').replace(' ', '').replace('[', '').replace(']', '')
        resp_li = xxx.split('-')
        resp_li_all.extend(resp_li)
        # resp_li = ['1', '1', '1']
    return resp_li_all

#简历关键字搜索
def jl_sou_suo(cookie,meta,tj_data,job_id,orgid):
    page_num=0
    yxz_num = 0
    # key_word=tj_data["keyWord"]
    dict_city = {'赣榆县': '3089', '桐庐县': '2241', '淄川区': '3029', '盐都区': '3072', '嘉兴': '656', '宜良县': '3267', '长海县': '2397',
                 '龙门县': '3257', '江岸区': '2057', '沣西新城': '3361', '辽中县': '2384', '衡阳': '752', '马山县': '3155', '武穴': '10139',
                 '栾川县': '3334', '嵩县': '3332', '昌江': '10195', '普兰店市': '2394', '滨海县': '3075', '福州': '681', '六盘水': '823',
                 '侯马': '3279', '吴忠': '888', '金堂县': '2118', '德惠市': '2389', '陕西': '556', '通河县': '2431', '昔阳县': '3284',
                 '扬州': '645', '泾河新城': '3363', '云南': '554', '驻马店': '735', '麻涌镇': '3236', '九江': '694', '新建区': '2542',
                 '南通': '641', '太仓市': '911', '沙河口区': '2183', '长安镇': '3251', '临海市': '3130', '晋城': '580', '庐阳区': '2352',
                 '鼓楼区': '2251', '南关区': '2140', '福田区': '2037', '安宁区': '3352', '淄博高新': '3032', '兴城': '10023',
                 '泉山区': '3052', '仙桃': '10168', '武威': '869', '点军区': '3347', '高碑店市': '3320', '邕宁区': '3152', '六合区': '2091',
                 '兴业县': '3179', '景宁县': '3142', '新乡': '725', '永济市': '910', '滨江区': '2238', '濠江区': '3218', '宜春': '699',
                 '海盐县': '3123', '天河区': '2048', '平潭县': '2261', '龙华区': '3144', '楚州区': '3081', '莱州市': '2552', '阳泉': '578',
                 '浙江': '540', '合浦县': '3172', '杨凌': '10470', '江东区': '3004', '大亚湾区': '3254', '黑龙江': '537', '绵阳': '806',
                 '海门市': '3048', '辽宁': '535', '辽源': '616', '陆川县': '3177', '南朗镇': '3203', '龙华新区': '2361', '鄢陵县': '3343',
                 '浦口区': '2090', '定安': '10188', '奎屯市': '10164', '本溪': '603', '广元': '807', '乌兰察布': '596', '南沙区': '2054',
                 '黄冈': '745', '巴音郭楞': '896', '平山县': '2301', '阿坝': '819', '保税区': '2391', '西湖区': '2537', '阿克苏': '897',
                 '睢宁县': '3056', '滨湖区': '2517', '灌南县': '3092', '汝阳县': '3337', '金湾区': '3182', '塔城': '902', '黔西南': '827',
                 '钦州': '791', '海阳市': '2556', '洋浦市/': '907', '西岗区': '2181', '廊坊': '574', '桥西区': '2290', '江干区': '2235',
                 '和顺县': '3283', '马鞍山': '668', '桑海经济': '3307', '神农架': '10179', '苏家屯区': '2135', '兴安盟': '594',
                 '寿光市': '3013', '雁塔区': '2073', '观山湖区': '2524', '文登区': '4010', '开发区': '2558', '漯河': '729',
                 '无锡新区': '2518', '开阳县': '2530', '巴彦淖尔': '597', '苏州': '639', '东湖区': '2536', '海曙区': '3003', '缙云县': '3137',
                 '亭湖区': '3071', '万柏林区': '2505', '开平市': '3213', '朝阳': '611', '启东市': '3395', '开原': '10144', '祁县': '3287',
                 '双城': '10159', '扬中市': '3393', '蓝田县': '2079', '石龙镇': '3225', '天台县': '3127', '峨眉': '10065',
                 '招远市': '2554', '葫芦岛': '612', '德宏': '842', '东升镇': '3198', '阜阳': '674', '武汉吴家': '2367', '绥化': '633',
                 '宿州': '675', '晋宁县': '3265', '云岩区': '2521', '三水区': '2534', '仪征市': '3065', '保山': '834', '宁夏': '559',
                 '阜新': '607', '绿园区': '2144', '城关区': '3350', '白银': '867', '锦江区': '2108', '郑州': '719', '七台河': '630',
                 '裕华区': '2292', '临夏': '876', '北流市': '3175', '临潼区': '2078', '恩平市': '3215', '高港区': '3068', '清溪镇': '3244',
                 '厦门': '682', '宁德': '690', '日照': '712', '三亚': '800', '政务文化': '2437', '石岐区': '3188', '河北': '532',
                 '南阳': '731', '同安区': '2268', '美兰区': '3146', '翔安区': '2269', '龙口市': '2550', '阿拉善盟': '598', '安丘市': '3017',
                 '淮阴区': '3082', '寮步镇': '3234', '渭北工业': '3278', '公安': '10057', '金坛区': '3043', '玄武区': '2084',
                 '普洱': '10163', '鹰潭': '696', '哈密': '893', '石狮市': '3100', '万宁': '10186', '常州': '638', '盱眙县': '3398',
                 '德阳': '805', '昌都': '848', '自贡': '802', '金平区': '3217', '渭南': '858', '珲春': '10198', '贺州': '795',
                 '沈北新区': '2134', '方正县': '2426', '郫都区': '2117', '邯郸': '568', '哈尔滨': '622', '长丰县': '3275', '工业园区': '2218',
                 '石河子': '10061', '丹徒区': '3061', '新城区': '2070', '建德市': '2409', '德清县': '3388', '德化县': '3099', '漳州': '687',
                 '永嘉县': '3384', '大理': '841', '汉中': '860', '黄陂区': '2068', '西区': '3189', '南昌县': '2541', '西安国家': '2373',
                 '泰州': '647', '西咸新区': '933', '武汉': '736', '青羊区': '2107', '安顺': '825', '梅州': '774', '林芝': '853',
                 '泰顺县': '3114', '七里河区': '3351', '滨州': '717', '山东': '544', '新民市': '2383', '榆树市': '2387', '巴彦县': '2429',
                 '新都区': '2114', '经济开发': '4011', '江苏': '539', '安吉县': '3134', '涧西区': '3324', '长兴县': '3133',
                 '公主岭': '10122', '遵义': '824', '琼山区': '3145', '眉山': '812', '黄南': '881', '大厂回族': '3316', '湛江': '770',
                 '宁海县': '3372', '萧山区': '2239', '荆州': '744', '洛宁县': '3333', '陇南': '875', '温岭市': '3129', '昌乐县': '3014',
                 '广州': '763', '东陵区（': '2132', '铁山港区': '3171', '文山': '838', '昭通': '835', '东莞': '779', '二七区': '2195',
                 '微山县': '3021', '河池': '796', '广东': '548', '彭州市': '2379', '汕头': '767', '蓬江区': '3210', '叠彩区': '3164',
                 '满城区': '3321', '唐山': '566', '浐灞生态': '2371', '新疆': '560', '海西': '885', '锦州': '605', '农安县': '2390',
                 '惠城区': '2246', '迎泽区': '2502', '北屯市': '932', '永春县': '3098', '钟楼区': '3039', '开封': '720', '江北区': '3005',
                 '鄂州': '741', '镇海区': '3007', '襄城县': '3344', '涟水县': '3084', '栖霞区': '2092', '忻州': '584', '江夏区': '2067',
                 '新乐市': '2298', '永康市': '3378', '曲阜市': '3019', '道里区': '2271', '东川区': '3263', '崂山区': '2158',
                 '东湖新技': '2366', '海城': '10070', '上城区': '2233', '永登县': '3355', '闽侯县': '2256', '伊川县': '3336',
                 '广德': '10181', '阿勒泰': '903', '台湾省': '563', '增城区': '2475', '海北': '880', '西工区': '3327', '南昌经济': '3304',
                 '潮州': '781', '柳河县': '4005', '北仑区': '3006', '涿州市': '3318', '经开区': '2203', '汶上县': '3025', '高陵县': '2082',
                 '临汾': '585', '景德镇': '692', '寻甸县': '3271', '萍乡': '693', '莲都区': '3135', '深圳': '765', '金州区': '2188',
                 '洛阳': '721', '琼海': '10153', '石碣镇': '3224', '通化': '617', '城中区': '3159', '红河': '837', '青岛高新': '2393',
                 '咸阳': '857', '金湖县': '3086', '青云谱区': '2538', '诸城市': '3016', '宣城': '680', '行唐县': '2413', '响水县': '3074',
                 '依兰县': '2427', '甘肃': '557', '包头': '588', '诸暨市': '3387', '长清区': '2102', '胶州市': '2160', '乌当区': '2526',
                 '道外区': '2272', '楚雄': '836', '黄江镇': '3242', '铜川': '855', '博尔塔拉': '895', '梧州': '788', '尖草坪区': '2504',
                 '嵊州市': '3106', '思明区': '2264', '锡林郭勒': '595', '浏阳市': '2408', '泉港区': '3400', '清徐县': '2507',
                 '洛龙区': '3325', '衡水': '575', '长葛县': '3406', '木兰县': '2430', '铁岭': '610', '秦汉新城': '3362', '舟山': '661',
                 '官渡区': '3261', '呼和浩特': '587', '甘孜': '820', '甘井子区': '2184', '平凉': '871', '环翠区': '4009', '未央区': '2074',
                 '海州区': '3088', '虎门镇': '3248', '民众镇': '3202', '小店区': '2501', '古交市': '2510', '青岛': '703', '长兴岛': '2398',
                 '威海': '711', '长治': '579', '临淄区': '3031', '宿松': '10182', '洞头区': '3110', '桂林': '787', '阎良国家': '2372',
                 '任城区': '3018', '永泰县': '2259', '宜兴市': '2513', '合肥': '664', '株洲': '750', '海东': '879', '普宁': '3404',
                 '龙湖区': '3216', '泰兴市': '3397', '西乡塘区': '3150', '昆明': '831', '高邑县': '2418', '夷陵区': '3349', '溧水区': '2095',
                 '吉林': '536', '平度市': '2162', '丰县': '3054', '揭阳': '782', '吴兴区': '3131', '宜城': '10171', '云龙区': '3050',
                 '通化县': '4003', '长沙县': '2406', '庆阳': '873', '铁西区': '2130', '淮南': '667', '天心区': '2225', '商丘': '732',
                 '莱芜': '713', '福建': '542', '焦作': '726', '湘西': '762', '瑞安市': '3385', '湾里区': '2540', '云和县': '3140',
                 '攀枝花': '803', '姑苏区': '2511', '金东区': '3116', '成都': '801', '红谷滩新': '3302', '盐田区': '2040', '江汉区': '2058',
                 '香港': '561', '滁州': '673', '肇东市': '10510', '岳麓区': '2226', '惠州': '773', '荔湾区': '2047', '盘龙区': '3260',
                 '三河市': '3310', '吴中区': '2216', '霸州市': '3309', '嵩明县': '3269', '汽车产业': '2147', '安国市': '3319',
                 '松阳县': '3139', '越秀区': '2045', '南长区': '2515', '龙泉驿区': '2112', '吐鲁番': '892', '巢湖市': '3277', '阳江': '777',
                 '高邮市': '3396', '西安': '854', '鱼峰区': '3160', '丽江': '843', '嘉祥县': '3024', '滨湖新区': '2357', '秦淮区': '2086',
                 '高新园区': '2185', '娄底': '761', '丰泽区': '3094', '东区': '3186', '东营': '706', '余姚市': '3371', '东凤镇': '3195',
                 '福山区': '2546', '虎丘区': '2215', '连云区': '3087', '鹿泉区': '2299', '米东区': '3297', '吉安': '698', '灌云县': '3091',
                 '息烽县': '2529', '仲恺区': '3253', '浦江县': '3118', '凉山': '821', '芜湖': '665', '西双版纳': '840', '西昌': '10104',
                 '如东县': '3047', '锡山区': '2520', '阜宁县': '3076', '南安市': '3102', '瑶海区': '2353', '如皋市': '3394',
                 '昌图': '10080', '安宁市': '3272', '南昌高新': '3305', '呼伦贝尔': '593', '经济技术': '2356', '高明区': '2535',
                 '云浮': '783', '贵州': '553', '常熟': '650', '四川': '552', '青岛经济': '2392', '文成县': '3113', '斗门区': '3181',
                 '隆安县': '3154', '金水区': '2197', '台山市': '3403', '空港新城': '3364', '亳州': '678', '孟津县': '3335', '金牛区': '2109',
                 '进出口加': '4013', '双阳区': '2148', '泗水县': '3026', '高埗镇': '3238', '都江堰市': '2380', '济宁': '709',
                 '二道江区': '4002', '克拉玛依': '891', '蒲江县': '2120', '临港经济': '4014', '丽水': '663', '大兴安岭': '634',
                 '句容市': '3391', '小榄镇': '3197', '罗源县': '2257', '延边': '621', '和田': '900', '遵化': '10143', '闽清县': '2260',
                 '蚌埠': '666', '淄博': '704', '登封市': '2400', '黔东南': '829', '大鹏新区': '2362', '靖江市': '3390', '曲靖': '832',
                 '伊滨区': '3329', '南湖区': '3121', '喀什': '899', '高新区': '3330', '于洪区': '2133', '阳曲县': '2508', '延寿县': '2432',
                 '百色': '794', '郴州': '758', '烟台': '707', '怒江': '844', '黄石': '737', '南昌临空': '3303', '襄阳': '740',
                 '许昌县': '3341', '皋兰县': '3356', '惠安县': '3096', '瓯海区': '3109', '乐东': '10196', '鄂尔多斯': '592',
                 '江都区': '3064', '承德': '572', '淳安县': '2242', '福安': '3401', '海南': '550', '石排镇': '3227', '伍家岗区': '3346',
                 '雨花台区': '2093', '六安': '677', '安阳': '723', '咸宁': '746', '白山': '618', '崇川区': '3044', '金乡县': '3023',
                 '广陵区': '3063', '毕节': '828', '池州': '679', '恩施': '748', '随州': '747', '大岭山镇': '3240', '九台市': '2388',
                 '七星区': '3166', '防城港': '790', '三门县': '3375', '越城区': '3103', '鹤壁': '724', '长岛县': '2549', '惠阳区': '2247',
                 '惠东县': '3256', '保亭': '10193', '沛县': '3055', '三角镇': '3201', '樟木头镇': '3239', '建邺区': '2087',
                 '猇亭区': '3348', '汉南区': '2066', '兰溪市': '3120', '横县': '3158', '梁山县': '3027', '进贤县': '2543', '花都区': '2051',
                 '新昌县': '3105', '西海岸新': '3009', '邹城市': '3020', '洛江区': '3095', '磐安县': '3119', '江宁区': '2094',
                 '新沂市': '3057', '正定县': '2300', '宜宾': '813', '大东区': '2129', '南岗区': '2270', '福绵区': '3174', '来宾': '904',
                 '天桥区': '2099', '从化区': '2474', '修文县': '2528', '赞皇县': '2419', '松北区': '2274', '齐齐哈尔': '623', '崇左': '905',
                 '连云港': '642', '香坊区': '2273', '宜昌': '739', '南充': '811', '白城': '620', '遂宁': '808', '中山区': '2182',
                 '硚口区': '2059', '鞍山': '601', '温江区': '2115', '青秀区': '3148', '禹州县': '3342', '蔡甸区': '2064', '黄山': '672',
                 '遂昌县': '3138', '文昌': '10185', '大涌镇': '3205', '海口': '799', '菏泽': '718', '杏花岭区': '2503', '沣东新城': '3360',
                 '二道区': '2143', '管城区': '2196', '丹阳市': '3392', '平房区': '2275', '运城': '583', '井陉县': '2420', '谢岗镇': '3231',
                 '金昌': '866', '雨花区': '2228', '溧阳市': '3042', '银川': '886', '贾汪区': '3051', '新站综合': '2358', '临沂': '714',
                 '神湾镇': '3208', '新密市': '2401', '无极县': '2416', '南海区': '2562', '集美区': '2266', '富阳区': '2478',
                 '市北区（': '2154', '莞城区': '3220', '沙田镇': '3245', '石林彝族': '3268', '杭州': '653', '阎良区': '2077',
                 '西山区': '3262', '河源': '776', '淮安': '643', '象山县': '3373', '义乌市': '3376', '汉阳区': '2060', '即墨市': '2161',
                 '兴化市': '3070', '常德': '755', '迪庆': '845', '碑林区': '2071', '瓦房店市': '2395', '台州': '662', '太谷县': '3286',
                 '甘南': '877', '柯桥区': '3104', '鸡西': '624', '老城区': '3326', '沙溪镇': '3206', '衢州': '660', '姜堰区': '3069',
                 '固原': '889', '望牛墩镇': '3241', '天水': '868', '坪山新区': '2043', '双流区': '2116', '东阳市': '3377', '巩义市': '2444',
                 '赣州': '697', '双鸭山': '626', '牟平区': '2547', '昆山': '640', '新余': '695', '马尾区': '2254', '山西': '533',
                 '铜仁': '826', '江南区': '3149', '南京': '635', '板芙镇': '3192', '达阪城区': '3298', '吕梁': '586', '松山湖区': '3252',
                 '雁山区': '3167', '婺城区': '3115', '海沧区': '2267', '崇州市': '2378', '万江区': '3223', '荣成市': '3368',
                 '罗湖区': '2038', '安溪县': '3097', '高淳区': '2096', '长沙': '749', '新安县': '3338', '武昌区': '2061', '南区': '3187',
                 '横琴新区': '3183', '李沧区': '2156', '五家渠': '10178', '阿拉尔': '10176', '灵石县': '3289', '鱼台县': '3022',
                 '秀英区': '3143', '克孜勒苏': '898', '酒泉': '872', '灵寿县': '2414', '日喀则': '850', '龙湾区': '3108', '南昌': '691',
                 '历城区': '2101', '济南': '702', '定西': '874', '莱山区': '2548', '坦洲镇': '3209', '南平': '688', '龙岗区': '2042',
                 '东坑镇': '3232', '秀峰区': '3163', '天府新区': '3300', '江门': '769', '道滘镇': '3246', '内江': '809', '城阳区': '2159',
                 '雅安': '816', '左权县': '3282', '兰州新区': '3358', '莱阳市': '2551', '兴平': '10058', '宁乡县': '2407', '邢台': '569',
                 '火炬开发': '3191', '兰州': '864', '泰安': '710', '榆次区': '3280', '临朐县': '4008', '武汉经济': '2365', '清镇市': '2527',
                 '安庆': '671', '东城区': '3222', '澳门': '562', '博白县': '3178', '潜江': '10169', '思茅': '3402', '惠山区': '2519',
                 '永清县': '3311', '海安县': '3046', '惠济区': '2198', '徐州': '637', '金华': '659', '图木舒克': '10177', '肥东县': '3273',
                 '肇庆': '772', '信阳': '733', '南宁': '785', '黑河': '632', '邗江区': '3062', '广西': '549', '水磨沟区': '3293',
                 '邳州市': '3058', '新津县': '2121', '龙川': '3405', '肥城市': '3369', '塘厦镇': '3247', '福清': '2473', '黔南': '830',
                 '秦皇岛': '567', '乌苏': '10166', '达州': '815', '柳州': '786', '乌审旗': '10031', '呼兰区': '2276', '燕郊开发': '3317',
                 '企石镇': '3228', '周口': '734', '许昌': '728', '张店区': '3028', '榆中县': '3357', '贵港': '792', '德州': '715',
                 '宝安区': '2041', '兴宁区': '3147', '台江区': '2252', '常平镇': '3233', '湘潭': '751', '宾阳县': '3157', '佛山': '768',
                 '濮阳': '727', '石嘴山': '887', '天宁区': '3038', '滨海经济': '3011', '张家港': '652', '慈溪市': '3370', '茂名': '771',
                 '新会区': '3212', '天山区': '3295', '新市区': '3292', '高密市': '3012', '张掖': '870', '蜀山区': '2354', '南浔区': '3132',
                 '成华区': '2111', '集安市': '4007', '宁波': '654', '康平县': '2385', '通州区': '3399', '鹿城区': '3107', '榆社县': '3281',
                 '辛集市': '2295', '阿城区': '2277', '东开发区': '2293', '宝鸡': '856', '中山': '780', '禄劝县': '3270', '南昌望城': '3308',
                 '南山区': '2039', '绍兴': '658', '路桥区': '3126', '果洛': '883', '海南州': '882', '连江县': '2258', '灞桥区': '2075',
                 '望城区': '2405', '中原区': '2194', '肥西县': '3274', '旅顺口区': '2187', '乳山市': '3367', '章丘市': '2471',
                 '武侯区': '2110', '永州': '759', '大城县': '3314', '方家山': '10158', '晋中': '582', '海宁市': '3382', '东昌区': '4001',
                 '安达': '10081', '青田县': '3136', '西藏': '555', '莲湖区': '2072', '荆门': '742', '朔州': '581', '航空港区': '2445',
                 '贵阳': '822', '中堂镇': '3237', '三明': '684', '青山湖区': '2539', '魏都区': '3340', '法库县': '2386', '朝阳区': '2142',
                 '盘锦': '609', '晋源区': '2506', '沈阳': '599', '泸州': '804', '历下区': '2098', '清远': '778', '昌吉': '894',
                 '三乡镇': '3207', '长安区': '2288', '丹东': '604', '芙蓉区': '2224', '元氏县': '2302', '榆林': '861', '淮北': '669',
                 '定州市': '3323', '余杭区': '2240', '椒江区': '3124', '鲤城区': '3093', '辉南县': '4004', '武鸣区': '3153',
                 '高新西区': '3301', '四平': '615', '营口': '606', '洪山区': '2063', '拉萨': '847', '湖南': '547', '西宁': '878',
                 '曲江新区': '2370', '宝应县': '3066', '吴江区': '2561', '白沙': '10194', '宿迁': '648', '巴中': '817', '孝感': '743',
                 '岳阳': '754', '棋盘山开': '2382', '南明区': '2522', '济源': '10044', '乐山': '810', '龙泉市': '3389', '射阳县': '3077',
                 '湖北': '546', '宽城区': '2141', '大庆': '627', '张家口': '571', '周至县': '2080', '张家界': '756', '厚街镇': '3249',
                 '海城区': '3169', '高新开发': '2145', '伊春': '628', '桐乡市': '3381', '拱墅区': '2236', '嘉峪关': '865', '沙依巴克': '3294',
                 '东港': '931', '禅城区': '2531', '博山区': '3030', '建湖县': '3078', '阿里': '852', '青山区': '2062', '博罗县': '3255',
                 '新洲区': '2069', '呈贡区': '3264', '资阳': '818', '长乐': '2472', '济阳县': '2104', '介休市': '3290', '港闸区': '3045',
                 '良庆区': '3151', '镇江': '646', '屯昌': '10189', '红古区': '3354', '聊城': '716', '满洲里': '10157', '西陵区': '3345',
                 '牡丹江': '631', '沧州': '573', '鄞州区': '3002', '新北区': '3040', '怀化': '760', '延安': '859', '香河市': '3313',
                 '石家庄': '565', '鹤山市': '3214', '栾城区': '2412', '湖州': '657', '光明新区': '2044', '五华区': '3259', '安义县': '2544',
                 '花溪区': '2523', '润州区': '3060', '龙岩': '689', '伊犁': '901', '香洲区': '3180', '南城区': '3221', '乌鲁木齐': '3299',
                 '武义县': '3117', '临沧': '846', '户县': '2081', '京口区': '3059', '大邑县': '2119', '庄河市': '2396', '武进区': '3041',
                 '五指山': '10184', '青州市': '3015', '包河区': '2355', '火炬高技': '4012', '玉树': '884', '临安市': '2479',
                 '阜沙镇': '3196', '玉环县': '3374', '晋州市': '2297', '长春': '613', '益阳': '757', '秀洲区': '3122', '新郑市': '2399',
                 '市中区': '2097', '东西湖区': '2065', '宜阳县': '3339', '东海县': '3090', '商河县': '2105', '荥阳市': '2402',
                 '吉利区': '3328', '仙居县': '3128', '上街区': '2205', '芝罘区': '2545', '黄圃镇': '3193', '那曲': '851', '偃师市': '3331',
                 '汕尾': '775', '萝岗区': '2053', '琼中': '10192', '玉州区': '3173', '梅河口市': '4006', '抚顺': '602', '内蒙古': '534',
                 '横沥镇': '3229', '松原': '619', '中卫': '906', '平阳县': '3111', '高新技术': '3010', '上饶': '701', '奉化区': '3001',
                 '乐清市': '3383', '南海新区': '4015', '容县': '3176', '桥头镇': '3230', '河南': '545', '仓山区': '2253', '赵县': '2417',
                 '苍南县': '3112', '通辽': '591', '海珠区': '2046', '保定': '570', '湖里区': '2265', '藁城区': '2296', '顺德区': '2560',
                 '潍坊': '708', '大连': '600', '嘉善县': '3380', '井陉矿区': '2294', '韶关': '764', '吉林市': '614', '玉溪': '833',
                 '南昌小蓝': '3306', '潮阳区': '3219', '黄岛区（': '2157', '安康': '862', '海陵区': '3067', '凤阳': '10069',
                 '下城区': '2234', '五桂山区': '3190', '铜陵': '670', '临桂区': '3168', '鲅鱼圈': '3034', '江海区': '3211',
                 '青白江区': '2113', '横栏镇': '3200', '北塘区': '2516', '新华区': '2291', '山南': '849', '鹤岗': '625', '儋州': '10183',
                 '胶南区': '2163', '大朗镇': '3235', '青海': '558', '洪梅镇': '3243', '深泽县': '2415', '兖州区': '3366', '珠海': '766',
                 '莱西市': '2164', '北城新区': '2438', '西固区': '3353', '江阴市': '2512', '广安': '814', '蓬莱市': '2553', '商洛': '863',
                 '大石桥': '3035', '莆田': '683', '五常市': '2424', '晋江市': '3101', '陵水': '10197', '简阳': '10201', '开福区': '2227',
                 '平湖市': '3379', '临高': '10191', '枣庄': '705', '头屯河区': '3296', '象山区': '3165', '崇安区': '2514', '固安市': '3312',
                 '西平': '10059', '市南区': '2153', '茶山镇': '3226', '抚州': '700', '三门峡': '730', '娄烦县': '2509', '槐荫区': '2100',
                 '黄埔区': '2050', '青浦区': '3083', '温州': '655', '绥芬河': '10161', '沈河区': '2127', '清苑区': '3322', '北海': '789',
                 '十堰': '738', '柳北区': '3162', '澄迈': '10190', '下沙': '2457', '白云区': '2525', '大丰区': '3073', '平阴县': '2103',
                 '辽阳': '608', '铜山区': '3053', '柳南区': '3161', '庆元县': '3141', '黄岩区': '3125', '邵阳': '753', '上虞区': '3386',
                 '晋安区': '2255', '无锡': '636', '庐江县': '3276', '文安县': '3315', '皇姑区': '2128', '玉林': '793', '和平区': '2126',
                 '古镇镇': '3199', '寿阳县': '3285', '郑东新区': '2199', '港口镇': '3204', '赤峰': '590', '栖霞市': '2555', '佳木斯': '629',
                 '邛崃市': '2377', '上林县': '3156', '安徽': '541', '凤岗镇': '3250', '太原': '576', '国际港务': '2374', '平遥县': '3288',
                 '天门': '10140', '东方': '10187', '乌海': '589', '平顶山': '722', '泉州': '685', '东台市': '3079', '番禺区': '2052',
                 '宾县': '2428', '大同': '577', '南头镇': '3194', '洪泽县': '3085', '相城区': '2217', '中牟县': '2403', '富民县': '3266',
                 '尚志': '10160', '清河区': '3080', '盐城': '644', '银海区': '3170', '江西': '543', '徐汇区': '2021', '嘉定区': '2030',
                 '九龙坡区': '2316', '铜梁区': '2334', '蓟县': '2180', '渝中区': '2312', '南开区': '2168', '巴南区': '2319',
                 '静海县': '2178', '虹口区': '2026', '北京': '530', '石景山区': '2008', '长寿区': '2325', '双桥区': '2328', '武隆县': '2347',
                 '丰都县': '2342', '青浦区': '2034', '密云县': '2017', '河北区': '2169', '红桥区': '2170', '门头沟区': '2016',
                 '滨海新区': '2171', '通州区': '2009', '东丽区': '2172', '房山区': '2011', '江北区': '2313', '江津区': '2326',
                 '西城区': '2002', '河东区': '2166', '平谷区': '2015', '和平区': '2165', '昌平区': '2013', '崇文区': '2003',
                 '秀山土家': '2434', '海淀区': '2005', '壁山区': '2333', '重庆': '551', '沙坪坝区': '2315', '宣武区': '2004', '开县': '2338',
                 '南川区': '2330', '黔江区': '2322', '金山区': '2032', '万盛区': '2329', '宁河县': '2179', '綦江区': '2336',
                 '河西区': '2167', '浦东新区': '2031', '闵行区': '2028', '北碚区': '2320', '石柱土家': '2433', '武清区': '2176',
                 '延庆县': '2018', '奉节县': '2343', '西青区': '2173', '潼南区': '2335', '大渡口区': '2317', '云阳县': '2339',
                 '松江区': '2033', '黄浦区': '2019', '北辰区': '2175', '崇明区': '2036', '怀柔区': '2014', '渝北区': '2318',
                 '杨浦区': '2027', '宝山区': '2029', '顺义区': '2010', '涪陵区': '2324', '东城区': '2001', '丰台区': '2007',
                 '朝阳区': '2006', '大足区': '2332', '巫山县': '2344', '南岸区': '2314', '万州区': '2321', '上海': '538', '荣昌区': '2331',
                 '奉贤区': '2035', '长宁区': '2022', '永川区': '2323', '天津': '531', '大兴区': '2012', '北部新区': '2360',
                 '酉阳土家': '2435', '垫江县': '2341', '静安区': '2023', '津南区': '2174', '忠县': '2337', '合川区': '2327',
                 '彭水苗族': '2436', '宝坻区': '2177', '普陀区': '2024', '梁平县': '2340', '巫溪县': '2345', '城口县': '2346'
                 }
    # for pagnum in range(0, 4):
    #     page_num = pagnum
    flag=True
    while flag:
        try:
            pay_load = {
                "start": page_num,
                "rows": 30,
                "S_DISCLOSURE_LEVEL": 2,
                "S_ENGLISH_RESUME": "1",
                "isrepeat": 1,
                "sort": "date"}
            # 关键字，最近一家公司名称
            try:
                if tj_data["keyWord"] != "":
                    pay_load["S_KEYWORD"] = tj_data["keyWord"]
                if tj_data["nearCompany"] != "":
                    pay_load["S_COMPANY_NAME_ALL"] = tj_data["nearCompany"]
            except:
                pass
            # 居住地
            try:
                if tj_data["place"] != []:
                    list_jz_d = []
                    for place in tj_data["place"]:
                        jz_di = place.replace("'", "").split("#")[-1]
                        jz_num = dict_city[jz_di]
                        list_jz_d.append(jz_num)
                    pay_load["S_CURRENT_CITY"] = str(list_jz_d).replace(",", ";").replace("[", "").replace("]", "").replace("'",
                                                                                                                            "").replace(
                        '"', "")
            except:
                pass
            # 期望工作地点
            try:
                if tj_data["expectPlace"] != []:
                    list_qwd = []
                    for expectPlace in tj_data["expectPlace"]:
                        qw_di = expectPlace.replace("'", "").split("#")[-1]
                        qw_num = dict_city[qw_di]
                        # print(qw_num)
                        list_qwd.append(qw_num)
                    pay_load["S_DESIRED_CITY"] = str(list_qwd).replace(",", ";").replace("[", "").replace("]", "").replace("'",
                                                                                                                           "").replace(
                        '"', "")
            except:
                pass
            # 性别
            try:
                dict_sex = {'男': '1', '女': '2'}
                if tj_data["sex"]:
                    if tj_data["sex"] != "不限":
                        sex = tj_data["sex"]
                        pay_load["S_GENDER"] = dict_sex[sex]
            except:
                pass
            # 工作年限
            try:
                if tj_data["workLimit"] != []:
                    try:
                        workLimit = tj_data["workLimit"]
                        low_year = int(workLimit[0])
                        upper_year = int(workLimit[1])
                        now_year = str(datetime.date.today()).split("-")[0]
                        low_year_0 = int(now_year) - upper_year
                        upper_year_0 = int(now_year) - low_year
                        now_low = str(low_year_0) + str(datetime.date.today()).split("-")[1]
                        now_upper = str(upper_year_0) + str(datetime.date.today()).split("-")[1]
                        pay_load["S_WORK_YEARS"] = now_low + "," + now_upper
                    except:
                        pass
            except:
                pass
            # 期望薪资（需要对应的码表）
            try:
                xinzi = {"13": "100001150000", "12": "70001100000", "11": "5000170000", "10": "3500150000", "9": "2500135000",
                         "8": "1500125000", "7": "1000115000", "6": "0800110000", "5": "0600108000", "4": "0400106000",
                         "3": "0200104000", "2": "0100102000", "1": "0000001000", "0": "0000000000"}
                if tj_data["expectPay"] != "不限":
                    expectPay = tj_data["expectPay"]
                    pay_load["S_DESIRED_SALARY"] = xinzi[expectPay]
            except:
                pass
            # 更新日期（固定写成一周前）
            try:
                today = str(datetime.date.today()).replace("-", "").replace("20", "")
                qi_day = get_date(7)
                low_day = str(qi_day).split(" ")[0].replace("-", "").replace("20", "")
                # print(low_day)
                pay_load["S_DATE_MODIFIED"] = str(low_day) + "," + str(today)
            except:
                pass
            # 学历
            try:
                dict_de = {"0": "9", "1": "9", "2": "13", "3": "7", "4": "12", "5": "5", "7": "4", "9": "3", "11": "10",
                           "13": "11", "15": "1"}
                if tj_data["education"] != []:
                    education = tj_data["education"]
                    low_edu = dict_de[education[0]]
                    upper_edu = dict_de[education[1]]
                    pay_load["S_EDUCATION"] = low_edu + "," + upper_edu
            except:
                pass
            # 年龄
            try:
                if tj_data["age"] != []:
                    age_li = tj_data["age"]
                    low_year = int(age_li[0])
                    upper_year = int(age_li[1])
                    now_ye = str(datetime.date.today()).split("-")[0]
                    lo_ye = int(now_ye) - upper_year
                    up_ye = int(now_ye) - low_year
                    pay_load["S_BIRTH_YEAR"] = str(lo_ye) + "," + str(up_ye)
            except:
                pass
            # 语言
            try:
                dict_lan = {"英语": "1", "日语": "2", "法语": "3", "德语": "4", "俄语": "5", "韩语": "6", "西班牙语": "7", "葡萄牙语": "8",
                            "阿拉伯语": "9", "意大利语": "10", }
                if tj_data["language"] != "不限":
                    language = tj_data["language"]
                    pay_load["S_LANGUAGE_SKILL_ALL"] = dict_lan[language]
            except:
                pass
            # 工作状态
            try:
                dict_zhuta = {"离职": "1", "在职，可一个月内到岗": "2", "在职，不想换工作": "3", "在职，考虑换工作": "4", "应届毕业生": "5"}
                if tj_data["workStatus"] != "不限":
                    workStatus = tj_data["workStatus"]
                    pay_load["S_CURRENT_CAREER_STATUS"] = dict_zhuta[workStatus]
            except:
                pass
            # 公司名称
            try:
                company_name = login_judge_zl(cookie)[1]
                pay_load["S_EXCLUSIVE_COMPANY"] = company_name
            except:
                pass
            # 期望行业
            try:
                dict_hangye = {'能源/矿产/采掘/冶炼': '130000', '通信/电信/网络设备': '300100', '物流/仓储': '301100', 'IT服务(系统/数据/维护)': '160000',
                               '物业管理/商业中心': '140200', '保险': '180100', '石油/石化/化工': '120500', '广告/会展/公关': '200302',
                               '电子技术/半导体/集成电路': '160500',
                               '环保': '201200', '租赁服务': '300700', '交通/运输': '150000', '外包服务': '300300', '跨领域经营': '100100',
                               '耐用消费品（服饰/纺织/皮革/家具/家电）': '120200', '礼品/玩具/工艺美术/收藏品/奢侈品': '120800', '检验/检测/认证': '201300',
                               '政府/公共事业/非盈利机构': '200100',
                               '快速消费品（食品/饮料/烟酒/日化）': '120400', '贸易/进出口': '170500', '其他': '990000', '互联网/电子商务': '210500',
                               '计算机硬件': '160200',
                               '媒体/出版/影视/文化传播': '210300', '教育/培训/院校': '201100', '娱乐/体育/休闲': '200700', '医疗设备/器械': '121500',
                               '大型设备/机电设备/重工业': '129900', '银行': '300500', '加工制造（原料加工/模具）': '121100', '办公用品及设备': '120700',
                               '汽车/摩托车': '121000',
                               '家居/室内设计/装饰装潢': '140100', '仪器仪表及工业自动化': '121200', '航空/航天研究与制造': '300000', '酒店/餐饮': '200600',
                               '中介服务': '201400',
                               '旅游/度假': '200800', '信托/担保/拍卖/典当': '300900', '基金/证券/期货/投资': '180000', '学术/科研': '120600',
                               '农/林/牧/渔': '100000',
                               '通信/电信运营、增值服务': '160100', '电气/电力/水利': '130100', '医药/生物工程': '121300', '计算机软件': '160400',
                               '网络游戏': '160600',
                               '印刷/包装/造纸': '210600', '房地产/建筑/建材/工程': '140000', '医疗/护理/美容/保健/卫生服务': '121400',
                               '专业服务/咨询(财会/法律/人力资源等)': '200300',
                               '零售/批发': '170000'}
                if tj_data["industry"] != []:
                    list_hangye = []
                    for industry in tj_data["industry"]:
                        hang_ye = industry.replace("'", "").split("#")[-1]
                        hang_num = dict_hangye[hang_ye]
                        list_hangye.append(hang_num)
                    pay_load["S_DESIRED_INDUSTRY"] = str(list_hangye).replace(",", ";").replace("[", "").replace("]",
                                                                                                                 "").replace(
                        "'", "").replace('"', "")
            except:
                pass
            # 期望工作职能
            try:
                dict_zhi_n = {"parents": [["4010200", "0", "销售业务", "Sales"], ["7001000", "0", "销售管理", "Sales Management"],
                                          ["7002000", "0", "销售行政/商务", "Sales Administration"],
                                          ["4000000", "0", "客服/售前/售后技术支持", "Customer Service/Pre/Post-sales technical Support"],
                                          ["4082000", "0", "市场", "Marketing"], ["4084000", "0", "公关/媒介", "PR/Media"],
                                          ["7004000", "0", "广告/会展", "Advertising/Exhibition"],
                                          ["2060000", "0", "财务/审计/税务", "Accounting/Auditing/Taxation"],
                                          ["5002000", "0", "人力资源", "Human Resource"],
                                          ["3010000", "0", "行政/后勤/文秘", "Administration/Logistics/Secretary"],
                                          ["201300", "0", "项目管理/项目协调", "Project Management"],
                                          ["2023405", "0", "质量管理/安全防护", "Quality Control/Safety Protection"],
                                          ["1050000", "0", "高级管理", "Senior Management"],
                                          ["160000", "0", "软件/互联网开发/系统集成", "Software Development/System Integration"],
                                          ["160300", "0", "硬件开发", "Hardware Development"],
                                          ["160200", "0", "互联网产品/运营管理", "Internet Product/Operation Magagement"],
                                          ["160400", "0", "IT质量管理/测试/配置管理", "IT QA/Configuration Management"],
                                          ["200500", "0", "IT运维/技术支持", "IT Operation/Technical Support"],
                                          ["200300", "0", "IT管理/项目协调", "IT Management/Project Coordination"],
                                          ["5001000", "0", "电信/通信技术开发及应用", "Communication Technology/Application"],
                                          ["141000", "0", "房地产开发/经纪/中介", "Real Estate Development/Agent/Broker"],
                                          ["140000", "0", "土木/建筑/装修/市政工程", "Civil/Decoration/Municipal Engineering"],
                                          ["142000", "0", "物业管理", "Property Management"], ["2071000", "0", "银行", "Banking"],
                                          ["2070000", "0", "证券/期货/投资管理/服务", "Security/Futures/Investment Service"],
                                          ["7006000", "0", "保险", "Insurance"],
                                          ["200900", "0", "信托/担保/拍卖/典当", "Trust/Guarantee/Auction/Pawn Business"],
                                          ["4083000", "0", "采购/贸易", "Purchasing/Trade"],
                                          ["4010300", "0", "交通运输服务", "Traffic Service"],
                                          ["4010400", "0", "物流/仓储", "Logistics/Warehouse"],
                                          ["121100", "0", "生产管理/运营", "Production Management/Operation"],
                                          ["160100", "0", "电子/电器/半导体/仪器仪表", "Electronics/Semiconductor/Instrument"],
                                          ["7003000", "0", "汽车制造", "Automobile Manufacture"],
                                          ["7003100", "0", "汽车销售与服务", "Automobile Sales & Service"],
                                          ["5003000", "0", "机械设计/制造/维修", "Mechanical Design/Production/Maintenance"],
                                          ["7005000", "0", "服装/纺织/皮革设计/生产", "Apparels/Textiles/Leather Design/Production"],
                                          ["5004000", "0", "技工/操作工", "Skilled Worker"],
                                          ["121300", "0", "生物/制药/医疗器械", "Biotechnology/Pharmaceuticals/Medical Equipment"],
                                          ["120500", "0", "化工", "Chemical Industry"],
                                          ["2120000", "0", "影视/媒体/出版/印刷", "Films/Media/Publication/Printing"],
                                          ["2100708", "0", "艺术/设计", "Art/Design"],
                                          ["2140000", "0", "咨询/顾问/调研/数据分析", "Consultant/Research/Data Analysis"],
                                          ["2090000", "0", "教育/培训", "Education/Training"],
                                          ["2080000", "0", "律师/法务/合规", "Legal/Compliance"],
                                          ["2120500", "0", "翻译（口译与笔译）", "Translator/Interpreter"],
                                          ["5005000", "0", "商超/酒店/娱乐管理/服务", "Department Store/Hotel/Entertainment Service"],
                                          ["4040000", "0", "旅游/度假/出入境服务", "Tourism/Exit and Entry Service"],
                                          ["201100", "0", "烹饪/料理/食品研发", "Cooking/Food R&D"],
                                          ["2050000", "0", "保健/美容/美发/健身", "Health Care/Beauty/Hairdressing/Fitness"],
                                          ["2051000", "0", "医院/医疗/护理", "Hospital/Nursing/Nursing"],
                                          ["6270000", "0", "社区/居民/家政服务", "Community/Residents/Housekeeping Service"],
                                          ["130000", "0", "能源/矿产/地质勘查", "Energy/Mining/Geological Exploration"],
                                          ["2023100", "0", "环境科学/环保", "Environmental Science/Protection"],
                                          ["100000", "0", "农/林/牧/渔业", "Agriculture/Forestry/Animal Husbandry/Fishing"],
                                          ["200100", "0", "公务员/事业单位/科研机构",
                                           "Civil Servant/Public Organization/Scientific Institution"],
                                          ["5006000", "0", "实习生/培训生/储备干部", "Intern/Trainee/Associate Trainee"],
                                          ["200700", "0", "志愿者/社会工作者", "Volunteer/Social Worker"],
                                          ["300100", "0", "兼职/临时", "Part-time Jobs"], ["300200", "0", "其他", "Others"]],
                              "children": [[["006", "4010200", "销售代表", "Sales Representative"],
                                            ["008", "4010200", "客户代表", "Account Representative"],
                                            ["009", "4010200", "销售工程师", "Sales Engineer"],
                                            ["007", "4010200", "渠道/分销专员", "Channel Specialist"],
                                            ["925", "4010200", "区域销售专员/助理", "Regional Sales Specialist/Assistant"],
                                            ["933", "4010200", "业务拓展专员/助理", "BD Specialist/Assistant"],
                                            ["926", "4010200", "大客户销售代表", "KA Representative"],
                                            ["011", "4010200", "电话销售", "Tele Sales"],
                                            ["924", "4010200", "网络/在线销售", "Online Sales"],
                                            ["452", "4010200", "团购业务员", "Team Buying Sales"],
                                            ["927", "4010200", "销售业务跟单", "Merchandising Associate"],
                                            ["010", "4010200", "医药代表", "Medical Sales Representative"],
                                            ["2149", "4010200", "经销商", "Dealers"],
                                            ["2150", "4010200", "招商经理", "sponsorship manager"],
                                            ["2151", "4010200", "招商主管", "Lease Executive"],
                                            ["2152", "4010200", "招商专员", "Leasing Executive"],
                                            ["2153", "4010200", "会籍顾问", "member consultant"],
                                            ["018", "4010200", "其他", "Others"]], [["000", "7001000", "销售总监", "Sales Director"],
                                                                                  ["001", "7001000", "销售经理", "Sales Manager"],
                                                                                  ["002", "7001000", "销售主管",
                                                                                   "Sales Supervisor"],
                                                                                  ["845", "7001000", "客户总监",
                                                                                   "Account Director"],
                                                                                  ["004", "7001000", "客户经理", "Account Manager"],
                                                                                  ["548", "7001000", "客户主管",
                                                                                   "Account Supervisor"],
                                                                                  ["003", "7001000", "渠道/分销总监",
                                                                                   "Channel Director"],
                                                                                  ["453", "7001000", "渠道/分销经理/主管",
                                                                                   "Channel Manager/Supervisor"],
                                                                                  ["005", "7001000", "区域销售总监",
                                                                                   "Regional Sales Director"],
                                                                                  ["843", "7001000", "区域销售经理/主管",
                                                                                   "Regional Sales Manager/Supervisor"],
                                                                                  ["454", "7001000", "业务拓展经理/主管",
                                                                                   "BD Manager/Supervisor"],
                                                                                  ["660", "7001000", "大客户销售经理", "KA Manager"],
                                                                                  ["455", "7001000", "团购经理/主管",
                                                                                   "Team Buying Manager/Supervisor"],
                                                                                  ["844", "7001000", "医药销售经理/主管",
                                                                                   "Medical Sales Manager/Supervisor"],
                                                                                  ["458", "7001000", "其他", "Others"]],
                                           [["459", "7002000", "销售行政经理/主管", "Sales Admin Manager/Supervisor"],
                                            ["015", "7002000", "销售行政专员/助理", "Sales Admin Specialist/Assistant"],
                                            ["662", "7002000", "销售运营经理/主管", "Sales Operations Manager/Supervisor"],
                                            ["661", "7002000", "销售运营专员/助理", "Sales Operations Specialist/Assistant"],
                                            ["461", "7002000", "商务经理/主管", "Business Manager/Supervisor"],
                                            ["460", "7002000", "商务专员/助理", "Business Specialist/Assistant"],
                                            ["463", "7002000", "销售培训师/讲师", "Sales Trainer"],
                                            ["462", "7002000", "销售数据分析", "Sales Data Analysis"],
                                            ["2230", "7002000", "业务分析经理/主管", "business analysis manager"],
                                            ["2231", "7002000", "业务分析专员/助理", "business analyst"],
                                            ["464", "7002000", "其他", "Others"]],
                                           [["391", "4000000", "客户服务总监", "Customer Service Director"],
                                            ["390", "4000000", "客户服务经理", "Customer Service Manager"],
                                            ["549", "4000000", "客户服务主管", "Customer Service Supervisor"],
                                            ["257", "4000000", "客户服务专员/助理", "Customer Service Specialist/Assistant"],
                                            ["261", "4000000", "客户关系/投诉协调人员", "Customer Relation/Complaint Coordinator"],
                                            ["260", "4000000", "客户咨询热线/呼叫中心人员", "Hotline/Call Center"],
                                            ["846", "4000000", "网络/在线客服", "Online Customer Service"],
                                            ["258", "4000000", "售前/售后技术支持管理", "Pre/Post-sale Management"],
                                            ["392", "4000000", "售前/售后技术支持工程师", "Pre/Post-sale Engineer"],
                                            ["2147", "4000000", "VIP专员", "VIP  Commissioner"],
                                            ["2148", "4000000", "呼叫中心客服", "Call Centre"], ["262", "4000000", "其他", "Others"]],
                                           [["158", "4082000", "市场总监", "Marketing Director"],
                                            ["600", "4082000", "市场经理", "Marketing Manager"],
                                            ["604", "4082000", "市场主管", "Marketing Supervisor"],
                                            ["171", "4082000", "市场专员/助理", "Marketing Specialist/Assistant"],
                                            ["159", "4082000", "市场营销经理", "Marketing & Sales Manager"],
                                            ["601", "4082000", "市场营销主管", "Marketing & Sales Supervisor"],
                                            ["160", "4082000", "市场营销专员/助理", "Marketing & Sales Specialist/Assistant"],
                                            ["311", "4082000", "业务拓展经理/主管", "BD Manager/Supervisor"],
                                            ["602", "4082000", "业务拓展专员/助理", "BD Specialist/Assistant"],
                                            ["847", "4082000", "产品经理", "Product Manager"],
                                            ["848", "4082000", "产品主管", "Product Supervisor"],
                                            ["849", "4082000", "产品专员/助理", "Product Specialist/Assistant"],
                                            ["168", "4082000", "品牌经理", "Brand Manager"],
                                            ["603", "4082000", "品牌主管", "Brand Supervisor"],
                                            ["170", "4082000", "品牌专员/助理", "Brand Specialist/Assistant"],
                                            ["161", "4082000", "市场策划/企划经理/主管", "Marketing Planning Manager/Supervisor"],
                                            ["605", "4082000", "市场策划/企划专员/助理", "Marketing Planning Specialist/Assistant"],
                                            ["851", "4082000", "市场文案策划", "Marketing Copywriter"],
                                            ["749", "4082000", "活动策划", "Event Planner"],
                                            ["759", "4082000", "活动执行", "Event Execution"],
                                            ["748", "4082000", "促销主管/督导", "Promotion Supervisor"],
                                            ["850", "4082000", "促销员", "Promoter"], ["451", "4082000", "网站推广", "Web Promotion"],
                                            ["866", "4082000", "SEO/SEM", "SEO/SEM"],
                                            ["853", "4082000", "学术推广", "Academic Promotion"],
                                            ["747", "4082000", "选址拓展/新店开发", "Site Location/Development"],
                                            ["167", "4082000", "市场调研与分析", "Market Research/Analyst"],
                                            ["2174", "4082000", "品牌策划", "brand planning"],
                                            ["2175", "4082000", "市场通路专员", "Trade Marketing Specialist"],
                                            ["2176", "4082000", "促销经理", "promotions manager"],
                                            ["174", "4082000", "其他", "Others"]], [["162", "4084000", "公关总监", "PR Director"],
                                                                                  ["606", "4084000", "公关经理/主管",
                                                                                   "PR Manager/Supervisor"],
                                                                                  ["163", "4084000", "公关专员/助理",
                                                                                   "PR Specialist/Assistant"],
                                                                                  ["164", "4084000", "媒介经理/主管",
                                                                                   "Media Manager/Supervisor"],
                                                                                  ["165", "4084000", "媒介专员/助理",
                                                                                   "Media Specialist/Assistant"],
                                                                                  ["513", "4084000", "媒介策划/管理",
                                                                                   "Media Planning/Administration"],
                                                                                  ["768", "4084000", "政府事务管理",
                                                                                   "Government Affairs"],
                                                                                  ["2181", "4084000", "媒介销售",
                                                                                   "General Service Administration"],
                                                                                  ["2182", "4084000", "活动执行",
                                                                                   "Event Executive"],
                                                                                  ["607", "4084000", "其他", "Others"]],
                                           [["756", "7004000", "广告创意/设计总监", "Advertising Creative Director"],
                                            ["757", "7004000", "广告创意/设计经理/主管", "Advertising Creative Manager/Supervisor"],
                                            ["510", "7004000", "广告创意/设计师", "Advertising Designer"],
                                            ["509", "7004000", "广告文案策划", "Advertising Copywriter"],
                                            ["512", "7004000", "广告美术指导", "Advertising Art Director"],
                                            ["514", "7004000", "广告制作执行", "Advertising Production"],
                                            ["855", "7004000", "广告客户总监", "Advertising Account Director"],
                                            ["506", "7004000", "广告客户经理", "Advertising Account Manager"],
                                            ["856", "7004000", "广告客户主管", "Advertising Account Supervisor"],
                                            ["507", "7004000", "广告客户代表", "Advertising Account Representative"],
                                            ["508", "7004000", "广告/会展业务拓展", "Advertising/Exhibition BD"],
                                            ["610", "7004000", "会展策划/设计", "Exhibition Designing"],
                                            ["857", "7004000", "会务经理/主管", "Exhibition Manager/Supervisor"],
                                            ["172", "7004000", "会务专员/助理", "Exhibition Specialist/Assistant"],
                                            ["609", "7004000", "广告/会展项目管理", "Advertising/Exhibition Project Management"],
                                            ["2237", "7004000", "企业/业务发展经理", "Business Development Manager"],
                                            ["515", "7004000", "其他", "Others"]], [["399", "2060000", "首席财务官CFO", "CFO"],
                                                                                  ["200", "2060000", "财务总监",
                                                                                   "Finance Director"],
                                                                                  ["201", "2060000", "财务经理", "Finance Manager"],
                                                                                  ["202", "2060000", "财务主管/总帐主管",
                                                                                   "Finance Supervisor"],
                                                                                  ["714", "2060000", "财务顾问",
                                                                                   "Finance Consultant"],
                                                                                  ["205", "2060000", "财务助理",
                                                                                   "Finance Assistant"],
                                                                                  ["203", "2060000", "财务分析经理/主管",
                                                                                   "Finance Analysis Manager/Supervisor"],
                                                                                  ["204", "2060000", "财务分析员",
                                                                                   "Finance Analyst"],
                                                                                  ["206", "2060000", "会计经理/主管",
                                                                                   "Accounting Manager/Supervisor"],
                                                                                  ["207", "2060000", "会计/会计师", "Accountant"],
                                                                                  ["713", "2060000", "会计助理/文员",
                                                                                   "Accounting Assistant"],
                                                                                  ["208", "2060000", "出纳员", "Cashier"],
                                                                                  ["212", "2060000", "审计经理/主管",
                                                                                   "Audit Manager/Supervisor"],
                                                                                  ["213", "2060000", "审计专员/助理",
                                                                                   "Audit Specialist/Assistant"],
                                                                                  ["209", "2060000", "税务经理/主管",
                                                                                   "Tax Manager/Supervisor"],
                                                                                  ["210", "2060000", "税务专员/助理",
                                                                                   "Tax Specialist/Assistant"],
                                                                                  ["211", "2060000", "成本经理/主管",
                                                                                   "Cost Control Manager/Supervisor"],
                                                                                  ["527", "2060000", "成本会计", "Cost Accountant"],
                                                                                  ["570", "2060000", "资产/资金管理",
                                                                                   "Asset Management"],
                                                                                  ["715", "2060000", "资金专员",
                                                                                   "Treasury Specialist"],
                                                                                  ["214", "2060000", "统计员", "Statistician"],
                                                                                  ["2098", "2060000", "固定资产会计",
                                                                                   "Fixed Asset Accountant"],
                                                                                  ["2099", "2060000", "成本管理员",
                                                                                   "Cost Accounting Specialist"],
                                                                                  ["215", "2060000", "其他", "Others"]],
                                           [["120", "5002000", "人力资源总监", "HR Director"],
                                            ["121", "5002000", "人力资源经理", "HR Manager"],
                                            ["618", "5002000", "人力资源主管", "HR Supervisor"],
                                            ["122", "5002000", "人力资源专员/助理", "HR Specialist/Assistant"],
                                            ["125", "5002000", "培训经理/主管", "Training Manager/Supervisor"],
                                            ["126", "5002000", "培训专员/助理", "Training Specialist/Assistant"],
                                            ["123", "5002000", "招聘经理/主管", "Recruiting Manager/Supervisor"],
                                            ["124", "5002000", "招聘专员/助理", "Recruiting Specialist/Assistant"],
                                            ["127", "5002000", "薪酬福利经理/主管", "C&B Manager/Supervisor"],
                                            ["780", "5002000", "薪酬福利专员/助理", "C&B Specialist/Assistant"],
                                            ["619", "5002000", "绩效考核经理/主管", "Performance Assessment Manager/Supervisor"],
                                            ["778", "5002000", "绩效考核专员/助理", "Performance Assessment Specialist/Assistant"],
                                            ["620", "5002000", "员工关系/企业文化/工会",
                                             "Employee Relationship/Corporate Culture/Labor Union"],
                                            ["858", "5002000", "企业培训师/讲师", "Staff Trainer"],
                                            ["779", "5002000", "人事信息系统(HRIS)管理", "HRIS Management"],
                                            ["128", "5002000", "猎头顾问/助理", "Headhunter/Assistant"],
                                            ["130", "5002000", "其他", "Others"]],
                                           [["328", "3010000", "行政总监", "Administration Director"],
                                            ["114", "3010000", "行政经理/主管/办公室主任", "Administration Manager/Supervisor"],
                                            ["115", "3010000", "行政专员/助理", "Administration Specialist/Assistant"],
                                            ["116", "3010000", "助理/秘书/文员", "Assistant/Secretary/Clerk"],
                                            ["117", "3010000", "前台/总机/接待", "Receptionist"],
                                            ["859", "3010000", "文档/资料管理", "Document Keeper"],
                                            ["498", "3010000", "电脑操作/打字/录入员", "Typist"],
                                            ["119", "3010000", "后勤人员", "Logistics"],
                                            ["2144", "3010000", "党工团干事", "The party working group director"],
                                            ["2145", "3010000", "图书管理员", "librarian"],
                                            ["2146", "3010000", "内勤人员", "indoor staff"], ["329", "3010000", "其他", "Others"]],
                                           [["813", "201300", "项目总监", "Project Director"],
                                            ["814", "201300", "项目经理/项目主管", "Project Manager/Supervisor"],
                                            ["815", "201300", "项目专员/助理", "Project Specialist/Assistant"],
                                            ["816", "201300", "广告/会展项目管理", "Advertising/Exhibition Project Management"],
                                            ["817", "201300", "IT项目总监", "IT Project Director"],
                                            ["818", "201300", "IT项目经理/主管", "IT Project Manager/Supervisor"],
                                            ["819", "201300", "IT项目执行/协调人员", "IT Project Coordinator"],
                                            ["820", "201300", "通信项目管理", "Communication Project Management"],
                                            ["829", "201300", "房地产项目配套工程师", "Real Estate Supporting Engineer"],
                                            ["830", "201300", "房地产项目管理", "Real Estate Project Management"],
                                            ["834", "201300", "证券/投资项目管理", "Security/Investment Project Management"],
                                            ["831", "201300", "保险项目经理/主管", "Insurance Project Management"],
                                            ["821", "201300", "生产项目经理/主管", "Production Project Manager/Supervisor"],
                                            ["822", "201300", "生产项目工程师", "Production Project Engineer"],
                                            ["823", "201300", "汽车工程项目管理", "Automobile Engineering Project Management"],
                                            ["824", "201300", "电子/电器项目管理", "Electronic/Electrical Project Management"],
                                            ["825", "201300", "服装/纺织/皮革项目管理", "Apparels/Textiles/Leather Project Management"],
                                            ["826", "201300", "医药项目管理", "Pharmaceutical Project Management"],
                                            ["827", "201300", "化工项目管理", "Chemical Project Management"],
                                            ["828", "201300", "物流/仓储项目管理", "Logistics/Warehousing Project Management"],
                                            ["832", "201300", "咨询项目管理", "Consulting Project Management"],
                                            ["833", "201300", "能源/矿产项目管理", "Energy/Mining Project Management"],
                                            ["2079", "201300", "项目计划合约专员", "Project plan contract commissioner"],
                                            ["2080", "201300", "项目招投标", "project bidding"], ["835", "201300", "其他", "Others"]],
                                           [["249", "2023405", "质量管理/测试经理", "QA/QC Manager"],
                                            ["250", "2023405", "质量管理/测试主管", "QA/QC Supervisor"],
                                            ["251", "2023405", "质量管理/测试工程师", "QA/QC Engineer"],
                                            ["252", "2023405", "质量检验员/测试员", "QA Inspector"],
                                            ["067", "2023405", "化验/检验", "Laboratory Technician"],
                                            ["253", "2023405", "认证/体系工程师/审核员", "Quality System Inspector"],
                                            ["807", "2023405", "环境/健康/安全经理/主管", "EHS Manager/Supervisor"],
                                            ["529", "2023405", "环境/健康/安全工程师", "EHS Engineer"],
                                            ["330", "2023405", "供应商/采购质量管理", "Supplier/Purchasing Quality Management"],
                                            ["331", "2023405", "安全管理", "Security Management"],
                                            ["384", "2023405", "安全消防", "Safety/Fire Control"],
                                            ["2081", "2023405", "可靠度工程师", "CRE"],
                                            ["2082", "2023405", "故障分析工程师", "Failure Analysis Engineer"],
                                            ["2083", "2023405", "采购材料/设备管理", "Development and Procurement of Materials"],
                                            ["254", "2023405", "其他", "Others"]],
                                           [["136", "1050000", "首席执行官CEO/总裁/总经理", "CEO"], ["138", "1050000", "首席运营官COO", "COO"],
                                            ["139", "1050000", "首席财务官CFO", "CFO"], ["137", "1050000", "CTO/CIO", "CTO/CIO"],
                                            ["140", "1050000", "副总裁/副总经理", "Vice-President"],
                                            ["141", "1050000", "分公司/代表处负责人", "Head of Branch Company"],
                                            ["144", "1050000", "部门/事业部管理", "Department Management"],
                                            ["142", "1050000", "总裁助理/总经理助理", "Assistant to General Manager"],
                                            ["870", "1050000", "总编/副总编", "Chief Editor"],
                                            ["907", "1050000", "行长/副行长", "Bank President"],
                                            ["911", "1050000", "工厂厂长/副厂长", "Factory Manager"],
                                            ["912", "1050000", "校长/副校长", "Principal"], ["143", "1050000", "合伙人", "Partner"],
                                            ["2001", "1050000", "办事处首席代表", "chief representative of the office"],
                                            ["2002", "1050000", "投资者关系", "Investor Relations"],
                                            ["2003", "1050000", "企业秘书/董事会秘书", "Organizational Secretary"],
                                            ["2004", "1050000", "策略发展总监", "Director of strategic development,"],
                                            ["2005", "1050000", "运营总监", "Director of Operations"],
                                            ["148", "1050000", "其他", "Others"]],
                                           [["044", "160000", "高级软件工程师", "Senior Software Engineer"],
                                            ["045", "160000", "软件工程师", "Software Engineer"],
                                            ["079", "160000", "软件研发工程师", "Software Developer"],
                                            ["665", "160000", "需求工程师", "Requirements Engineer"],
                                            ["667", "160000", "系统架构设计师", "System Architect"],
                                            ["668", "160000", "系统分析员", "Systems Analyst"],
                                            ["047", "160000", "数据库开发工程师", "Database Developer"],
                                            ["048", "160000", "ERP技术/开发应用", "ERP Development"],
                                            ["053", "160000", "互联网软件工程师", "Internet Software Engineer"],
                                            ["679", "160000", "手机软件开发工程师", "Mobile Software Developer"],
                                            ["687", "160000", "嵌入式软件开发", "Embedded Software Developer"],
                                            ["863", "160000", "移动互联网开发", "Mobile Internet Development"],
                                            ["864", "160000", "WEB前端开发", "Front-end Development"],
                                            ["317", "160000", "语音/视频/图形开发", "Audio/Video/Graphics Development"],
                                            ["669", "160000", "用户界面（UI）设计", "UI Design"],
                                            ["861", "160000", "用户体验（UE/UX）设计", "UE/UX Design"],
                                            ["054", "160000", "网页设计/制作/美工", "Web Page Design/Production"],
                                            ["057", "160000", "游戏设计/开发", "Game Design/Development"],
                                            ["671", "160000", "游戏策划", "Game Planner"],
                                            ["672", "160000", "游戏界面设计", "Game UI Design"],
                                            ["666", "160000", "系统集成工程师", "System Integration Engineer"],
                                            ["2034", "160000", "算法工程师", "Algorithm Engineer"],
                                            ["2035", "160000", "仿真应用工程师", "Simulation Application Engineer"],
                                            ["2036", "160000", "计算机辅助设计师", "Computer aided designer"],
                                            ["2037", "160000", "网站架构设计师", "Web Architecture Design"],
                                            ["2038", "160000", "IOS开发工程师", "IOS development engineer"],
                                            ["2039", "160000", "Android开发工程师", "Android  development engineer"],
                                            ["2040", "160000", "Java开发工程师", "Java  development engineer"],
                                            ["2041", "160000", "PHP开发工程师", "PHP Development Engineer"],
                                            ["2042", "160000", "C语言开发工程师", "Senior C Engineer"],
                                            ["2043", "160000", "脚本开发工程师", "Script development engineers"],
                                            ["060", "160000", "其他", "Others"]],
                                           [["314", "160300", "高级硬件工程师", "Senior Hardware Engineer"],
                                            ["043", "160300", "硬件工程师", "Hardware Engineer"],
                                            ["407", "160300", "嵌入式硬件开发", "Embedded Hardware Developer"],
                                            ["557", "160300", "其他", "Others"]],
                                           [["316", "160200", "互联网产品经理/主管", "Internet Product Manager/Supervisor"],
                                            ["675", "160200", "互联网产品专员/助理", "Internet product Specialist/Assistant"],
                                            ["676", "160200", "电子商务经理/主管", "E-Commerce Manager/Supervisor"],
                                            ["677", "160200", "电子商务专员/助理", "E-Commerce Specialist/Assistant"],
                                            ["052", "160200", "网络运营管理", "Web Operations Management"],
                                            ["670", "160200", "网络运营专员/助理", "Web Operations Specialist/Assistant"],
                                            ["056", "160200", "网站编辑", "Web Editor"], ["552", "160200", "SEO/SEM", "SEO/SEM"],
                                            ["2046", "160200", "产品总监", "Product Director"],
                                            ["2047", "160200", "运营总监", "Director of Operations"],
                                            ["2048", "160200", "网站运营总监/经理", "Director of Ecommerce"],
                                            ["2049", "160200", "电子商务总监", "Chief E-commerce Officer"],
                                            ["2050", "160200", "新媒体运营", "New media operation"],
                                            ["2051", "160200", "网店店长", "Store manager"],
                                            ["2052", "160200", "网店推广", "Online promotion"],
                                            ["2053", "160200", "网店客服", "Online Customer Service"],
                                            ["2054", "160200", "网店运营", "Online and product operation"],
                                            ["2055", "160200", "网店管理员", "Site administrators"],
                                            ["2056", "160200", "运营主管/专员", "Operations Supervisor"],
                                            ["2057", "160200", "微信推广", "WeChat promotion"],
                                            ["2058", "160200", "淘宝/微信运营专员/主管", "WeChat operations specialist"],
                                            ["2059", "160200", "产品运营", "Product Operation"],
                                            ["2060", "160200", "数据运营", "mobile data operation"],
                                            ["2061", "160200", "市场运营", "market operation"],
                                            ["2062", "160200", "内容运营", "Content Specialist"],
                                            ["556", "160200", "其他", "Others"]],
                                           [["693", "160400", "IT质量管理经理/主管", "IT QA/QC Manager/Supervisor"],
                                            ["049", "160400", "IT质量管理工程师", "IT QA/QC Engineer"],
                                            ["694", "160400", "系统测试", "System Testing"],
                                            ["695", "160400", "软件测试", "Software Testing"],
                                            ["696", "160400", "硬件测试", "Hardware Testing"],
                                            ["868", "160400", "配置管理工程师", "Configuration Management Engineer"],
                                            ["692", "160400", "信息技术标准化工程师", "IT Standardization Engineer"],
                                            ["2063", "160400", "标准化工程师", "standardization engineer"],
                                            ["2064", "160400", "游戏测试", "game testing"],
                                            ["2065", "160400", "手机维修", "Cellphone Repairs"], ["561", "160400", "其他", "Others"]],
                                           [["040", "200500", "信息技术经理/主管", "IT Manager/Supervisor"],
                                            ["041", "200500", "信息技术专员", "IT Specialist"],
                                            ["058", "200500", "IT技术支持/维护经理", "IT Technical Support Manager"],
                                            ["315", "200500", "IT技术支持/维护工程师", "IT Technical Support Engineer"],
                                            ["046", "200500", "系统工程师", "System Engineer"],
                                            ["051", "200500", "系统管理员", "System Administrator"],
                                            ["055", "200500", "网络工程师", "Network Engineer"],
                                            ["388", "200500", "网络管理员", "Web Administrator"],
                                            ["059", "200500", "网络与信息安全工程师", "Information Security Engineer"],
                                            ["389", "200500", "数据库管理员", "Database Administrator"],
                                            ["678", "200500", "计算机硬件维护工程师", "Hardware Maintenance Engineer"],
                                            ["551", "200500", "ERP实施顾问", "ERP Implementation"],
                                            ["690", "200500", "IT技术文员/助理", "IT Technical Clerk/Assistant"],
                                            ["699", "200500", "IT文档工程师", "IT Technical Writer"],
                                            ["698", "200500", "Helpdesk", "Helpdesk"], ["840", "200500", "其他", "Others"]],
                                           [["398", "200300", "CTO/CIO", "CTO/CIO"],
                                            ["928", "200300", "IT技术/研发总监", "IT Technology Director"],
                                            ["313", "200300", "IT技术/研发经理/主管", "IT Technology Manager/Supervisor"],
                                            ["688", "200300", "IT项目总监", "IT Project Director"],
                                            ["042", "200300", "IT项目经理/主管", "IT Project Manager/Supervisor"],
                                            ["689", "200300", "IT项目执行/协调人员", "IT Project Coordinator"],
                                            ["841", "200300", "其他", "Others"]],
                                           [["680", "5001000", "通信技术工程师", "Communication Engineer"],
                                            ["500", "5001000", "通信研发工程师", "Communication Developer"],
                                            ["323", "5001000", "数据通信工程师", "Data Communication Engineer"],
                                            ["324", "5001000", "移动通信工程师", "Mobile Communication Engineer"],
                                            ["325", "5001000", "电信网络工程师", "Telecom Network Engineer"],
                                            ["322", "5001000", "电信交换工程师", "Telecom Exchange Engineer"],
                                            ["320", "5001000", "有线传输工程师", "Wired Transmission Engineer"],
                                            ["321", "5001000", "无线/射频通信工程师", "RF Communication Engineer"],
                                            ["326", "5001000", "通信电源工程师", "Communication Power Supply Engineer"],
                                            ["558", "5001000", "通信标准化工程师", "Communication Standardization Engineer"],
                                            ["499", "5001000", "通信项目管理", "Communication Project Management"],
                                            ["2183", "5001000", "增值产品开发工程师", "Value-Added Product Development Engineer"],
                                            ["327", "5001000", "其他", "Others"]],
                                           [["710", "141000", "房地产项目策划经理/主管", "Real Estate Planning Manager/Supervisor"],
                                            ["351", "141000", "房地产项目策划专员/助理", "Real Estate Planning Specialist/Assistant"],
                                            ["883", "141000", "房地产项目招投标", "Real Estate Bidding Management"],
                                            ["701", "141000", "房地产项目开发报建", "Applying for Construction"],
                                            ["711", "141000", "房地产项目配套工程师", "Real Estate Supporting Engineer"],
                                            ["709", "141000", "房地产销售经理", "Real Estate Sales Manager"],
                                            ["882", "141000", "房地产销售主管", "Real Estate Sales Supervisor"],
                                            ["708", "141000", "房地产销售/置业顾问", "Real Estate Sales Representative"],
                                            ["567", "141000", "房地产评估", "Real Estate Evaluation"],
                                            ["105", "141000", "房地产中介/交易", "Real Estate Agent/Broker"],
                                            ["566", "141000", "房地产项目管理", "Real Estate Project Management"],
                                            ["2028", "141000", "房地产资产管理", "Real Estate Assets Management"],
                                            ["2029", "141000", "监察人员", "supervisory personnel"],
                                            ["2030", "141000", "地产店长/经理", "Real estate manager"],
                                            ["2031", "141000", "房地产内勤", "The real estate office work"],
                                            ["2032", "141000", "房地产客服", "The real estate customer service"],
                                            ["568", "141000", "其他", "Others"]],
                                           [["350", "140000", "高级建筑工程师/总工", "Senior Architect"],
                                            ["096", "140000", "建筑工程师", "Architect"],
                                            ["884", "140000", "建筑设计师", "Architectural Designer"],
                                            ["097", "140000", "土木/土建/结构工程师", "Civil/Structural Engineer"],
                                            ["707", "140000", "岩土工程", "Geotechnical Engineer"],
                                            ["703", "140000", "建筑制图", "Architectural Drafting"],
                                            ["383", "140000", "建筑工程测绘/测量", "Building Engineering Survey"],
                                            ["466", "140000", "道路/桥梁/隧道工程技术", "Road/Bridge/Tunnel Technology"],
                                            ["885", "140000", "水利/港口工程技术", "Water Conservancy/Port Engineering Technology"],
                                            ["886", "140000", "架线和管道工程技术", "Pipeline Engineering Technology"],
                                            ["099", "140000", "给排水/暖通/空调工程", "Drainage/HVAC/Air Conditioning Engineering"],
                                            ["289", "140000", "智能大厦/布线/弱电/安防",
                                             "Intelligent Building/Structure Cabling/Weak Current/Safety"],
                                            ["100", "140000", "室内装潢设计", "Interior Design"],
                                            ["564", "140000", "幕墙工程师", "Facade Engineer"],
                                            ["563", "140000", "园林/景观设计", "Landscape Design"],
                                            ["103", "140000", "城市规划与设计", "Urban Planning & Design"],
                                            ["562", "140000", "市政工程师", "Municipal Engineer"],
                                            ["106", "140000", "工程监理/质量管理", "Construction Quality Management"],
                                            ["102", "140000", "工程造价/预结算", "Construction Budget/Cost Management"],
                                            ["704", "140000", "工程资料管理", "Engineering Data Management"],
                                            ["705", "140000", "建筑施工现场管理", "Construction Site Management"],
                                            ["706", "140000", "施工队长", "Construction Team Leader"],
                                            ["107", "140000", "施工员", "Construction Worker"],
                                            ["565", "140000", "建筑工程安全管理", "Construction Security Management"],
                                            ["2023", "140000", "软装设计师", "Decoration Designer"],
                                            ["2024", "140000", "工程总监", "Chief Engineer"],
                                            ["2025", "140000", "土建勘察", "Civil engineering surveying"],
                                            ["2026", "140000", "硬装设计师", "Hard outfit stylist"],
                                            ["2027", "140000", "橱柜设计师", "Ambry stylist"], ["108", "140000", "其他", "Others"]],
                                           [["393", "142000", "物业经理/主管", "Property Management Manager/Supervisor"],
                                            ["095", "142000", "物业管理专员/助理", "Property Management Specialist/Assistant"],
                                            ["101", "142000", "物业租赁/销售", "Property Rent/Sales"],
                                            ["352", "142000", "物业维修", "Property Maintenance"],
                                            ["712", "142000", "物业顾问", "Property Consultant"],
                                            ["465", "142000", "物业招商管理", "Property Lease"],
                                            ["2033", "142000", "监控维护", "system monitoring and maintenance"],
                                            ["569", "142000", "其他", "Others"]], [["716", "2071000", "行长/副行长", "Bank President"],
                                                                                 ["347", "2071000", "银行经理/主任", "Bank Manager"],
                                                                                 ["721", "2071000", "银行大堂经理",
                                                                                  "Bank Lobby Manager"],
                                                                                 ["887", "2071000", "银行客户总监",
                                                                                  "Bank Account Director"],
                                                                                 ["718", "2071000", "银行客户经理",
                                                                                  "Bank Account Manager"],
                                                                                 ["888", "2071000", "银行客户主管",
                                                                                  "Bank Account Supervisor"],
                                                                                 ["889", "2071000", "银行客户代表",
                                                                                  "Bank Account Representative"],
                                                                                 ["192", "2071000", "银行客户服务",
                                                                                  "Bank Customer Service"],
                                                                                 ["719", "2071000", "综合业务经理/主管",
                                                                                  "Integrated Service Manager/Supervisor"],
                                                                                 ["720", "2071000", "综合业务专员/助理",
                                                                                  "Integrated Service Specialist/Assistant"],
                                                                                 ["193", "2071000", "银行会计/柜员",
                                                                                  "Bank Accountant"], ["572", "2071000", "公司业务",
                                                                                                       "Enterprise Business Service"],
                                                                                 ["573", "2071000", "个人业务",
                                                                                  "Individual Business Service"],
                                                                                 ["571", "2071000", "银行卡/电子银行业务推广",
                                                                                  "Credit Card/Bank Card/E-banking  Promotion"],
                                                                                 ["194", "2071000", "信贷管理/资信评估/分析",
                                                                                  "Credit Management/Valuation/Analysis"],
                                                                                 ["725", "2071000", "信审核查", "Credit Review"],
                                                                                 ["717", "2071000", "外汇交易", "Foreign Exchange"],
                                                                                 ["722", "2071000", "进出口/信用证结算",
                                                                                  "Settlement of Imports & Exports"],
                                                                                 ["723", "2071000", "清算人员", "Bank Clearing"],
                                                                                 ["724", "2071000", "风险控制", "Risk Management"],
                                                                                 ["2108", "2071000", "个人业务部门经理/主管",
                                                                                  "Personal business department manager"],
                                                                                 ["2109", "2071000", "公司业务部门经理/主管",
                                                                                  "The company's business department manager"],
                                                                                 ["2110", "2071000", "高级客户经理/客户经理",
                                                                                  "senior account manager"],
                                                                                 ["2111", "2071000", "信用卡销售",
                                                                                  "credit card sales"],
                                                                                 ["2112", "2071000", "银行柜员", "bank teller"],
                                                                                 ["574", "2071000", "其他", "Others"]],
                                           [["349", "2070000", "证券总监/部门经理", "Security Director/Department Manager"],
                                            ["187", "2070000", "证券/期货/外汇经纪人", "Security/Futures/Foreign Exchange Broker"],
                                            ["910", "2070000", "证券/投资客户总监", "Security/Investment Account Director"],
                                            ["191", "2070000", "证券/投资客户经理", "Security/Investment Account Manager"],
                                            ["908", "2070000", "证券/投资客户主管", "Security/Investment Account Supervisor"],
                                            ["909", "2070000", "证券/投资客户代表", "Security/Investment Account Representative"],
                                            ["575", "2070000", "证券分析/金融研究", "Security Analysis/Financial Research"],
                                            ["188", "2070000", "投资/理财服务", "Investment Service"],
                                            ["576", "2070000", "投资银行业务", "Investment Banking Business"],
                                            ["346", "2070000", "融资总监", "Treasury Director"],
                                            ["809", "2070000", "融资经理/主管", "Treasury Manager/Supervisor"],
                                            ["810", "2070000", "融资专员/助理", "Treasury Specialist/Assistant"],
                                            ["577", "2070000", "股票/期货操盘手", "Stock/Futures Operator"],
                                            ["579", "2070000", "资产评估", "Assets Assessment"],
                                            ["190", "2070000", "风险管理/控制/稽查", "Risk Management/Control"],
                                            ["198", "2070000", "储备经理人", "Agency Management Associate"],
                                            ["468", "2070000", "证券/投资项目管理", "Security/Investment Project Management"],
                                            ["2100", "2070000", "金融/经济研究员", "Financial Analyst/Economist"],
                                            ["2101", "2070000", "金融产品经理", "Product Manager"],
                                            ["2102", "2070000", "金融产品销售", "Investment Product Sales"],
                                            ["2103", "2070000", "基金项目经理", "Fund project manager"],
                                            ["2104", "2070000", "金融服务经理", "F&I Manager"],
                                            ["2105", "2070000", "投资经理", "Investment Manager"],
                                            ["2106", "2070000", "投资银行财务分析", "Investment bank financial analysis"],
                                            ["2107", "2070000", "金融租赁", "financial lease"], ["199", "2070000", "其他", "Others"]],
                                           [["535", "7006000", "保险业务管理", "Insurance Business Management"],
                                            ["196", "7006000", "保险代理/经纪人/客户经理", "Insurance agent"],
                                            ["537", "7006000", "保险顾问/财务规划师", "Insurance Consultant"],
                                            ["540", "7006000", "保险产品开发/项目策划", "Insurance Development/Planning"],
                                            ["543", "7006000", "保险培训师", "Insurance Trainer"],
                                            ["545", "7006000", "保险契约管理", "Insurance Contract Administration"],
                                            ["197", "7006000", "核保理赔", "Insurance Underwriting/Claim Processing"],
                                            ["726", "7006000", "汽车定损/车险理赔", "Automobile Insurance"],
                                            ["348", "7006000", "保险精算师", "Actuary"],
                                            ["541", "7006000", "客户服务/续期管理", "Insurance Customer Service/Contract Extension"],
                                            ["539", "7006000", "保险内勤", "Insurance Office Staff"],
                                            ["536", "7006000", "保险项目经理/主管", "Insurance Project Management"],
                                            ["544", "7006000", "储备经理人", "Agency Management Associate"],
                                            ["2251", "7006000", "理财顾问/财务规划师", "Financial Planner"],
                                            ["2252", "7006000", "保险电销", "telesales"],
                                            ["2253", "7006000", "保险核安", "Insurance nuclear security"],
                                            ["546", "7006000", "其他", "Others"]], [["930", "200900", "信托服务", "Trust Service"],
                                                                                  ["921", "200900", "担保业务",
                                                                                   "Guarantee Business"],
                                                                                  ["929", "200900", "拍卖师", "Auctioneer"],
                                                                                  ["931", "200900", "典当业务", "Pawn Business"],
                                                                                  ["811", "200900", "珠宝/收藏品鉴定",
                                                                                   "Jewellery /Collection Appraiser"],
                                                                                  ["812", "200900", "其他", "Others"]],
                                           [["235", "4083000", "采购总监", "Purchasing Director"],
                                            ["550", "4083000", "采购经理/主管", "Purchasing Manager/Supervisor"],
                                            ["236", "4083000", "采购专员/助理", "Purchasing Specialist/Assistant"],
                                            ["663", "4083000", "供应商开发", "Supplier Development"],
                                            ["488", "4083000", "供应链管理", "Supply Chain Administration"],
                                            ["664", "4083000", "买手", "Buyer"],
                                            ["312", "4083000", "外贸/贸易经理/主管", "Foreign Trade Manager/Supervisor"],
                                            ["237", "4083000", "外贸/贸易专员/助理", "Foreign Trade Specialist/Assistant"],
                                            ["238", "4083000", "贸易跟单", "Trade Merchandiser"],
                                            ["239", "4083000", "报关员", "Customs Declarer"],
                                            ["2177", "4083000", "业务跟单经理", "Merchandiser Manager"],
                                            ["2178", "4083000", "高级业务跟单", "Senior Merchandiser"],
                                            ["2179", "4083000", "助理业务跟单", "Assistant Merchandiser"],
                                            ["2180", "4083000", "国际贸易主管/专员", "International Trading Supervisor"],
                                            ["240", "4083000", "其他", "Others"]],
                                           [["246", "4010300", "机动车司机/驾驶", "Automobile Driver"],
                                            ["879", "4010300", "列车驾驶/操作", "Train Driver"],
                                            ["880", "4010300", "船舶驾驶/操作", "Watercraft Operation"],
                                            ["245", "4010300", "飞机驾驶/操作", "Airplane Operation"],
                                            ["594", "4010300", "公交/地铁乘务", "Bus Conductor/Subway Attendant"],
                                            ["489", "4010300", "列车乘务", "Train Crew"],
                                            ["881", "4010300", "船舶乘务", "Shipping Service"],
                                            ["878", "4010300", "船员/水手", "Sailor/Shipmate"],
                                            ["737", "4010300", "航空乘务", "Airline Crew"],
                                            ["736", "4010300", "地勤人员", "Ground Attendant"],
                                            ["2154", "4010300", "安检员", "Screeners"],
                                            ["2155", "4010300", "驾驶教练", "Driving Instructor"],
                                            ["2156", "4010300", "交通管理员", "traffic warden"],
                                            ["2157", "4010300", "船长", "Captain"],
                                            ["2158", "4010300", "代驾", "designated driver"], ["248", "4010300", "其他", "Others"]],
                                           [["241", "4010400", "物流总监", "Logistics Director"],
                                            ["597", "4010400", "物流经理/主管", "Logistics Manager/Supervisor"],
                                            ["242", "4010400", "物流专员/助理", "Logistics Specialist/Assistant"],
                                            ["740", "4010400", "货运代理", "Cargo Agent"],
                                            ["353", "4010400", "运输经理/主管", "Transportation Manager/Supervisor"],
                                            ["247", "4010400", "快递员/速递员", "Express Deliver/Courier"],
                                            ["746", "4010400", "水运/空运/陆运操作", "Transport Operation"],
                                            ["741", "4010400", "集装箱业务", "Container Operator"],
                                            ["742", "4010400", "报关员", "Customs Declarer"],
                                            ["490", "4010400", "单证员", "Documentation Specialist"],
                                            ["243", "4010400", "仓库经理/主管", "Warehouse Manager/Supervisor"],
                                            ["244", "4010400", "仓库/物料管理员", "Warehouse/Material Administrator"],
                                            ["745", "4010400", "理货/分拣/打包", "Tallying/Sorting/Packing"],
                                            ["394", "4010400", "物流/仓储调度", "Logistics/Warehousing Dispatcher"],
                                            ["744", "4010400", "物流/仓储项目管理", "Logistics/Warehousing Project Management"],
                                            ["491", "4010400", "搬运工", "Mover"],
                                            ["2159", "4010400", "集装箱维护", "Container Type Maintenance"],
                                            ["2160", "4010400", "集装箱操作", "container handling charges"],
                                            ["2161", "4010400", "物流销售", "Logistics   sales"],
                                            ["2162", "4010400", "供应链总监", "Supply Chain Director"],
                                            ["2163", "4010400", "供应链经理/主管", "Supply Chain Manager"],
                                            ["2164", "4010400", "物料经理", "rials manager"],
                                            ["2165", "4010400", "物料主管/专员", "materials supervisor"],
                                            ["2166", "4010400", "项目经理/主管", "Project Manager"],
                                            ["2167", "4010400", "海关事务管理", "Customs Affairs Management"],
                                            ["2168", "4010400", "船务/空运陆运操作", "Shipping Specialist"],
                                            ["2169", "4010400", "订单处理员", "Order Processor"],
                                            ["2170", "4010400", "水运/陆运/空运销售", "Air Sales Manager"],
                                            ["2254", "4010400", "外卖快递", "Takeout Express"], ["598", "4010400", "其他", "Others"]],
                                           [["061", "121100", "工厂厂长/副厂长", "Factory Manager"],
                                            ["869", "121100", "生产总监", "Production Director"],
                                            ["065", "121100", "生产经理/车间主任", "Production Manager/Workshop Supervisor"],
                                            ["064", "121100", "生产主管/督导/组长", "Production Supervisor"],
                                            ["932", "121100", "生产运营管理", "Production Operating Management"],
                                            ["063", "121100", "生产项目经理/主管", "Production Project Manager/Supervisor"],
                                            ["062", "121100", "生产项目工程师", "Production Project Engineer"],
                                            ["871", "121100", "产品管理", "Product Management"],
                                            ["487", "121100", "生产计划", "Production Planning"],
                                            ["075", "121100", "制造工程师", "Manufacture Engineer"],
                                            ["072", "121100", "工艺/制程工程师", "PE Engineer"],
                                            ["074", "121100", "工业工程师", "IE Engineer"],
                                            ["068", "121100", "生产设备管理", "Production Equipment Management"],
                                            ["069", "121100", "生产物料管理（PMC）", "Production Material Control(PMC)"],
                                            ["592", "121100", "包装工程师", "Packaging Engineer"],
                                            ["090", "121100", "技术文档工程师", "Technical Documents Engineer"],
                                            ["2011", "121100", "总工程师/副总工程师", "Chief Engineer ; chelloef engineer"],
                                            ["2012", "121100", "生产文员", "Production Clerk"],
                                            ["2013", "121100", "营运主管", "operations supervisor ; operations director"],
                                            ["2014", "121100", "营运经理", "Operations Manager"],
                                            ["2015", "121100", "设备主管", "facility supervisor"],
                                            ["2016", "121100", "化验师", "Chemist"],
                                            ["2017", "121100", "生产跟单", "production technician"],
                                            ["077", "121100", "其他", "Others"]],
                                           [["686", "160100", "电子技术研发工程师", "Electronic technology R & D Engineer"],
                                            ["078", "160100", "电子/电器工程师", "Electronic/Electrical Equipment Engineer"],
                                            ["528", "160100", "电器研发工程师", "Electrical Equipment Developer"],
                                            ["091", "160100", "电子/电器工艺/制程工程师", "Electronic/Electrical Equipment PE Engineer"],
                                            ["089", "160100", "电路工程师/技术员", "Electronic Circuit Engineer"],
                                            ["406", "160100", "模拟电路设计/应用工程师", "Analog Circuit Engineer"],
                                            ["408", "160100", "版图设计工程师", "Layout Design Engineer"],
                                            ["404", "160100", "集成电路IC设计/应用工程师", "IC Design/Application Engineer"],
                                            ["405", "160100", "IC验证工程师", "IC Verification Engineer"],
                                            ["082", "160100", "电子元器件工程师", "Electronic Component Engineer"],
                                            ["684", "160100", "射频工程师", "RF Engineer"],
                                            ["318", "160100", "无线电工程师", "Radio Engineer"],
                                            ["411", "160100", "激光/光电子技术", "Laser/Optoelectronic Technology"],
                                            ["559", "160100", "光源/照明工程师", "Lighting Engineer"],
                                            ["681", "160100", "变压器与磁电工程师", "Transformer and Magnetoelectricity Engineer"],
                                            ["083", "160100", "电池/电源开发", "Battery/Power Development"],
                                            ["085", "160100", "家用电器/数码产品研发",
                                             "Household Electronics/Digital Products Development"],
                                            ["560", "160100", "空调工程/设计", "Air Conditioning Engineering/Design"],
                                            ["402", "160100", "音频/视频工程师/技术员", "Audio/Video Engineer/Technician"],
                                            ["808", "160100", "安防系统工程师", "Security Systems Engineer"],
                                            ["401", "160100", "电子/电器设备工程师", "Electronic/Electrical Equipment Engineer"],
                                            ["403", "160100", "电子/电器维修/保养", "Electronics Repair/Maintenance"],
                                            ["409", "160100", "电子/电器项目管理", "Electronic/Electrical Project Management"],
                                            ["865", "160100", "电气工程师", "Electrical Engineer"],
                                            ["467", "160100", "电气设计", "Electrical Design"],
                                            ["683", "160100", "电气线路设计", "Electrical Circuit Design"],
                                            ["682", "160100", "线路结构设计", "Route Structure Design"],
                                            ["081", "160100", "半导体技术", "Semiconductor Technology"],
                                            ["086", "160100", "仪器/仪表/计量工程师", "Instrument/Measurement Engineer"],
                                            ["033", "160100", "自动化工程师", "Automation Engineer"],
                                            ["084", "160100", "现场应用工程师（FAE）", "Field Application Engineer(FAE)"],
                                            ["410", "160100", "测试/可靠性工程师", "Testing/Reliability Engineer"],
                                            ["2044", "160100", "电子工程师/技术员", "Electronics Engineer"],
                                            ["2045", "160100", "电声/音响工程师/技术员", "Sound Effect"],
                                            ["094", "160100", "其他", "Others"]],
                                           [["872", "7003000", "汽车动力系统工程师", "Automobile Power System Engineers"],
                                            ["474", "7003000", "汽车底盘/总装工程师", "Automobile Chassis/Assembly Engineer"],
                                            ["470", "7003000", "车身设计工程师", "Automobile Body Designer"],
                                            ["476", "7003000", "汽车电子工程师", "Automobile Electronic Engineer"],
                                            ["475", "7003000", "汽车机械工程师", "Automobile Mechanical Engineer"],
                                            ["473", "7003000", "汽车零部件设计师", "Auto Parts Designer"],
                                            ["472", "7003000", "汽车装配工艺工程师", "Automobile Assembly PE Engineer"],
                                            ["478", "7003000", "安全性能工程师", "Safety Performance Engineer"],
                                            ["471", "7003000", "汽车工程项目管理", "Automobile Engineering Project Management"],
                                            ["2232", "7003000", "汽车机构工程师", "Automotive Structural Engineer"],
                                            ["2233", "7003000", "汽车电工", "automobile electrician"],
                                            ["2234", "7003000", "售后服务/客户服务", "after service"],
                                            ["2235", "7003000", "加油站工作员", "Service Station worker"],
                                            ["2236", "7003000", "发动机/总装工程师", "Assembly Technology Specialist"],
                                            ["485", "7003000", "其他", "Others"]],
                                           [["469", "7003100", "汽车销售", "Automobile Sales"],
                                            ["479", "7003100", "汽车零配件销售", "Auto Parts Sales"],
                                            ["581", "7003100", "汽车售后服务/客户服务", "Automobile Customer Service"],
                                            ["728", "7003100", "汽车维修/保养", "Automobile Repair/Maintenance"],
                                            ["727", "7003100", "汽车质量管理/检验检测", "Automobile Quality Management"],
                                            ["480", "7003100", "汽车定损/车险理赔", "Automobile Insurance"],
                                            ["483", "7003100", "汽车装饰美容", "Auto Beauty"],
                                            ["484", "7003100", "二手车评估师", "Second-hand Auto Appraiser"],
                                            ["477", "7003100", "4S店管理", "4S Shop Management"],
                                            ["582", "7003100", "其他", "Others"]],
                                           [["332", "5003000", "工程机械经理", "Mechanical Engineering Manager"],
                                            ["333", "5003000", "工程机械主管", "Mechanical Engineering Supervisor"],
                                            ["729", "5003000", "机械设备经理", "Mechanical Equipment Manager"],
                                            ["583", "5003000", "机械设备工程师", "Mechanical Equipment Engineer"],
                                            ["029", "5003000", "机械工程师", "Mechanical Engineering"],
                                            ["093", "5003000", "机械设计师", "Mechanical Designer"],
                                            ["334", "5003000", "机械制图员", "Mechanical Drawer"],
                                            ["584", "5003000", "机械研发工程师", "Mechanical Developer"],
                                            ["586", "5003000", "机械结构工程师", "Mechanical Structural Engineer"],
                                            ["585", "5003000", "机械工艺/制程工程师", "Mechanical PE Engineer"],
                                            ["587", "5003000", "气动工程师", "Pneumatic Engineer"],
                                            ["591", "5003000", "CNC/数控工程师", "CNC Engineer"],
                                            ["588", "5003000", "模具工程师", "Mould Engineer"],
                                            ["873", "5003000", "夹具工程师", "Fixture Engineer"],
                                            ["874", "5003000", "注塑工程师", "Injection Engineer"],
                                            ["590", "5003000", "铸造/锻造工程师/技师", "Foundry/Forging Engineer/Technician"],
                                            ["732", "5003000", "机电工程师", "Electromechanical Engineer"],
                                            ["593", "5003000", "材料工程师", "Material Engineer"],
                                            ["589", "5003000", "机械维修/保养", "Mechanical Repair/Maintenance"],
                                            ["735", "5003000", "飞机设计与制造", "Aircraft Design & Manufacture"],
                                            ["734", "5003000", "飞机维修/保养", "Aircraft Repair/Maintenance"],
                                            ["595", "5003000", "列车设计与制造", "Train Design & Manufacture"],
                                            ["920", "5003000", "列车维修/保养", "Train Repair/Maintenance"],
                                            ["923", "5003000", "船舶设计与制造", "Watercraft Design & Manufacture"],
                                            ["922", "5003000", "船舶维修/保养", "Watercraft Repair/Maintenance"],
                                            ["2184", "5003000", "技术研发工程师", "research and development engineer"],
                                            ["2185", "5003000", "技术研发经理/主管", "research and development manager"],
                                            ["2186", "5003000", "产品策划工程师", "product planning engineer"],
                                            ["2187", "5003000", "项目管理", "project management"],
                                            ["2188", "5003000", "实验室负责人/工程师", "lab manager"],
                                            ["2189", "5003000", "工业工程师", "industrial engineer"],
                                            ["2190", "5003000", "维修经理/主管", "maintenance manager"],
                                            ["2191", "5003000", "装配工程师/客户经理", "Assembly engineer"],
                                            ["2192", "5003000", "焊接工程师/技师", "Welding Engineer"],
                                            ["2193", "5003000", "冲压工程师/技师", "Stamping engineer"],
                                            ["2194", "5003000", "锅炉工程师/技师", "Boiler Engineer"],
                                            ["2195", "5003000", "光伏系统工程师", "PV systems engineer"],
                                            ["2196", "5003000", "汽车/摩托车工程师", "automobile engineer"],
                                            ["2197", "5003000", "轨道交通工程师/技术员", "Rail Transit engineer"],
                                            ["2198", "5003000", "数控操作", "CNC operating"],
                                            ["2199", "5003000", "数控编程", "CNC progarming"],
                                            ["2200", "5003000", "无损检测工程师", "nondestructive testing engineer"],
                                            ["2201", "5003000", "浮法操作工(玻璃技术)", "Float operators"],
                                            ["2202", "5003000", "地铁轨道设计", "subway rail design"],
                                            ["2203", "5003000", "机修工", "mechanic"],
                                            ["2204", "5003000", "工装工程师", "Fixture Engineer"],
                                            ["335", "5003000", "其他", "Others"]],
                                           [["155", "7005000", "服装/纺织品设计", "Fashion and Textile Design"],
                                            ["522", "7005000", "服装打样/制版", "Apparel Sample Production"],
                                            ["739", "7005000", "服装/纺织/皮革工艺师", "Apparels/Textiles/Leather PE Engineer"],
                                            ["738", "7005000", "电脑放码员", "Grading"], ["524", "7005000", "裁床", "Cutting bed"],
                                            ["523", "7005000", "样衣工", "Sample man"],
                                            ["521", "7005000", "面料辅料开发/采购", "Material Purchasing"],
                                            ["520", "7005000", "服装/纺织/皮革跟单", "Apparels/Textiles/Leather Merchandiser"],
                                            ["516", "7005000", "服装/纺织品/皮革销售", "Apparels/Textiles/Leather Sales"],
                                            ["519", "7005000", "服装/纺织品/皮革质量管理",
                                             "QA/QC of Apparels/Textiles/Leather Production"],
                                            ["517", "7005000", "服装/纺织/皮革项目管理", "Apparels/Textiles/Leather Project Management"],
                                            ["2238", "7005000", "服装/纺织设计总监", "closing design director"],
                                            ["2239", "7005000", "纸样师/车板师", "Sewing Clerk"],
                                            ["2240", "7005000", "剪裁工", "tailoring"], ["2241", "7005000", "缝纫工", "hemmer"],
                                            ["2242", "7005000", "纺织工/针织工", "knitter"],
                                            ["2243", "7005000", "配色工", "colour matching"],
                                            ["2244", "7005000", "印染工", "dyeing worker"],
                                            ["2245", "7005000", "漂染工", "bleaching and dyeing"],
                                            ["2246", "7005000", "挡车工", "textile worker"],
                                            ["2247", "7005000", "浆纱工", "sizing worker"], ["2248", "7005000", "整经工", "warper"],
                                            ["2249", "7005000", "鞋子设计", "shoes design"],
                                            ["2250", "7005000", "细纱工", "spinning worker"], ["525", "7005000", "其他", "Others"]],
                                           [["339", "5004000", "车床/磨床/铣床/冲床工", "Latheman/Grinder/Milling/Punch"],
                                            ["343", "5004000", "模具工", "Mould Worker"],
                                            ["338", "5004000", "钳工/机修工/钣金工", "Fitter/Mechanic/Panel Beater"],
                                            ["337", "5004000", "电焊工/铆焊工", "Electric Welder/Rivet Welder"],
                                            ["599", "5004000", "电工", "Electrician"],
                                            ["342", "5004000", "水工/木工/油漆工", "Plumber/Woodworker/Painter"],
                                            ["341", "5004000", "铲车/叉车工", "Forklift Worker"],
                                            ["340", "5004000", "空调工/电梯工/锅炉工", "Air-Condition/Elevator/Boiler Worker"],
                                            ["336", "5004000", "汽车维修/保养", "Automobile Repair/Maintenance"],
                                            ["344", "5004000", "普工/操作工", "General Worker"],
                                            ["2205", "5004000", "技工", "Mechanic"], ["2206", "5004000", "组装工", "assembling"],
                                            ["2207", "5004000", "包装工", "packing"],
                                            ["2208", "5004000", "电力线路工", "Power lineman"],
                                            ["2209", "5004000", "拖压工", "Tow pressure work"],
                                            ["2210", "5004000", "仪表工", "E&I Technician"],
                                            ["2211", "5004000", "电镀工", "electroplating"],
                                            ["2212", "5004000", "喷塑工", "spraying plastics"],
                                            ["2213", "5004000", "电梯工", "ELEVATOR"],
                                            ["2214", "5004000", "吊车司机/卡车司机", "Crane driver"],
                                            ["2215", "5004000", "洗车工", "Car washing"],
                                            ["2216", "5004000", "洗碗工", "washing dishes"],
                                            ["2217", "5004000", "瓦工", "brick layer"],
                                            ["2218", "5004000", "万能工", "fitting-up worker"],
                                            ["2220", "5004000", "钢筋工", "steel bender"],
                                            ["2221", "5004000", "学徒工", "apprentice"], ["345", "5004000", "其他", "Others"]],
                                           [["296", "121300", "医药代表", "Medical Sales Representative"],
                                            ["770", "121300", "医药销售经理/主管", "Medical Sales Manager/Supervisor"],
                                            ["766", "121300", "药品市场推广经理/主管", "Pharmaceutical Promotion Manager"],
                                            ["767", "121300", "药品市场推广专员/助理", "Pharmaceutical Promotion Specialist"],
                                            ["773", "121300", "医疗器械销售", "Medical Equipment Sales"],
                                            ["378", "121300", "医疗器械推广", "Medical Equipment Promotion"],
                                            ["775", "121300", "医药学术推广", "Pharmaceutical Academic Promotion"],
                                            ["496", "121300", "医药招商", "Pharmaceutical Business Development"],
                                            ["495", "121300", "医药项目管理", "Pharmaceutical Project Management"],
                                            ["769", "121300", "医药项目招投标管理", "Pharmaceutical Project Bidding Management"],
                                            ["292", "121300", "生物工程/生物制药", "Biotechnology/Bio-phamaceutics"],
                                            ["776", "121300", "药品研发", "Medicine R&D"],
                                            ["876", "121300", "医疗器械研发", "Medical Equipment R&D"],
                                            ["293", "121300", "临床研究员", "Clinical Researcher"],
                                            ["877", "121300", "临床协调员", "Clinical Coordinator"],
                                            ["765", "121300", "临床数据分析员", "Clinical Data Analyst"],
                                            ["763", "121300", "医药化学分析", "Medical Chemical Analyst"],
                                            ["764", "121300", "医药技术研发管理人员", "Pharmaceutical Technology R&D Management"],
                                            ["875", "121300", "药品注册", "Medicine Registration"],
                                            ["771", "121300", "医疗器械注册", "Medical Equipment Registration"],
                                            ["294", "121300", "药品生产/质量管理", "Pharmaceutical Manufacturing/QA/QC"],
                                            ["772", "121300", "医疗器械生产/质量管理", "Medical Equipment Manufacturing/QA/QC"],
                                            ["774", "121300", "医疗器械维修/保养", "Medical Equipment Repair/Maintenance"],
                                            ["2018", "121300", "临床推广经理", "Clinical promotion manager"],
                                            ["2019", "121300", "医药技术研发人员", "Pharmaceutical Technology r and d Specialist"],
                                            ["297", "121300", "其他", "Others"]],
                                           [["023", "120500", "化工工程师", "Chemical Engineer"],
                                            ["502", "120500", "化工研发工程师", "Chemical R&D Engineer"],
                                            ["396", "120500", "化学分析", "Chemical Analyst"],
                                            ["112", "120500", "化学技术应用", "Chemical Technical Application"],
                                            ["111", "120500", "化学操作", "Chemical Processing"],
                                            ["371", "120500", "化学制剂研发", "Chemical Agent R&D"],
                                            ["505", "120500", "油漆/化工涂料研发", "Paint/Coating R&D"],
                                            ["614", "120500", "塑料工程师", "Plastics Engineer"],
                                            ["504", "120500", "化学实验室技术员/研究员", "Chemical Lab Scientist/Researcher"],
                                            ["503", "120500", "化工项目管理", "Chemical Project Management"],
                                            ["2006", "120500", "橡胶工程师", "Rubber Processed Engineer"],
                                            ["2007", "120500", "配色技术员", "The color technician"],
                                            ["2008", "120500", "化妆品研发", "Cosmetics Scientist"],
                                            ["2009", "120500", "造纸研发", "Research and development of paper making"],
                                            ["2010", "120500", "化学/化工技术总监", "Director of chemical technology"],
                                            ["113", "120500", "其他", "Others"]], [["175", "2120000", "导演/编导", "Director"],
                                                                                 ["367", "2120000", "总编/副总编", "Chief Editor"],
                                                                                 ["180", "2120000", "艺术指导/舞美设计",
                                                                                  "Art Director/Stage Art Design"],
                                                                                 ["179", "2120000", "摄影师/摄像师",
                                                                                  "Photographer/Camera Operator"],
                                                                                 ["182", "2120000", "化妆师/造型师/服装/道具",
                                                                                  "Makeup Artist/Image Designer"],
                                                                                 ["177", "2120000", "主持人/司仪",
                                                                                  "Program/Events Host/Hostess"],
                                                                                 ["893", "2120000", "演员/模特",
                                                                                  "Actor(Actress)/Model"],
                                                                                 ["891", "2120000", "配音员",
                                                                                  "Dubbing Speicalist"],
                                                                                 ["890", "2120000", "音效师",
                                                                                  "Sound-effects Engineer"],
                                                                                 ["185", "2120000", "后期制作", "Post Production"],
                                                                                 ["178", "2120000", "经纪人/星探",
                                                                                  "Entertainment Agent"],
                                                                                 ["760", "2120000", "放映管理", "Projectionist"],
                                                                                 ["762", "2120000", "作家/编剧/撰稿人",
                                                                                  "Writer/Screenwriter"],
                                                                                 ["176", "2120000", "文字编辑/组稿", "Copy Editor"],
                                                                                 ["892", "2120000", "美术编辑/美术设计", "Art Editor"],
                                                                                 ["612", "2120000", "记者/采编", "Reporter"],
                                                                                 ["761", "2120000", "电话采编",
                                                                                  "Telephone Reporter"],
                                                                                 ["152", "2120000", "文案策划", "Copywriter"],
                                                                                 ["395", "2120000", "校对/录入",
                                                                                  "Proofreader/Typist"],
                                                                                 ["183", "2120000", "发行管理",
                                                                                  "Distribution Management"],
                                                                                 ["181", "2120000", "排版设计", "Layout Designer"],
                                                                                 ["533", "2120000", "印刷排版/制版",
                                                                                  "Typesetting Operation"],
                                                                                 ["613", "2120000", "印刷操作",
                                                                                  "Printing Operation"],
                                                                                 ["2121", "2120000", "编辑出版",
                                                                                  "Edition and publication"],
                                                                                 ["2122", "2120000", "主笔设计师",
                                                                                  "Project Designer"],
                                                                                 ["2123", "2120000", "放映员", "projectionist"],
                                                                                 ["2124", "2120000", "灯光师",
                                                                                  "lighting engineer"],
                                                                                 ["2125", "2120000", "艺术/设计总监",
                                                                                  "Design Director"],
                                                                                 ["2126", "2120000", "影视策划/制作人员",
                                                                                  "Entertainment Planning"],
                                                                                 ["2127", "2120000", "调色员", "Color by"],
                                                                                 ["2128", "2120000", "烫金工",
                                                                                  "gold finisher bookbinder"],
                                                                                 ["2129", "2120000", "晒版员", "Print member"],
                                                                                 ["2130", "2120000", "装订工", "bookbinder"],
                                                                                 ["2131", "2120000", "数码直印/菲林输出",
                                                                                  "Digital/Film Printing"],
                                                                                 ["2132", "2120000", "调墨技师", "Ink Technician"],
                                                                                 ["2133", "2120000", "电分操作员",
                                                                                  "Operator-Colour Distinguishing"],
                                                                                 ["2134", "2120000", "打稿机操作员", "Operator"],
                                                                                 ["2135", "2120000", "切纸机操作工",
                                                                                  "Paper cutter operators"],
                                                                                 ["2136", "2120000", "裱胶工", "Framed JiaoGong"],
                                                                                 ["2137", "2120000", "复卷工", "rewinderman"],
                                                                                 ["2138", "2120000", "压痕工", "indenting"],
                                                                                 ["2139", "2120000", "印刷机械机长",
                                                                                  "Printing Machine Operator"],
                                                                                 ["2140", "2120000", "转播工程师",
                                                                                  "Broadcast engineers"],
                                                                                 ["2141", "2120000", "视频主播",
                                                                                  "Broadcasting Jockey"],
                                                                                 ["186", "2120000", "其他", "Others"]],
                                           [["364", "2100708", "设计管理人员", "Design Management"],
                                            ["153", "2100708", "艺术/设计总监", "Art/Design Director"],
                                            ["753", "2100708", "绘画", "Painter/Illustrator"],
                                            ["754", "2100708", "原画师", "Original Artist"],
                                            ["608", "2100708", "CAD设计/制图", "CAD Design/Drawing"],
                                            ["149", "2100708", "平面设计", "Graphic Design"],
                                            ["554", "2100708", "三维/3D设计/制作", "3D Design/Production"],
                                            ["555", "2100708", "Flash设计/开发", "Flash Design"],
                                            ["673", "2100708", "特效设计", "Special Effects Design"],
                                            ["674", "2100708", "视觉设计", "Visual Design"],
                                            ["862", "2100708", "用户体验（UE/UX）设计", "UE/UX Design"],
                                            ["184", "2100708", "美术编辑/美术设计", "Art Editor"],
                                            ["151", "2100708", "多媒体/动画设计", "Multimedia/Animation Design"],
                                            ["150", "2100708", "包装设计", "Package Design"],
                                            ["366", "2100708", "家具设计", "Furniture Design"],
                                            ["751", "2100708", "家居用品设计", "Household Product Design"],
                                            ["365", "2100708", "工艺品/珠宝设计", "Artwork/Jewelry Design"],
                                            ["752", "2100708", "玩具设计", "Toy Design"],
                                            ["755", "2100708", "店面/展览/展示/陈列设计", "Exhibition/Display/Storefront Design"],
                                            ["750", "2100708", "工业设计", "Industrial Design"],
                                            ["867", "2100708", "游戏界面设计", "Game UI Design"],
                                            ["2118", "2100708", "园林景观设计师", "oversea garden landscape designer"],
                                            ["2119", "2100708", "平面设计总监", "Graphic design director"],
                                            ["2120", "2100708", "平面设计经理/主管", "CREATIVE CONTENT MANAGER"],
                                            ["157", "2100708", "其他", "Others"]],
                                           [["216", "2140000", "咨询总监", "Consulting Director"],
                                            ["217", "2140000", "咨询经理/主管", "Consulting Manager/Supervisor"],
                                            ["219", "2140000", "咨询顾问/咨询员", "Consultant"],
                                            ["220", "2140000", "专业顾问", "Professional Advisor"],
                                            ["623", "2140000", "调研员", "Researcher"],
                                            ["894", "2140000", "数据分析师", "Data Analyst"],
                                            ["221", "2140000", "情报信息分析", "Intelligence Analyst"],
                                            ["781", "2140000", "猎头顾问/助理", "Headhunter/Assistant"],
                                            ["783", "2140000", "咨询项目管理", "Consulting Project Management"],
                                            ["2142", "2140000", "咨询师", "counselor"], ["222", "2140000", "其他", "Others"]],
                                           [["361", "2090000", "幼教", "Preschool Education"],
                                            ["628", "2090000", "小学教师", "Elementary Teacher"],
                                            ["627", "2090000", "初中教师", "Junior High School Teacher"],
                                            ["625", "2090000", "高中教师", "Senior High School Teacher"],
                                            ["358", "2090000", "大学教师", "University Lecturer"],
                                            ["626", "2090000", "职业技术教师", "Technical School Teacher"],
                                            ["359", "2090000", "家教", "Tutor"], ["785", "2090000", "兼职教师", "Part-time Teacher"],
                                            ["791", "2090000", "理科教师", "Science Teacher"],
                                            ["792", "2090000", "文科教师", "Liberal Arts Teacher"],
                                            ["793", "2090000", "外语教师", "Foreign Language Teacher"],
                                            ["790", "2090000", "音乐教师", "Music Teacher"],
                                            ["906", "2090000", "美术教师", "Art Teacher"],
                                            ["360", "2090000", "体育老师/教练", "Physical Teacher/Coach"],
                                            ["624", "2090000", "校长/副校长", "Principal"],
                                            ["132", "2090000", "教学/教务管理人员", "Educational Administration"],
                                            ["786", "2090000", "培训督导", "Training Supervisor"],
                                            ["131", "2090000", "培训师/讲师", "Trainer"],
                                            ["788", "2090000", "培训助理/助教", "Training Assistant"],
                                            ["135", "2090000", "教育产品开发", "Educational Products R&D"],
                                            ["787", "2090000", "培训策划", "Training Planning"],
                                            ["789", "2090000", "培训/招生/课程顾问", "Enrollment/Course Consultant"],
                                            ["2114", "2090000", "大学教授", "University Professors"],
                                            ["2115", "2090000", "舞蹈老师", "Dance Instructor"],
                                            ["2116", "2090000", "外籍教师", "Foreign teacher"],
                                            ["2117", "2090000", "特教(特殊教育)", "Special (special education"],
                                            ["134", "2090000", "其他", "Others"]],
                                           [["225", "2080000", "法务经理/主管", "Legal Affairs Manager/Supervisor"],
                                            ["629", "2080000", "法务专员/助理", "Legal Affairs Specialist/Assistant"],
                                            ["223", "2080000", "律师", "Lawyer"], ["860", "2080000", "律师助理", "Paralegal"],
                                            ["363", "2080000", "企业律师/合规经理/主管", "Corporate Attorney/Compliance Manager"],
                                            ["224", "2080000", "企业律师/合规顾问", "Corporate Attorney/Compliance Consultant"],
                                            ["226", "2080000", "知识产权/专利顾问/代理人", "Intellectual Property/Patent Advisor"],
                                            ["497", "2080000", "合同管理", "Contract Management"],
                                            ["2113", "2080000", "合规经理", "Compliance Manager"],
                                            ["227", "2080000", "其他", "Others"]],
                                           [["268", "2120500", "英语翻译", "English Translator"],
                                            ["271", "2120500", "法语翻译", "French Translator"],
                                            ["269", "2120500", "日语翻译", "Japanese Translator"],
                                            ["270", "2120500", "德语翻译", "German Translator"],
                                            ["272", "2120500", "俄语翻译", "Russian Translator"],
                                            ["630", "2120500", "西班牙语翻译", "Spanish Translator"],
                                            ["631", "2120500", "意大利语翻译", "Italian Translator"],
                                            ["632", "2120500", "葡萄牙语翻译", "Portuguese Translator"],
                                            ["633", "2120500", "阿拉伯语翻译", "Arabic Translator"],
                                            ["273", "2120500", "韩语/朝鲜语翻译", "Korean Translator"],
                                            ["274", "2120500", "其他语种翻译", "Others"]],
                                           [["895", "5005000", "店长/卖场管理", "Store Manager"],
                                            ["016", "5005000", "楼面管理", "Floor Management"],
                                            ["493", "5005000", "品牌/连锁招商管理", "Brand/Chain Store Business Development"],
                                            ["276", "5005000", "大堂经理/领班", "Lobby Manager/Supervisor"],
                                            ["281", "5005000", "酒店管理", "Hotel Management"],
                                            ["636", "5005000", "客房管理", "Guest Room Management"],
                                            ["794", "5005000", "收银主管", "Cashier Supervisor"],
                                            ["354", "5005000", "收银员", "Cashier"],
                                            ["017", "5005000", "店员/营业员/导购员", "Shop Assistant"],
                                            ["355", "5005000", "理货员", "Order Picker"],
                                            ["896", "5005000", "促销主管/督导", "Promotion Supervisor"],
                                            ["173", "5005000", "促销员", "Promoter"],
                                            ["634", "5005000", "品类管理", "Category Management"],
                                            ["277", "5005000", "前厅接待/礼仪/迎宾", "Usher/Concierge"],
                                            ["796", "5005000", "预订员", "Reservation Staff"],
                                            ["798", "5005000", "行李员", "Bellperson"],
                                            ["279", "5005000", "服务员", "Waiter/Waitress"],
                                            ["492", "5005000", "防损员/内保", "Loss Prevention"],
                                            ["494", "5005000", "奢侈品销售", "luxury Sales"],
                                            ["637", "5005000", "主持人/司仪", "Program/Events Host/Hostess"],
                                            ["2222", "5005000", "客房服务员", "hotel attendants"],
                                            ["2223", "5005000", "生鲜食品加工/处理", "Fresh food processing"],
                                            ["2224", "5005000", "酒店试睡员", "hotel connoisseur"],
                                            ["2225", "5005000", "门卫", "gate guard"],
                                            ["2226", "5005000", "质量管理", "quality control"], ["357", "5005000", "其他", "Others"]],
                                           [["799", "4040000", "旅游产品销售", "Tourism Product Sales"],
                                            ["530", "4040000", "旅游顾问", "Travel Consultant"],
                                            ["282", "4040000", "导游/票务", "Tour Guide/Ticket Service"],
                                            ["531", "4040000", "旅游计划调度", "Travel Scheduling"],
                                            ["897", "4040000", "旅游产品/线路策划", "Tourism Product Planning"],
                                            ["800", "4040000", "签证业务办理", "Visa services"], ["2171", "4040000", "潜水员", "Diver"],
                                            ["2172", "4040000", "海外游计调", "Overseas tour plan adjustment"],
                                            ["2173", "4040000", "水族馆表演演员", "Aquarium show actor"],
                                            ["283", "4040000", "其他", "Others"]], [["275", "201100", "厨师/面点师", "Cook/Baker"],
                                                                                  ["635", "201100", "食品加工/处理",
                                                                                   "Food Processing"],
                                                                                  ["369", "201100", "调酒师/茶艺师/咖啡师",
                                                                                   "Bartender/Tea Maker/Barista"],
                                                                                  ["370", "201100", "营养师",
                                                                                   "Nutritionist/Dietitian"],
                                                                                  ["801", "201100", "厨工", "Cooking Assistant"],
                                                                                  ["596", "201100", "食品/饮料研发",
                                                                                   "Food/Beverage Development"],
                                                                                  ["836", "201100", "食品/饮料检验",
                                                                                   "Food/Beverage Quality Control"],
                                                                                  ["2066", "201100", "餐厅领班", "headwaiter"],
                                                                                  ["2067", "201100", "餐厅服务员", "Mess boy"],
                                                                                  ["2068", "201100", "行政主厨", "Executive Chef"],
                                                                                  ["2069", "201100", "中餐厨师",
                                                                                   "Executive Chinese Chef"],
                                                                                  ["2070", "201100", "西餐厨师",
                                                                                   "Executive Sous Chef"],
                                                                                  ["2071", "201100", "日式厨师",
                                                                                   "Commis-Japanese Cuisine"],
                                                                                  ["2072", "201100", "西点师",
                                                                                   "West Point Division"],
                                                                                  ["2073", "201100", "厨师助理/学徒",
                                                                                   "Chief Chef Assistant"],
                                                                                  ["2074", "201100", "送餐员", "Order Taker"],
                                                                                  ["2075", "201100", "传菜员", "Runner"],
                                                                                  ["2076", "201100", "烧烤师", "BBQ Chef"],
                                                                                  ["2077", "201100", "品酒师", "Sommelier"],
                                                                                  ["2078", "201100", "杂工", "Odd-jobs"],
                                                                                  ["837", "201100", "其他", "Others"]],
                                           [["377", "2050000", "美发/发型师", "Hair Stylist"],
                                            ["640", "2050000", "化妆师", "Cosmetician"],
                                            ["639", "2050000", "美容师/美甲师", "Beautician/Nail Beauty"],
                                            ["802", "2050000", "美容顾问(BA)", "Beauty Advisor"],
                                            ["376", "2050000", "健身/美体/舞蹈教练", "Fitness/Body/Dance Instructor"],
                                            ["641", "2050000", "按摩/足疗", "Massage/Foot Massage"],
                                            ["638", "2050000", "救生员", "Life Guard"],
                                            ["2084", "2050000", "美发培训师", "Hairdressing trainer"],
                                            ["2085", "2050000", "游泳教练", "swimming coach"],
                                            ["2086", "2050000", "高尔夫教练", "Golf Coach"],
                                            ["2087", "2050000", "瑜伽教练", "YOGA Instructor"],
                                            ["2088", "2050000", "户外/游戏教练", "The game the coach"],
                                            ["2089", "2050000", "美体师", "herapist"],
                                            ["2090", "2050000", "美容整形师", "Plastic Surgeon"],
                                            ["234", "2050000", "其他", "Others"]],
                                           [["228", "2051000", "医疗管理人员", "Medical Management"],
                                            ["229", "2051000", "综合门诊/全科医生", "General Practitioner (GP)"],
                                            ["642", "2051000", "内科医生", "Internist"], ["643", "2051000", "外科医生", "Surgeon"],
                                            ["644", "2051000", "儿科医生", "Pediatrician"], ["645", "2051000", "牙科医生", "Dentist"],
                                            ["899", "2051000", "美容整形科医生", "Plastic Surgeon"],
                                            ["646", "2051000", "中医科医生", "Chinese Medicine Doctor"],
                                            ["647", "2051000", "麻醉医生", "Anesthetist"],
                                            ["373", "2051000", "心理医生", "Psychologist"],
                                            ["648", "2051000", "眼科医生/验光师", "Oculist/Optometrist"],
                                            ["900", "2051000", "医学影像/放射科医师", "Radiology Therapist"],
                                            ["374", "2051000", "化验/检验科医师", "Laboratory Physician"],
                                            ["232", "2051000", "药房管理/药剂师", "Pharmacist"],
                                            ["804", "2051000", "理疗师", "Physical Therapist"],
                                            ["898", "2051000", "兽医", "Veterinarian"],
                                            ["397", "2051000", "护士/护理人员", "Nurse/Medical Assistant"],
                                            ["649", "2051000", "营养师", "Nutritionist/Dietitian"],
                                            ["375", "2051000", "针灸/推拿", "Acupuncturist"],
                                            ["2091", "2051000", "验光师", "optometrist"],
                                            ["2092", "2051000", "公共卫生/疾病监控", "ailment monitoring"],
                                            ["2093", "2051000", "护理主任/护士长", "head nurse"], ["2094", "2051000", "院长", "dean"],
                                            ["2095", "2051000", "专科医生", "specialist"], ["650", "2051000", "其他", "Others"]],
                                           [["805", "6270000", "保安经理", "Security Manager"],
                                            ["104", "6270000", "保安", "Security Guards"],
                                            ["308", "6270000", "家政人员", "Housekeeper"],
                                            ["611", "6270000", "婚礼/庆典策划服务", "Wedding/Celebration Planning"],
                                            ["233", "6270000", "宠物护理和美容", "Pet Care & Beauty"],
                                            ["901", "6270000", "保姆/母婴护理", "House Maid/Baby Sitter"],
                                            ["806", "6270000", "搬运工", "Mover"], ["651", "6270000", "保洁", "Cleaner"],
                                            ["2227", "6270000", "钟点工", "part-timer"],
                                            ["2228", "6270000", "月嫂", "maternity matron"],
                                            ["2229", "6270000", "家电维修", "Appliance Repairing"],
                                            ["310", "6270000", "其他", "Others"]],
                                           [["284", "130000", "石油/天然气技术人员", "Oil/Gas Technician"],
                                            ["285", "130000", "空调/热能工程师", "Air-Conditioner/Thermal Engineer"],
                                            ["290", "130000", "核力/火力工程师", "Nuclear/Fire Power Engineer"],
                                            ["617", "130000", "水利/水电工程师", "Water Conservancy/Hydroelectricity Engineer"],
                                            ["286", "130000", "电力工程师/技术员", "Electric Power Engineer"],
                                            ["372", "130000", "地质勘查/选矿/采矿", "Geological Exploration"],
                                            ["534", "130000", "能源/矿产项目管理", "Energy/Mining Project Management"],
                                            ["2020", "130000", "电力系统研发工程师",
                                             "Research and development of electric power system engineers"],
                                            ["2021", "130000", "电力电子研发工程师", "Power Engineer"],
                                            ["2022", "130000", "控制保护研发工程师", "R&d engineers control protection"],
                                            ["291", "130000", "其他", "Others"]],
                                           [["380", "2023100", "环保技术工程师", "Environmental Engineer"],
                                            ["616", "2023100", "环境评价工程师", "Environmental Assessment Engineer"],
                                            ["905", "2023100", "环境监测工程师", "Environmental Monitoring Engineer"],
                                            ["615", "2023100", "水处理工程师", "Water Treatment Engineer"],
                                            ["903", "2023100", "固废处理工程师", "Solid Waste Treatment Engineer"],
                                            ["904", "2023100", "废气处理工程师", "Exhaust Gas Treatment Engineer"],
                                            ["266", "2023100", "生态治理/规划", "Ecological Management/Planning"],
                                            ["379", "2023100", "环境管理/园林景区保护", "Environmental Management/Landscape Protection"],
                                            ["267", "2023100", "其他", "Others"]],
                                           [["2000", "100000", "插花设计师", "Flower arrangement designer"],
                                            ["656", "100000", "农艺师", "Agro-Technician"],
                                            ["914", "100000", "林业技术人员", "Forestry Technician"],
                                            ["915", "100000", "园艺师", "Gardener/Horticulturist"],
                                            ["657", "100000", "畜牧师", "Animal Husbandry Technician"],
                                            ["655", "100000", "动物育种/养殖", "Culturist"],
                                            ["913", "100000", "动物营养/饲料研发", "Animal nutrition/Feed Development"],
                                            ["654", "100000", "饲料销售", "Feed Sales"], ["264", "100000", "其他", "Others"]],
                                           [["305", "200100", "公务员/事业单位人员", "Civil Servant"],
                                            ["362", "200100", "科研管理人员", "Scientific Research Management"],
                                            ["255", "200100", "科研人员", "Scientific Researcher"],
                                            ["306", "200100", "其他", "Others"]],
                                           [["299", "5006000", "实习生", "Intern"], ["302", "5006000", "培训生", "Trainee"],
                                            ["301", "5006000", "储备干部", "Associate Trainee"],
                                            ["381", "5006000", "其他", "Others"]], [["658", "200700", "志愿者/义工", "Volunteer"],
                                                                                  ["838", "200700", "社会工作者/社工",
                                                                                   "Social Worker"],
                                                                                  ["839", "200700", "其他", "Others"]],
                                           [["659", "300100", "兼职", "Part-time Jobs"],
                                            ["300", "300100", "临时", "Temporary Jobs"],
                                            ["2143", "300100", "国外求职", "Major English recruitment websites abroad"],
                                            ["303", "300100", "其他", "Others"]], [["304", "300200", "其他", "Others"]]]}
                if tj_data["job"] != []:
                    zntj_temp = []
                    for tj_1 in tj_data["job"]:
                        if '#' in tj_1:
                            da_tj = tj_1.split('#')[0].strip()
                            xiao_tj = tj_1.split('#')[1].strip()
                            for zn_index, zn_1 in enumerate(dict_zhi_n['parents']):
                                if da_tj in ''.join(zn_1):
                                    # print(da_tj)
                                    for child_1 in dict_zhi_n['children'][zn_index]:
                                        if xiao_tj in ''.join(child_1):
                                            # print(child_1[0])
                                            zntj_temp.append(child_1[0])
                        else:
                            for parent_1 in dict_zhi_n['parents']:
                                if tj_1.strip() in ''.join(parent_1):
                                    # print(parent_1[0])
                                    zntj_temp.append(parent_1[0])
                    job_num = ';'.join(zntj_temp)
                    pay_load["S_DESIRED_JOB_TYPE"] = job_num
            except:
                pass
            # print(pay_load)
            now_time = str(int(time.time() * 1000))
            headers = {
                'User-Agent': get_useragent(),
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                # 'Accept-Encoding':'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'Connection': 'keep-alive',
                'Content-Length': '415',
                'Content-Type': 'text/plain',
                'Cookie': cookie,
                # 'Cookie': 'JSSearchModel=0; adfbid2=0; LastSearchHistory=%7b%22Id%22%3a%22339242f3-85b9-4958-9749-d8b0e389a203%22%2c%22Name%22%3a%22%e6%9d%ad%e5%b7%9e%e9%80%9a%e5%ae%bd%e5%b9%bf%e7%bd%91%e7%bb%9c%e6%8a%80%e6%9c%af%e6%9c%89%e9%99%90%e5%85%ac%e5%8f%b8+%2b+%e5%85%a8%e5%9b%bd%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fp%3d1%26jl%3d%25e6%25b5%2599%25e6%25b1%259f%25e7%259c%2581%25e6%259d%25ad%25e5%25b7%259e%25e5%25b8%2582%25e6%25b7%25b3%25e5%25ae%2589%25e5%258e%25bf%26kw%3d%25e6%259d%25ad%25e5%25b7%259e%25e9%2580%259a%25e5%25ae%25bd%25e5%25b9%25bf%25e7%25bd%2591%25e7%25bb%259c%25e6%258a%2580%25e6%259c%25af%25e6%259c%2589%25e9%2599%2590%25e5%2585%25ac%25e5%258f%25b8%22%2c%22SaveTime%22%3a%22%5c%2fDate(1528083176506%2b0800)%5c%2f%22%7d; login_point=35828671; NTKF_T2D_CLIENTID=guestB9DFEA98-1C5E-AA47-3ED7-CD91DAFD3321; sts_deviceid=163cd91dccd43d-0804b8fcaf563f-5b163f13-1049088-163cd91dcce222; _jzqy=1.1528716623.1528716623.1.jzqsr=baidu|jzqct=%E6%99%BA%E8%81%94%E6%8B%9B%E8%81%98.-; LastCity=%e6%9d%ad%e5%b7%9e; LastCity%5Fid=653; urlfrom2=121123457; adfcid2=sogoupz_zbt; zp-route-meta=uid=132309766,orgid=35828671; urlfrom=121123457; adfcid=sogoupz_zbt; adfbid=0; dywec=95841923; dywez=95841923.1529458691.41.6.dywecsr=zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/mp.html; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1528716622,1528763349,1529376124,1529458691; __utmc=269921210; __utmz=269921210.1529458691.26.6.utmcsr=zhaopin.com|utmccn=(referral)|utmcmd=referral|utmcct=/mp.html; _jzqa=1.3135276436143376000.1527662491.1529407236.1529458691.29; _jzqc=1; _jzqx=1.1527677343.1529458691.4.jzqsr=sou%2Ezhaopin%2Ecom|jzqct=/jobs/searchresult%2Eashx.jzqsr=zhaopin%2Ecom|jzqct=/mp%2Ehtml; __xsptplus30=30.5.1529458691.1529458691.1%231%7Cother%7Ccnt%7C121113803%7C%7C%23%23bJJTfGjaT4p-CL8-XAOJYZVHWEkaSoFJ%23; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1529458693; __zpWAM=1528716625873.348889.1528763352.1529458693.3; __zpWAMs2=1; at=8a42e0218b8641a0940a9b185c3ef0df; Token=8a42e0218b8641a0940a9b185c3ef0df; rt=3cc9f2b443b845d880452cc0e626dfb1; RDsUserInfo=3d692e695671467156775b755a6a547549775f695c695d714c7129772775546a0e751f77016904695071247131775475586a5f7532772c695769587142715d775b75516a52754777596951692a71237158775f75446a5675407748695369517144715d775275286a28754d77586951693e713671587723753b6a577542775b695a695271407153775f75516a5f7525773c6957695a714171557752753a6a2d754d775b6951696; uiioit=3d753d6a44640838586d5c62053554684c795d7952390e6b566e2036716455754a6a4c640138596d566200355368447951799; nTalk_CACHE_DATA={uid:kf_9051_ISME9754_35828671,tid:1529458713977275}; adShrink=1; sts_sg=1; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2Forg%2Flogin%3FDYWE%3D1528716625873.348889.1528763352.1529458693.3; dywea=95841923.2867715207976167400.1527662491.1529458691.1529475976.42; __utma=269921210.2124496823.1527662491.1529458691.1529475976.27; __utmt=1; sts_sid=1641bdf9355176-03c4dd979e2f3d-5b183a13-1049088-1641bdf93561df; sts_evtseq=3; dyweb=95841923.7.10.1529475976; __utmb=269921210.7.10.1529475976',
                'Host': 'rdapi.zhaopin.com',
                'Origin': 'https://rd5.zhaopin.com',
                'Referer': 'https://rd5.zhaopin.com/search/result',
                'zp-route-meta': meta
            }
            url_ss="https://rdapi.zhaopin.com/rd/search/resumeList?_="+now_time
            response_ss = requests.post(url=url_ss, headers=headers, data=json.dumps(pay_load)).text
            time.sleep(random.uniform(3, 5))
            # print(response_ss)
            dict_xinxi=json.loads(response_ss)
            dict_data=dict_xinxi["data"]
            list_jl=dict_data["dataList"]
            #判断是否存在下一页
            if len(list_jl) == 30:
                # print("下一页")
                page_num=page_num+1
            elif len(list_jl) < 30:
                flag = False
                # print("跳出")
            # orgid=meta.split('orgid=')[1].replace(" ","")
            resp_li_all=ask_new(list_jl, orgid, job_id)
            # print(resp_li_all)

            today=str(datetime.date.today())
            data_wu_zl=[]

            # for resp_li in resp_li_all:
            for li_index, resp_li in enumerate(resp_li_all):
                    # print("判断通过")
                    for jl_index, dict_jl in enumerate(list_jl[0:]):
                        if resp_li == '1' and li_index == jl_index:
                            modifyDate="20"+dict_jl["modifyDate"]
                            #判断更新时间是否为当天,获取指定简历的链接地址
                            # print(dict_jl)
                            if modifyDate == today:
                                d_pos = {"id":dict_jl["id"]}
                                postdata_str = str(parse.urlencode(d_pos).encode('utf-8'))
                                # key_word=postdata_str.split("kw=")[1].split("&")[0].replace("'","")
                                jl_id=postdata_str.split("id=")[1].split("&")[0].replace("'","")
                                resumeNo= jl_id+"_1_1%3B" + dict_jl["k"] +"%3B"+dict_jl["t"]
                                url_jl="https://rd5.zhaopin.com/resume/detail?"+"resumeNo="+ resumeNo +"&openFrom=1"
                                #获取简历页面的json文件
                                headers_jl={
                                'User-Agent': get_useragent(),
                                'Accept': 'application/json, text/javascript, */*; q=0.01',
                                # 'Accept-Encoding':'gzip, deflate, br',
                                'Accept-Language': 'zh-CN,zh;q=0.8',
                                'Connection': 'keep-alive',
                                'Cookie': cookie,
                                'Host': 'rdapi.zhaopin.com',
                                'Origin': 'https://rd5.zhaopin.com',
                                'Referer': url_jl,
                                'zp-route-meta': meta
                                }
                                url_json="https://rdapi.zhaopin.com/rd/resume/detail?_="+now_time+"&resumeNo="+resumeNo
                                time.sleep(random.uniform(3, 5))
                                response_json=requests.get(url=url_json,headers=headers_jl).text
                                # print(response_json)
                                # orgid=meta.split("orgid=")[1].strip()
                                try:
                                    zl_data=jl_jiexi(xinxi=dict_jl,text_json=response_json,org_id=orgid,job_id=job_id,resume_type=2)
                                    # print(zl_data)
                                    data_wu_zl.append(zl_data)
                                except:
                                    pass
                                if len(data_wu_zl) == 3:
                                    data = json.dumps(data_wu_zl)
                                    data = data.encode('utf-8')
                                    resp_page = requests.post(url=wu_jl_url, data=data)
                                    # print('3个了')
                                    yxz_num = yxz_num + 3
                                    # print(yxz_num)
                                    if yxz_num >= 50:
                                        # print('够50个了', '**'*100)
                                        flag = False
                                        return yxz_num
                                    data_wu_zl = []


            if len(data_wu_zl) == 3 or len(data_wu_zl) == 0:
                pass
            else:
                yxz_num = len(data_wu_zl) + yxz_num
                data = json.dumps(data_wu_zl)
                data = data.encode('utf-8')
                resp_page = requests.post(url=wu_jl_url, data=data)
                # print('不够我也传了')

        except:
            flag = False
            traceback.print_exc()
            logging.exception("Exception Logged")
            pass
    # print(2)
    return yxz_num


#简历解析
def jl_jiexi(xinxi,text_json,org_id,job_id,resume_type):
    dict_jl=json.loads(text_json)
    # print(dict_jl)
    dict_data=dict_jl["data"]
    detail=dict_data["detail"]
    #个人信息
    candidate=dict_data["candidate"]
    #开始解析
    zl_data = {}
    #简历主表
    try:
        zl_data['info'] = {}
        zl_data['info']['channel'] = 1
        zl_data['info']['channel_resume_id'] = dict_data["resumeNumber"].replace("_1_1","")
        zl_data['info']['name'] = candidate["userName"]
        zl_data['info']['birth_year'] = int(candidate["birthYear"])
        zl_data['info']['degree'] = xinxi["eduLevel"]
        zl_data['info']['sex'] = xinxi["gender"]
        zl_data['info']['current_address'] = xinxi["city"]
        zl_data['info']['update_time'] = "20"+xinxi["modifyDate"]
    except:
        pass
    try:
        if  candidate["mobilePhone"] != "":
            zl_data['info']['mobilephone'] = candidate["mobilePhone"]
        if  candidate["email"] != "":
            zl_data['info']['email'] = candidate["email"]
    except:
        pass

    #求职意向
    try:
        zl_data['objective'] = {}
        zl_data['objective']['self_evaluation'] =detail["CommentContent"].replace("\r", "").replace("\n","").replace("\t","").replace(" ","")
    except:
        pass
    try:
        salary=xinxi["desiredSalary"]  #薪资要求
        if '保密'  in salary or '面议'  in salary:
            zl_data['objective']['expected_salary_lower'] = int(0)
            zl_data['objective']['expected_salary_upper'] = int(0)
        elif '-' in salary :
            zl_data['objective']['expected_salary_lower'] = int(salary.replace("元/月", "").split('-')[0].strip())
            zl_data['objective']['expected_salary_upper'] = int(salary.replace("元/月", "").split('-')[1].strip())
        elif "以" in salary:
            zl_data['objective']['expected_salary_lower'] = int(salary.replace("元/月", "").split('以')[0].strip())
            zl_data['objective']['expected_salary_upper'] = int(salary.replace("元/月", "").split('以')[0].strip())
    except:
        pass
    zl_data['objective']['expected_address'] = []   #期望工作地点
    desireCity=xinxi['desireCity']
    try:
        for expected_address in desireCity.split(";")[0:]:
            zl_data['objective']['expected_address'].append(expected_address)
        zl_data['objective']['expected_job_title'] = []   #期望职业
        jobType = xinxi['jobType']
    except:
        pass
    try:
        for expected_job_title in jobType.split(";")[0:]:
            zl_data['objective']['expected_job_title'].append(expected_job_title)
        zl_data['objective']['job_nature'] = []            #工作性质
        employment = xinxi['employment']
    except:
        pass
    try:
        for job_nature in employment.split(";")[0:]:
            zl_data['objective']['job_nature'].append(job_nature)
    except:
        pass

    #工作经历
    try:
        WorkExperience = detail["WorkExperience"]
        if str(WorkExperience) != "[]":
            zl_data['jobs'] = []
            try:
                for  job_xinxi in WorkExperience[0:]:
                    train_dic={}
                    train_dic['company']=job_xinxi["CompanyName"]     #公司名称
                    train_dic['job_title']=job_xinxi["JobTitle"]      #职位名称
                    train_dic['job_title']=job_xinxi["JobTitle"]      #职位名称
                    train_dic['during_start']=job_xinxi["DateStart"].split(" ")[0]     #开始时间
                    DateEnd=job_xinxi["DateEnd"].split(" ")[0]    #结束时间
                    if DateEnd == "":
                        train_dic['during_end']="2099-01-01"
                    else:
                        train_dic['during_end'] = DateEnd
                    train_dic['job_content'] = job_xinxi["WorkDescription"].replace("\r", "").replace("\n", "").replace("\t", "").strip()  # 工作内容
                    # if job_xinxi["CompanySize"] != "":        # 公司规模
                    #     train_dic['company_scale'] = job_xinxi["CompanySize"]
                    zl_data['jobs'].append(train_dic)
            except:
                pass
    except:
        pass

    #项目经历
    try:
        ProjectExperience = detail["ProjectExperience"]
        if str(ProjectExperience) != "[]":
            zl_data['projects'] = []
            try:
                for pro_xinxi in ProjectExperience[0:]:
                    pro_dic = {}
                    pro_dic['title'] = pro_xinxi["ProjectName"]  # 项目名称
                    pro_dic['description'] = pro_xinxi["ProjectDescription"].replace("\r", "").replace("\n", "").replace("\t", "").strip()  # 项目描述
                    pro_dic['duty'] = pro_xinxi["ProjectResponsibility"].replace("\r", "").replace("\n", "").replace("\t", "").strip()  # 项目责任
                    pro_dic['during_start'] = pro_xinxi["DateStart"].split(" ")[0]  # 开始时间
                    DateEnd = pro_xinxi["DateEnd"].split(" ")[0]  # 结束时间
                    if DateEnd == "":
                        pro_dic['during_end'] = "2099-01-01"
                    else:
                        pro_dic['during_end'] = DateEnd
                    zl_data['projects'].append(pro_dic)
            except:
                pass
    except:
        pass
    #教育经历
    try:
        EducationExperience = detail["EducationExperience"]
        if str(EducationExperience) != "[]":
            zl_data['educations'] = []
            try:
                for edu_xinxi in EducationExperience[0:]:
                    edu_dic = {}
                    edu_dic['school'] = edu_xinxi["SchoolName"]  # 学校名称
                    edu_dic['major'] = edu_xinxi["MajorName"]  # 专业名称
                    # edu_dic['degree'] = edu_xinxi["MajorName"]  # 学历
                    edu_dic['during_start'] = edu_xinxi["DateStart"].split(" ")[0]  # 开始时间
                    DateEnd = edu_xinxi["DateEnd"].split(" ")[0]  # 结束时间
                    if DateEnd == "":
                        edu_dic['during_end'] = "2099-01-01"
                    else:
                        edu_dic['during_end'] = DateEnd
                    zl_data['educations'].append(edu_dic)
            except:
                pass
    except:
        pass

    #培训经历
    try:
        Training = detail["Training"]
        if  str(Training) != "[]":
            zl_data['trainings'] = []
            try:
                for tra_xinxi in Training[0:]:
                    tra_dic = {}
                    tra_dic['training_agency'] = tra_xinxi["Machinery"]  # 培训机构
                    tra_dic['training_course'] = tra_xinxi["TrainingName"]  # 培训课程
                    tra_dic['training_address'] = tra_xinxi["CityName"]  # 培训地点
                    tra_dic['certificate'] = tra_xinxi["CertificateName"]  # 获得证书
                    tra_dic['description'] = tra_xinxi["TrainingDescription"].replace("\r", "").replace("\n", "").replace("\t", "").strip()  # 培训介绍
                    tra_dic['during_start'] = tra_xinxi["DateStart"].split(" ")[0]  # 开始时间
                    DateEnd = tra_xinxi["DateEnd"].split(" ")[0]  # 结束时间
                    if DateEnd == "":
                        tra_dic['during_end'] = "2099-01-01"
                    else:
                        tra_dic['during_end'] = DateEnd
                    zl_data['trainings'].append(tra_dic)
            except:
                pass
    except:
        pass
    # 所获证书
    try:
        AchieveCertificate = detail["AchieveCertificate"]
        if str(AchieveCertificate) != "[]":
            zl_data['credentials'] = []
            for ach_xinxi in AchieveCertificate[0:]:
                ach_dic = {}
                ach_dic['title'] = ach_xinxi["CertificateName"]  # 证书名称
                ach_dic['get_date'] = ach_xinxi["AchieveDate"].split(" ")[0]  # 获得时间
                zl_data['credentials'].append(ach_dic)
    except:
        pass
    # 语言及技能
    try:
        LanguageSkill = detail["LanguageSkill"]
        ProfessionnalSkill= detail["ProfessionnalSkill"]
        if str(LanguageSkill) != "[]" or str(ProfessionnalSkill) != "[]":
            zl_data['languages'] = []
            try:
                if str(LanguageSkill) != "[]" :    #语言
                    for lan_xinxi in LanguageSkill[0:]:
                        lan_dic = {}
                        lan_dic['language'] = lan_xinxi["LanguageName"]  # 语种
                        lan_dic['writing'] = lan_xinxi["ReadWriteSkill"]  # 读写能力
                        lan_dic['speaking'] = lan_xinxi["HearSpeakSkill"]  # 听说能力
                        zl_data['languages'].append(lan_dic)
            except:
                pass
            try:
                if str(ProfessionnalSkill) != "[]":
                    for profe_xinxi in ProfessionnalSkill[0:]: #技能
                        profe_dic = {}
                        profe_dic['skill'] = profe_xinxi["SkillName"]  # 技能名称
                        profe_dic['duration'] = profe_xinxi["UsedMonths"]+"个月"  # 使用时间
                        profe_dic['level'] = profe_xinxi["MasterDegree"]  # 掌握程度
                        zl_data['languages'].append(profe_dic)
            except:
                pass
    except:
        pass
    #org
    zl_data['org'] = {}
    zl_data['org']['resume_type'] = resume_type
    zl_data['org']['org_id'] = org_id
    try:
        if zl_data['info']['mobilephone']:
            zl_data['org']['download_status'] = 1
    except:
        zl_data['org']['download_status'] = 0
    # 推荐时间
    zl_data['org']['receive_time'] = str(datetime.datetime.now())[0:10]

    # 工作ID
    try:
        if job_id != "":
            zl_data['org']['job_id'] =job_id
    except:
        pass
    # print(zl_data)
    return zl_data



