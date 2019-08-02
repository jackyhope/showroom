# -*- coding: utf-8 -*- 
# @Author : Zhy

import threading
import redis
import random
import requests
import traceback
import json
import time
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from multiprocessing import Queue
from  setting import *
from xq_project.Logger import Log
from xq_project.func_xq import xq_classify,xq_attention
from wb_project.account_handler import CookiePool
from wb_project.generalize_mode import RecommendedContentGeneralize, RecommendedBloggerGeneralize, FollowersGeneralize

log = Log('server')
myqueue_main = Queue()

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

def reset_redis():
    dict_pid = r.hgetall('thread:pid')

    for task_id, state in dict_pid.items():
        try:
            r.hdel('thread:pid', task_id)
        except:
            traceback.print_exc()
            pass

    dict_pid = r.hgetall('thread:pid')

    return dict_pid

def time_manage():
    '''时间控制，22:00-9:00期间不接收评论任务'''
    while True:
        now_time=int(time.strftime("%H%M%S"))
        if now_time > 220000 or now_time < 90000:
            print('限制时间')
            dict_pid = r.hgetall('thread:pid')
            print(dict_pid)
            for task_id,state in dict_pid.items():
                try:
                    if int(state) == 1:
                        r.hset('thread:pid', task_id, 0)
                        print('终止任务：{}成功'.format(task_id))
                    else:
                        print('没有此任务!!!')
                except:
                    traceback.print_exc()
                    pass

        if now_time > 80000 and now_time < 80200:
            print(reset_redis())

        time.sleep(30)
def wb_hot(data,task):

    with CookiePool() as cookie_pool:
        account = cookie_pool.select_account(task['taskAcc'], task['accountId'], data['orgId'], 2)
    if account:
        generalize = RecommendedContentGeneralize(account.cookies, account.uid, data['orgId'], task['ownerAcc'], task['taskAcc'], task['id'], task['text'], task)
        generalize.run(task['groupClass'].split(','))
    else:
        # data_1 = json.dumps({'channelAcc':task['taskAcc'],'type':task['channelType'],'act':'cookie_notuse','ownerAcc':task['ownerAcc']})
        data_1 = json.dumps({'accinfo':task,'act':'cookie_notuse',})
        data_1 = data_1.encode('utf-8')
        a = requests.post(url=URL_LOGIN, data=data_1).text
def wb_classify(data,task):
    with CookiePool() as cookie_pool:
        account = cookie_pool.select_account(task['taskAcc'], task['accountId'], data['orgId'], 2)
    if account:
        generalize = RecommendedBloggerGeneralize(account.cookies, account.uid, data['orgId'], task['ownerAcc'], task['taskAcc'], task['id'], task['text'], task)
        generalize.run(task['groupClass'].split(','))
    else:
        # data_1 = json.dumps({'channelAcc':task['taskAcc'],'type':task['channelType'],'act':'cookie_notuse','ownerAcc':task['ownerAcc']})
        data_1 = json.dumps({'accinfo':task,'act':'cookie_notuse',})

        data_1 = data_1.encode('utf-8')
        a = requests.post(url=URL_LOGIN, data=data_1).text
def wb_attention(data,task):
    with CookiePool() as cookie_pool:
        account = cookie_pool.select_account(task['taskAcc'], task['accountId'], data['orgId'], 2)
    if account:
        generalize = FollowersGeneralize(account.cookies, account.uid, data['orgId'], task['ownerAcc'], task['taskAcc'], task['id'], task['text'], task)
        generalize.run()
    else:
        # data_1 = json.dumps({'channelAcc':task['taskAcc'],'type':task['channelType'],'act':'cookie_notuse','ownerAcc':task['ownerAcc']})
        data_1 = json.dumps({'accinfo':task,'act':'cookie_notuse',})
        data_1 = data_1.encode('utf-8')
        a = requests.post(url=URL_LOGIN, data=data_1).text
def get_comment(data_task):
    task_id = data_task['taskList']['id']
    r.hset('thread:pid', task_id, 1)
    print('开启任务：{}'.format(task_id))
    print('总线程数：{}'.format(threading.activeCount()))

    box_id=data_task['boxId']
    if box_id == '3001':
        try:
            print('雪球关注任务启动')
            log.logger.info('雪球关注任务启动：{}'.format(task_id))
            xq_attention(data=data_task,task=data_task['taskList'])     #雪球关注

        except:
            traceback.print_exc()
            pass
    elif box_id == '3002' or box_id == '3000':
        try:
            print('雪球分类任务启动')
            log.logger.info('雪球分类任务启动：{}'.format(task_id))
            xq_classify(data=data_task,task=data_task['taskList'])      #雪球分类

        except:
            traceback.print_exc()
            pass
    elif box_id == '2000':
        try:
            print('微博热门任务启动')
            log.logger.info('微博热门任务启动：{}'.format(task_id))
            wb_hot(data=data_task,task=data_task['taskList'])           #微博热门

        except:
            traceback.print_exc()
            pass
    elif box_id == '2001':
        try:
            print('微博关注任务启动')
            log.logger.info('微博关注任务启动：{}'.format(task_id))
            wb_attention(data=data_task,task=data_task['taskList'])     #微博关注

        except:
            traceback.print_exc()
            pass
    elif box_id == '2002':
        try:
            print('微博博主分类任务启动')
            log.logger.info('微博博主分类任务启动：{}'.format(task_id))
            wb_classify(data=data_task,task=data_task['taskList'])     #微博博主分类

        except:
            traceback.print_exc()
            pass
    task_id=data_task['taskList']['id']
    r.hdel('thread:pid', task_id)
    print('已删除任务：{}'.format(task_id))
    log.logger.info('删除任务：{}'.format(task_id))
def deal_task(newdata):
    '''接收指令'''
    try:
        act_type = newdata['act']
        if act_type == 'channelLogin':
            '''新增账号'''
            log.logger.info('新增账号任务：{}'.format(newdata))
            data_1 = json.dumps(newdata)
            data_1 = data_1.encode('utf-8')
            a = requests.post(url=URL_LOGIN, data=data_1).text
        elif act_type == 'taskOperate':
            try:
                if newdata['isOperate'] == 0:
                    for task in newdata['taskList']:
                        if task['isOpen'] == 0:
                            '''判断任务是否已存在'''
                            if r.hexists('thread:pid', task['id']):
                                a = r.hmget('thread:pid', task['id'])
                                if int(a[0]) == 1:
                                    '''存在且处于开启的状态'''
                                    log.logger.info('该任务：{}当前正在执行中'.format(task['id']))
                                    print('该任务：{}当前正在执行中'.format(task['id']))
                                    pass
                                elif int(a[0]) == 0:
                                    '''存在且处于关闭的状态'''
                                    r.hset('thread:pid', task['id'], 1)
                                    print('该任务：{}已重新开启'.format(task['id']))
                                    log.logger.info('该任务：{}已重新开启'.format(task['id']))
                            else:
                                '''任务不存在，添加单任务'''
                                log.logger.info('开启新任务指令：{}'.format(task))
                                newdata['taskList'] = task
                                myqueue_main.put(newdata)
                                print(task)
                        elif task['isOpen'] == 1:
                            if r.hexists('thread:pid', task['id']):
                                a = r.hmget('thread:pid', task['id'])
                                if int(a[0]) == 1:
                                    '''存在且处于开启的状态'''
                                    r.hset('thread:pid', task['id'], 0)
                                    print('该任务：{}关闭成功'.format(task['id']))
                                    log.logger.info('该任务：{}关闭成功'.format(task['id']))
                                else:
                                    '''存在且处于关闭的状态'''
                                    print('该任务：{}当前已处于关闭状态'.format(task['id']))
                                    log.logger.info('该任务：{}当前已处于关闭状态'.format(task['id']))
                elif newdata['isOperate'] == 1:
                    log.logger.info('终止模块任务指令：{}'.format(newdata))
                    for task in newdata['taskList']:
                        '''终止模块任务'''
                        if r.hexists('thread:pid', task['id']):
                            a = r.hmget('thread:pid', task['id'])
                            if int(a[0]) == 1:
                                '''存在且处于开启的状态'''
                                r.hset('thread:pid', task['id'], 0)
                                print('该任务：{}关闭成功'.format(task['id']))
                                log.logger.info('该任务：{}关闭成功'.format(task['id']))
                            else:
                                '''存在且处于关闭的状态'''
                                print('该任务：{}当前已处于关闭状态'.format(task['id']))
                                log.logger.info('该任务：{}当前已处于关闭状态'.format(task['id']))
                        else:
                            print('该任务：{}当前不存在'.format(task['id']))
                            log.logger.info('该任务：{}当前不存在'.format(task['id']))
            except:
                log.logger.exception("Exception Logged")
                pass
        '''开启队列内所有的任务'''

        while not myqueue_main.empty():
            if threading.activeCount() < 600:
                th_1 = threading.Thread(target=get_comment, args=(myqueue_main.get(),))
                th_1.start()
                time.sleep(random.uniform(2,4))
    except:
        traceback.print_exc()
        pass


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        self.send_response(200, message=None)
        # self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            datas = self.rfile.read(int(self.headers['content-length']))
            return_data={'code':0,'desc':''}
            res = bytes('{}'.format(return_data), 'utf-8')
            res=base64.b64encode(res)
            self.wfile.write(res)
            # self.wfile.write(json.dumps({'code':0,'desc':''}).encode())  # 请求返回内容
        except:
            traceback.print_exc()
            return_data = {'code':1,'desc':'指令接收失败'}
            res = bytes('{}'.format(return_data), 'utf-8')
            res = base64.b64encode(res)
            self.wfile.write(res)

        try:
            newdata=base64.b64decode(datas)
            newdata=newdata.decode('utf-8',errors='ignore')
            newdata = json.loads(newdata)

        except:
            traceback.print_exc()
        print(newdata)

        th_1 = threading.Thread(target=deal_task, args=(newdata,))
        th_1.start()

def run():
    th_2 = threading.Thread(target=time_manage)
    th_2.start()
    server_address = (IP,SERVER_POST)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    print(reset_redis())
    run()
    pass