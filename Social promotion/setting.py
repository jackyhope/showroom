# -*- coding: utf-8 -*- 
# @Author : Zhy
from urllib import request
import redis

#发给张建华
URL_GENTER='http://*******/thead/theadMsg/generalizable'       #内网,询问指定文章是否已评论过
URL_RESULT='http://*******/thead/theadMsg/generalizeResult'    #内网,提交评论结果
URL_CHANNEL='http://*******/thead/theadMsg/channelInfo'        #内网,提交账号状态


#服务地址及端口
# IP='*******'          #测试ip
IP='127.0.0.1'          #本地ip
SERVER_POST=9800



#数据库地址
MYSQL_HOST = '*******'
MYSQL_USER = 'test'
MYSQL_PASSWD = '*******'
MYSQL_DB = '*******'
PORT=3306


REDIS_HOST = '*******'
REDIS_PORT = 6379
REDIS_PASSWORD = '*******'
REDIS_KEY = 'thread:pid'



URL_SERVER = 'http://*******'       # 主服务接口
URL_CODE_TABLE= '*******'    # 码表接口
URL_LOGIN='*******'          # 登录接口