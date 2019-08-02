# -*- coding: utf-8 -*- 
# @Author : Zhy
from http.server import BaseHTTPRequestHandler, HTTPServer
import pymysql
import time
import json
import traceback
import base64
from setting import *



def  get_code_table():
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
    dict_code={}
    sql_select_company = 'select * from category '
    conn.ping(reconnect=True)
    code_table = cursor.execute(sql_select_company)
    code_table = cursor.fetchall()

    wb_rm=code_table[0][0]
    wb_bloggers=code_table[0][1]

    xq_rm=code_table[0][2]
    xq_bloggers=code_table[0][3]

    dict_code['wb_rm']=eval(wb_rm)
    dict_code['wb_bloggers']=eval(wb_bloggers)
    dict_code['xq_rm']=eval(xq_rm)
    dict_code['xq_bloggers']=eval(xq_bloggers)
    try:
        cursor.close()
        conn.close()
    except:
        pass

    return dict_code

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):

        self.send_response(200, message=None)
        self.end_headers()

        try:
            # datas = self.rfile.read(int(self.headers['content-length']))
            data_code=get_code_table()
            print(data_code)
            res = {'code': 0, 'desc': '', 'map': data_code}
            res = bytes('{}'.format(res), 'utf-8')

            res=base64.b64encode(res)
            self.wfile.write(res)
        except:
            traceback.print_exc()
            return_data = {'code':0,'desc':'指令接收失败','map': data_code}
            res = json.dumps(return_data)
            res = base64.b64encode(res.encode('utf-8',errors='ignore'))
            self.wfile.write(res)

def run():
    server_address = (IP,CODE_TABLE_POST)
    httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run()