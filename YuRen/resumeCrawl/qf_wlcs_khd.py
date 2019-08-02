#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
import request
import urllib.parse


# 外网可以，内网不可以，可能不是构建服务器的问题，可能是发送网址的问题
url_to_js = 'http://127.0.0.1:8900/JsPython?account=qf9999'
# url_to_js = 'http://127.0.0.1:9600'
# url_to_js = 'http://192.168.1.164:8070/crawler/param'
# url = 'https://www.jianshu.com/p/bab98f95b6d3'
# data_to_js = {}
# data_to_js['PythonToJs'] = {}
# data_to_js['PythonToJs']['result'] = '0'
# data_to_js['PythonToJs']['desc'] = '错误传值成功'

# data_to_py = {}
# data_to_py['ClientToPython'] = {}
# data_to_py['ClientToPython']['LoginInit'] = {}
# data_to_py['ClientToPython']['LoginInit']['Account'] = 'zhanghu'
# data_to_py['ClientToPython']['LoginInit']['CompID'] = 'comid'

# PythonToJs = {}
# PythonToJs['result'] = '0'
# PythonToJs['desc'] = '错误传值成功'
# aa = '{"JsToPython": {"type": "isLogin", "channel": 1}}'

# js_to_py = '123456'
# js_to_py = '10000'
js_to_py = {}
js_to_py['JsToPython'] = {}
js_to_py['JsToPython']['orgId'] = '1233211234567'
# js_to_py['JsToPython'] = {"JsToPython":{"json":{"id":"8b163f6157bd4d24b27c96716bd45219","jobId":"d069f8b55d184763801689bea12362e0","channel":1,"keyWord":"客服","keyWordRule":1,"nearCompany":"中国","place":["海南"],"expectPlaceRule":0,"job":["电子/电器/半导体/仪器仪表 -仪器/仪表/计量工程师 ","医院/医疗/护理 "],"latelyJob":1,"expectPlace":["河北-邯郸","澳门","台湾省"],"workLimit":["4年","20年"],"overseas":1,"expectPay":"35000-50000元/月","industry":["计算机软件","通信/电信运营、增值服务","IT服务(系统/数据/维护)"],"latelyIndustry":1,"language":"法语","workStatus":"不限","dateUpdated":"最近六个月","education":["高中","本科"],"sex":"女","age":["23","60"]},"type":"channel_upgrade","channel":1,"timestamp":1521796852268}}
# js_to_py['JsToPython']['json'] = {
# 	  # "id" : "111",
# 	  # "id" : "f642710cfb444269b8a03ce6413e2a66",
#       "sex" : "男",
#      "jobId" :"f5991fb736b64a4986e5624657cedaa6",
# }
# js_to_py['JsToPython']['type'] = 'channel_upgrade'
# js_to_py['JsToPython']['timestamp'] = 225656565
# # js_to_py['JsToPython']['channel'] = 2
# js_to_py['JsToPython']['channel'] = 1
# js_to_py['JsToPython']['jobId'] = '54545454'

# 客户端根据ID下载简历前询问
js_to_py['JsToPython']['type'] = 'download_confrim'
js_to_py['JsToPython']['timestamp'] = 225656565
# # # js_to_py['JsToPython']['resumeId'] = 'T9379L8LyZMF(mfYcxSq)Q'  # 无对应简历
# js_to_py['JsToPython']['resumeId'] = '3_nerpnGOsneHQTEmaTGr5lEDkTen5Tvm5nGUknpsfnGOYnGONMGOunu5f_e0knGrsnEralEyunGrX'
js_to_py['JsToPython']['resumeId'] = 'dAvb(9l(m(Z)BhtyLagopA'
js_to_py['JsToPython']['channelId'] = 1

# 客户端根据ID下载简历
# js_to_py['JsToPython']['type'] = 'download_resume'
# js_to_py['JsToPython']['payType'] = 1
# js_to_py['JsToPython']['timestamp'] = 225656565
# js_to_py['JsToPython']['resumeId'] = 'UqcfVXxcpdw7P1ZJLKxLJQ'
# js_to_py['JsToPython']['channelId'] = 1
# 获取点数T9379L8LyZMF(mfYcxSq)Q
# js_to_py['JsToPython']['type'] = 'job_channel_pointer'
# js_to_py['JsToPython']['channels'] = [1, 2,3]
# js_to_py['JsToPython']['timestamp'] = 225656565
# 是否登录
# js_to_py['JsToPython']['type'] = 'isLogin_auto'
# js_to_py['JsToPython']['timestamp'] = 225656565
# js_to_py['JsToPython']['channels'] = [i for i in range(1,20,1)]
# 刷新职位
# js_to_py['JsToPython']['type'] = 'batch_job_sync'
# js_to_py['JsToPython']['timestamp'] = 225656565
# js_to_py['JsToPython']['Jobids'] = [{'channelId': '1', 'ids': ['CC358286719J00145731008']}]
# # 简历抓取
# js_to_py['JsToPython']['type'] = 'crawl_url'
# js_to_py['JsToPython']['timestamp'] = 225656565
# # js_to_py['JsToPython']['url'] = 'https://ihr.zhaopin.com/resume/details/?access_token=9f62f8c597c7486a92e1a1c486d6deb8&resumeNo=510439195408_CC358286719J90250488000_P0mIc%29Vk%28ZkF%28mfYcxSq%29Q_1_1&resumeSource=3&version=3&openFrom=4&haveEnglish='
# js_to_py['JsToPython']['url'] = 'https://rd5.zhaopin.com/resume/detail?resumeNo=511742019408_1_1&openFrom=4'
# js_to_py['JsToPython']['id'] = '589438358'
# 同步职位
# js_to_py['JsToPython']['timestamp'] = 225656565
# js_to_py['JsToPython']['type'] = 'job_sync_all'
# 检测浏览器
# js_to_py['JsToPython']['type'] = 'jcllq'
# 保存简历给吴
# js_to_py['JsToPython']['timestamp'] = 225656565
# js_to_py['JsToPython']['type'] = 'crawl_save'
# js_to_py['JsToPython']['userInfo'] = {}
# js_to_py['JsToPython']['position'] = ''
# js_to_py = {}
# js_to_py['messageContent'] = "系统检测到您邮箱有来自杭州人才网的简历，请您先登录杭州人才网正常获取简历"
# js_to_py['orgId'] = "123456"

# xx = 'http://192.168.1.115:8080/crawler/resume/addSystemMessage'
# xx = 'http://192.168.1.9:9021/crawler/resume/addSystemMessage'
data = json.dumps(js_to_py)
data = data.encode('utf-8')
print(data)
resp_page = requests.post(url='http://192.168.1.133:6000/?_t=12222222222&account=33333333', data=data)
# 查看最终发出去的url
print('11111', resp_page.url)
# 修改返回值的编码
resp_page.encoding = 'utf-8'
print(22222, resp_page.text)
print('状态码：', resp_page)


#====================================================================================================================

