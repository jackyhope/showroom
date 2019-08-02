import time
import requests
from wb_project.settings import *


class Request(object):
    base_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    }

    def __init__(self, cookies, log):
        self.cookies = cookies
        self.proxies = self.get_fixed_proxies()
        self.log = log

    @staticmethod
    def get_dynamic_proxies():
        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": PROXY_HOST,
            "port": PROXY_PORT,
            "user": PROXY_USER,
            "pass": PROXY_PASS,
        }
        proxies = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        return proxies

    @staticmethod
    def get_fixed_proxies():
        proxies = {
            "http": 'http://47.96.71.176:3128',
            "https": 'http://47.96.71.176:3128',
        }
        return proxies

    def get(self, url, headers=None, params=None, retry_times=RETRY_TIMES):
        if headers:
            headers.update(self.base_headers)
        else:
            headers = self.base_headers
        while retry_times > 0:
            try:
                response = requests.get(url=url, headers=headers, params=params, cookies=self.cookies, proxies=self.proxies, timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    return response
                else:
                    self.log.logger.info('Crawled ({status_code}) <GET {url}>'.format(status_code=str(response.status_code), url=url))
            except Exception as e:
                self.log.logger.info(str(e))
            retry_times -= 1
            time.sleep(1)

        if retry_times == 0:
            raise ConnectionError

    def post(self, url, headers=None, data=None, retry_times=RETRY_TIMES):
        headers.update(self.base_headers)
        while retry_times > 0:
            try:
                response = requests.post(url=url, headers=headers, data=data, cookies=self.cookies, proxies=self.proxies, timeout=DOWNLOAD_TIMEOUT)
                if response.status_code == 200:
                    return response
                else:
                    self.log.logger.info('Crawled ({status_code}) <POST {url}>'.format(status_code=str(response.status_code), url=url))
            except Exception as e:
                self.log.logger.info(str(e))
            retry_times -= 1
            time.sleep(1)

        if retry_times == 0:
            raise ConnectionError
