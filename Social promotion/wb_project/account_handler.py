import re
import json
import pymysql
import time
from lxml import etree
from sqlalchemy import create_engine

from wb_project.request import Request
from wb_project.tools import Log, CookieConvert, PostData
from wb_project.settings import *

log = Log('account')


class CookiePool:
    mysql_engine = create_engine(MYSQL_KEY, pool_size=MYSQL_POOL_SIZE, pool_recycle=MYSQL_POOL_RECYCLE, pool_timeout=MYSQL_POOL_TIMEOUT, pool_pre_ping=True)

    def __init__(self):
        self.conn = self.mysql_engine.connect()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()

    def fetch(self, username, channelType):
        sql = 'select cookie from cookie_pool where username=%s and channelType=%s'
        cursor = self.conn.execute(sql, (username, channelType))
        result = cursor.fetchone()
        if result:
            return result[0]

    def add_account(self, username, accountId, orgId, channelType):
        cookies = self.fetch(username, channelType)
        if cookies:
            account = Account(username=username, cookies=cookies)
            if not hasattr(account, 'error_msg'):
                data = {
                    'id': accountId,
                    'orgId': orgId,
                    'headUrl': account.headUrl,
                    'focusNum': int(account.focusNum),
                    'status': 0,
                    'nickname': account.nickname
                }
                PostData.channel_info(data)
                log.logger.info('账号添加成功: {}'.format(str((username, data))))
                return True
            else:
                data = {
                    'id': accountId,
                    'orgId': orgId,
                    'status': 1,
                    'errorDescription': account.error_msg
                }
                PostData.channel_info(data)
                log.logger.warning('账号异常: {}'.format(str((username, data))))
                return

    def select_account(self, username, accountId, orgId, channelType):
        cookies = self.fetch(username, channelType)
        if cookies:
            account = Account(username=username, cookies=cookies)
            if not hasattr(account, 'error_msg'):
                return account
            else:
                data = {
                    'id': accountId,
                    'orgId': orgId,
                    'status': 1,
                    'errorDescription': account.error_msg
                }
                PostData.channel_info(data)
                log.logger.warning('账号异常: {}'.format(str((username, data))))
                return


class Account:
    def __init__(self, username, cookies):
        self.username = username
        self.cookies = CookieConvert.str_to_jar(cookies)
        self.req = Request(self.cookies, log)
        try:
            self.uid = re.search('uid%3D(.*?)%26', cookies).group(1)
        except:
            log.logger.warning('uid获取失败：{}'.format(username))
            self.uid = ''
        try:
            self.nickname, self.headUrl, self.focusNum = self.get_info()
        except:
            self.error_msg = '登录状态失效'

    def get_info(self):
        url = 'https://weibo.com/{}/profile?is_all=1'.format(self.uid)
        response = self.req.get(url=url)
        nick = re.search("\$CONFIG\['nick'\]='(.*?)';", response.text).group(1)
        avatar_large = re.search("\$CONFIG\['avatar_large'\]='(.*?)';", response.text).group(1)
        match = re.search(r'<script>FM\.view\(({.*?"domid":"Pl_Core_T8CustomTriColumn__3".*})\)</script>', response.text).group(1)
        html = json.loads(match).get('html')
        element = etree.HTML(html)
        focus_num = element.xpath('//table[@class="tb_counter"]/tbody/tr[1]/td[1]/a[1]/strong[@class="W_f18"]/text()')[0]
        return nick, 'https:' + avatar_large, int(focus_num)
