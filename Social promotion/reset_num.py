# -*- coding: utf-8 -*- 
# @Author : Zhy

'''每天重置一次数据库，将当日账号爬取数量置为0'''

from setting import *
import pymysql
import traceback
import time

def select_crawelNum(username,channelType):
    '''查询指定账号当日爬取数量'''
    while True:
        try:
            conn = pymysql.connect(host=MYSQL_HOST, port=PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD,
                                   db=MYSQL_DB,
                                   charset='utf8')
            cursor = conn.cursor()
            break
        except:
            time.sleep(3)
    try:
        '''查询当前数量'''
        sql_select = "select crawelNum from cookie_pool where username='{}' and channelType='{}'".format(username,channelType)
        conn.ping(reconnect=True)
        cursor.execute(sql_select)
        crawel_num = cursor.fetchall()
        crawel_num = crawel_num[0][0]
        return crawel_num
    except:
        pass
def update_crawelNum(username,channelType):
    '''更新数据库中对应账号的当日爬取数量，返回当前已累计数量，满200后不再添加'''

    while True:
        try:
            conn = pymysql.connect(host=MYSQL_HOST, port=PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD,
                                   db=MYSQL_DB,
                                   charset='utf8')
            cursor = conn.cursor()
            break
        except:
            time.sleep(3)
    try:
        '''查询当前数量'''
        sql_select = "select crawelNum from cookie_pool where username='{}' and channelType='{}'".format(username,channelType)
        conn.ping(reconnect=True)
        cursor.execute(sql_select)
        crawel_num = cursor.fetchall()
        crawel_num = crawel_num[0][0]

        if crawel_num >=40:
            return 40
        else:
            '''更新数据库'''
            sql_update = "update cookie_pool set crawelNum='{}' where username='{}'and channelType='{}'".format(crawel_num+1,username, channelType)
            conn.ping(reconnect=True)
            cursor.execute(sql_update)
            conn.commit()
            
            return crawel_num+1
    except:
        pass

if __name__ == '__main__':

    while True:
        now_time = int(time.strftime("%H%M%S"))
        if now_time > 220000 and now_time < 220200:
            while True:
                try:
                    conn = pymysql.connect(host=MYSQL_HOST, port=PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD,
                                           db=MYSQL_DB,
                                           charset='utf8')
                    cursor = conn.cursor()
                    break
                except:
                    traceback.print_exc()
                    time.sleep(3)

            '''查询成功，更新cookie'''
            sql_update = "update cookie_pool set crawelNum='{}' ".format(0)
            conn.ping(reconnect=True)
            cursor.execute(sql_update)
            conn.commit()
            print('{}:更新crawelNum成功'.format(now_time))

        time.sleep(30)








