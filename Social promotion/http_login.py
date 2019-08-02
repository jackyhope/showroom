# -*- coding: utf-8 -*- 
# @Author : Zhy
import time
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import traceback
import base64
import pymysql
import requests
from xq_project.func_xq import xq_login,qx_test_cookie
from wb_project.account_handler import CookiePool
from setting import *
from xq_project.Logger import Log

log = Log('login')

dict_hyx = {}
url_channel=URL_CHANNEL
dict_cookie_state={}

def  write_cookie(datas):
    while True:
        try:
            conn = pymysql.connect(host=MYSQL_HOST, port=PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD,
                                   db=MYSQL_DB,
                                   charset='utf8',connect_timeout=5)
            cursor = conn.cursor()
            print(1)
            break
        except:
            traceback.print_exc()
            time.sleep(3)

    username=datas['accinfo']['channelAcc']
    password=datas['accinfo']['password']

    cookie=datas['accinfo']['cookies']
    channelType=datas['accinfo']['type']
    '''先查询，没有再插入'''
    try:
        sql_select = "select cookie from cookie_pool where username='{}' and channelType='{}'".format(username,channelType)
        conn.ping(reconnect=True)
        cur_cookie = cursor.execute(sql_select)
        cur_cookie = cursor.fetchall()
        cookie_old = cur_cookie[0][0]

        '''查询成功，更新cookie'''
        sql_update = "update cookie_pool set cookie='{}' where username='{}'and channelType='{}'".format(cookie,username,channelType)
        conn.ping(reconnect=True)
        cursor.execute(sql_update)
        conn.commit()
        print('更新{}：cookie成功'.format(username))
        log.logger.info('更新{}：cookie成功'.format(username))

    except:

        sql_insert = "insert into cookie_pool(username, password,cookie, channelType, code) values(%s,%s,%s,%s,%s)"
        insert_info = (str(username), str(password), str(cookie), int(channelType), 1)
        print('插入', insert_info)
        conn.ping(reconnect=True)
        cursor.execute(sql_insert, insert_info)
        conn.commit()
    try:
        cursor.close()
        conn.close()
    except:
        pass
    if channelType == 2:
        '''微博登录'''
        try:
            with CookiePool() as cookie_pool:
                result = cookie_pool.add_account(datas['accinfo']['channelAcc'], datas['accinfo']['id'],
                                                      datas['accinfo']['orgId'], datas['accinfo']['type'])
            if result:
                print('微博账号:{}登录成功'.format(datas['accinfo']['channelAcc']))
                log.logger.info('微博账号:{}登录成功'.format(datas['accinfo']['channelAcc']))

            else:
                data_1 = {'accinfo': datas['accinfo'], 'act': 'cookie_notuse', }
                # data_1 = {'channelAcc': datas['accinfo']['channelAcc'], 'type': datas['accinfo']['type'],
                #           'act': 'cookie_notuse', 'ownerAcc': datas['accinfo']['ownerAcc']}
                ownerAcc = datas['accinfo']['ownerAcc']
                dict_cookie_state[ownerAcc] = data_1
                # data_1 = json.dumps({'channelAcc':datas['accinfo']['taskAcc'],'type':datas['accinfo']['channelType'],'act':'cookie_notuse','ownerAcc':datas['accinfo']['ownerAcc']})
                # data_1 = data_1.encode('utf-8')
                # a = requests.post(url=URL_LOGIN, data=data_1).text
                print('微博账号:{}登录失败'.format(datas['accinfo']['channelAcc']))
                log.logger.info('微博账号:{}登录失败'.format(datas['accinfo']['channelAcc']))
        except:
            traceback.print_exc()
    elif channelType == 3:
        '''雪球登录'''
        try:
            state=qx_test_cookie(cookie,datas['accinfo'])
            if state == '该账号登录状态有效':
                dict_login = xq_login(cookie)
                data_acc_xq = {'id': datas['accinfo']['id'],
                               'orgId': datas['accinfo']['orgId'],
                               'headUrl': dict_login['headUrl'],  # 账号头像
                               'focusNum': dict_login['focusNum'],  # 关注人数
                               'status': 0,  # 账号状态，0正常，1异常
                               'nickname': dict_login['nickname'],
                               'errorDescription': '登录成功'  # 异常信息
                               }
                print(data_acc_xq)
                data_acc_xq = json.dumps(data_acc_xq)
                data_acc_xq = data_acc_xq.encode('utf-8')
                print('雪球账号:{}登录成功'.format(datas['accinfo']['channelAcc']))
                log.logger.info('雪球账号:{}登录成功'.format(datas['accinfo']['channelAcc']))
                pass
            elif state == '该账号登录状态失效':
                '''客户端弹框通知'''
                data_1 = {'accinfo': datas['accinfo'], 'act': 'cookie_notuse', }
                # data_1={'channelAcc': datas['accinfo']['channelAcc'], 'type': datas['accinfo']['type'],'act': 'cookie_notuse', 'ownerAcc': datas['accinfo']['ownerAcc']}
                ownerAcc = datas['accinfo']['ownerAcc']
                dict_cookie_state[ownerAcc] = data_1

                data_acc_xq = {'id': datas['accinfo']['id'],
                               'orgId': datas['accinfo']['orgId'],
                               'headUrl': '',  # 账号头像
                               'focusNum': '',  # 关注人数
                               'status': 1,  # 账号状态，0正常，1异常
                               'nickname': '',
                               'errorDescription': '登录失败'  # 异常信息
                               }
                data_acc_xq = json.dumps(data_acc_xq)
                data_acc_xq = data_acc_xq.encode('utf-8')
                print('雪球账号:{}登录失败'.format(datas['accinfo']['channelAcc']))
                log.logger.info('雪球账号:{}登录失败'.format(datas['accinfo']['channelAcc']))

        except:
            log.logger.exception("Exception Logged")
            pass

        try:
            state_acc_xq = requests.post(url=url_channel, data=data_acc_xq,
                                         headers={'Content-type': 'application/json'}).text
            print('提交账号登录状态：{}'.format(state_acc_xq))
        except:
            log.logger.exception("Exception Logged")
            pass

    elif channelType == 1:
        '''抖音'''
        data_acc_dy = {'id': datas['accinfo']['id'],
                       'orgId': datas['accinfo']['orgId'],
                       'headUrl': '',  # 账号头像
                       'focusNum': 20,  # 关注人数
                       'status': 0,  # 账号状态，0正常，1异常
                       'nickname': "抖音测试账号",
                       'errorDescription': ''  # 异常信息
                       }
        data_acc_dy = json.dumps(data_acc_dy)
        data_acc_dy = data_acc_dy.encode('utf-8')
        try:
            state_acc_dy = requests.post(url=url_channel, data=data_acc_dy,
                                         headers={'Content-type': 'application/json'}).text
            print(state_acc_dy)
        except:
            pass
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        # self.send_response(200, message=None)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

        datas = self.rfile.read(int(self.headers['content-length']))
        datas=datas.decode('utf-8', errors='ignore')
        datas=json.loads(datas)
        print(datas)
        if datas['act'] == 'channelLogin':
            ownerAcc=datas['ownerAcc']
            dict_hyx[ownerAcc]=datas
        elif datas['act'] == 'login_stat':
            ownerAcc = datas['account_hyx']
            if ownerAcc in dict_hyx.keys():
                return_data = {'code': 0, 'desc': '','accinfo':dict_hyx[ownerAcc]}
                print(return_data)
                print('获取cookie')
                log.logger.info('获取cookie')

                dict_hyx.pop(ownerAcc)
            elif ownerAcc in dict_cookie_state.keys():
                task=dict_cookie_state[ownerAcc]
                log.logger.info(task)
                task['accinfo']['cookies']=''
                try:
                    task_1 = {}
                    task_1['type'] = task['accinfo']['channelType']
                    task_1['channelAcc'] = task['accinfo']['taskAcc']
                    task_1['password'] = task['accinfo']['password']
                    task_1['cookies'] = ''
                    task_1['id'] = task['accinfo']['accountId']
                    task_1['orgId'] = task['accinfo']['orgId']
                    task_1['act'] = 'channelLogin'
                    task_1['ownerAcc'] = task['accinfo']['ownerAcc']
                    return_data = {'code': 3, 'desc': '', 'accinfo': task_1}

                except:
                    return_data = {'code': 3, 'desc': '', 'accinfo': task['accinfo']}

                print(return_data)
                print('cookie失效提醒')
                log.logger.info(return_data)
                log.logger.info('cookie失效提醒')
                dict_cookie_state.pop(ownerAcc)

            else:
                return_data= {'code':1,'desc':'无账户需要登录'}
            try:
                return_data=json.dumps(return_data)
                res = bytes('{}'.format(return_data), 'utf-8')
                res = base64.b64encode(res)
                self.wfile.write(res)

            except:
                traceback.print_exc()
                pass
        elif datas['act'] == 'login_resp':
            write_cookie(datas)
            print('cookie已写入：{}'.format(datas))
        elif datas['act'] == 'cookie_notuse':
            ownerAcc = datas['accinfo']['ownerAcc']
            dict_cookie_state[ownerAcc]=datas

    def do_OPTIONS(self):
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS, POST')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run():

    server_address = (IP,LOGIN_POST)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
