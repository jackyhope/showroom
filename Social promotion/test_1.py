# -*- coding: utf-8 -*- 
# @Author : Zhy

import base64
import requests
from setting import *
import json


# task_2 = '{"isOperate":0,"act":"taskOperate","taskList":[{"isOpen":0,"endDate":"","contentId":"8ca9857fc47346c79191f19f6fd56c09","headUrl":"","inputTime":{"date":1,"hours":14,"seconds":58,"month":3,"timezoneOffset":-480,"year":119,"minutes":57,"time":1554101878000,"day":1},"channelType":3,"todayCount":0,"groupKey":"","limitKey":"","orgId":"rd","imageUrl":"","nickname":"","inputAcc":"rd001","groupClass":"","id":"9a114875e2dd46b2805dbc66f56d9f0e","text":"","orderKey":"","taskAcc":"aaas","updateAcc":"","updateTime":null,"focusNum":0,"ownerAcc":"rd001","generalizeType":1,"isDel":0,"startDate":""},{"isOpen":0,"endDate":"","contentId":"196c8fabe2d54d63a3c05a1265fd3e4a","headUrl":"","inputTime":{"date":2,"hours":11,"seconds":8,"month":3,"timezoneOffset":-480,"year":119,"minutes":21,"time":1554175268000,"day":2},"channelType":3,"todayCount":0,"groupKey":"","limitKey":"","orgId":"rd","imageUrl":"","nickname":"","inputAcc":"rd001","groupClass":"","id":"e2a0c7b9428f43f6888627a919d61f07","text":"","orderKey":"","taskAcc":"13018956681","updateAcc":"","updateTime":null,"focusNum":0,"ownerAcc":"rd001","generalizeType":1,"isDel":0,"startDate":""}],"orgId":"rd","boxId":"2000"}'

task_2={'startDate': '', 'channelType': 3, 'accountId': 'ab96ac5d24eb41babcf38b770d794d31', 'updateAcc': '', 'imageUrl': '', 'focusNum': 0, 'endDate': '', 'password': 'zhy200817436', 'contentId': 'aaba011b9d9f43c297fd1dd6b5153673', 'id': '1689ffc7f7c14acabb58d1328acf00f6', 'orgId': 'qfzn', 'todayCount': 0, 'ownerAcc': 'qfzn002', 'groupClass': '', 'isDel': 0, 'headUrl': '', 'inputAcc': 'qfzn002', 'text': '哈哈哈', 'limitKey': '', 'updateTime': None, 'nickname': '', 'taskAcc': '13018956681', 'inputTime': {'time': 1556102409000, 'minutes': 40, 'seconds': 9, 'hours': 18, 'month': 3, 'year': 119, 'timezoneOffset': -480, 'day': 3, 'date': 24}, 'isOpen': 0, 'groupKey': '', 'orderKey': '', 'generalizeType': 1}


task_xqgz={'orgId': 'qfzn', 'boxId': '3001', 'taskList': [{'startDate': '', 'channelType': 3, 'accountId': '', 'updateAcc': '', 'imageUrl': '', 'focusNum': 0, 'endDate': '', 'password': '', 'contentId': 'aaba011b9d9f43c297fd1dd6b5153673', 'id': '1689ffc7f7c14acabb58d1328acf00f6', 'orgId': 'qfzn', 'todayCount': 0, 'ownerAcc': 'qfzn002', 'groupClass': '', 'isDel': 0, 'headUrl': '', 'inputAcc': 'qfzn002', 'text': '哈哈哈', 'limitKey': '', 'updateTime': None, 'nickname': '', 'taskAcc': '13018956681', 'inputTime': {'time': 1556102409000, 'minutes': 40, 'seconds': 9, 'hours': 18, 'month': 3, 'year': 119, 'timezoneOffset': -480, 'day': 3, 'date': 24}, 'isOpen': 0, 'groupKey': '', 'orderKey': '', 'generalizeType': 1}], 'act': 'taskOperate', 'isOperate': 0}
task_login = {"act": "channelLogin","id": "gradfffgWQQdfdfsgvbtdf","orgId": "rd","channelAcc": "13018956681","password": "kaopza743","type": 2,"ownerAcc": "333333"}
task_xqfl={'orgId': 'qfzn', 'boxId': '3000', 'taskList': [{'startDate': '', 'channelType': 3, 'accountId': 'ab96ac5d24eb41babcf38b770d794d31', 'updateAcc': '', 'imageUrl': '', 'focusNum': 0, 'endDate': '', 'password': 'zhy200817436', 'contentId': 'aaba011b9d9f43c297fd1dd6b5153673', 'id': '9b4790bc332940d6997cfec2438a93b3', 'orgId': 'qfzn', 'todayCount': 0, 'ownerAcc': 'qfzn002', 'groupClass': '3063,2003', 'isDel': 0, 'headUrl': '', 'inputAcc': 'qfzn002', 'text': '哈哈哈', 'limitKey': '', 'updateTime': None, 'nickname': '', 'taskAcc': '13018956681', 'inputTime': {'time': 1556158401000, 'minutes': 13, 'seconds': 21, 'hours': 10, 'month': 3, 'year': 119, 'timezoneOffset': -480, 'day': 4, 'date': 25}, 'isOpen': 0, 'groupKey': '', 'orderKey': '', 'generalizeType': 0}], 'act': 'taskOperate', 'isOperate': 0}




url = 'http://192.168.1.168:8866'    # 主服务接口
url_1 = URL_CODE_TABLE     # 码表接口

task_2=json.dumps(task_xqfl)
res = task_2.encode('utf-8')
# res = bytes('{}'.format(task_2), 'utf-8')
res = base64.b64encode(res)

b = requests.post(url=url, data=res).text
b = base64.b64decode(b)
b = b.decode('utf-8', errors='ignore')
print(b)




