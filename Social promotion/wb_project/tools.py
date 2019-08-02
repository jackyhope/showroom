import requests
import logging
import logging.handlers
import concurrent_log_handler
import json
from setting import URL_GENTER, URL_RESULT, URL_CHANNEL


def emit(self, record):
    """
    Emit a record.

    Format the record and send it to the specified addressees.
    """
    try:
        import smtplib
        from email.message import EmailMessage
        import email.utils

        port = self.mailport
        if not port:
            port = smtplib.SMTP_PORT
        smtp = smtplib.SMTP_SSL(self.mailhost, port, timeout=self.timeout)
        msg = EmailMessage()
        msg['From'] = self.fromaddr
        msg['To'] = ','.join(self.toaddrs)
        msg['Subject'] = self.getSubject(record)
        msg['Date'] = email.utils.localtime()
        msg.set_content(self.format(record))
        if self.username:
            smtp.ehlo()
            smtp.login(self.username, self.password)
        smtp.send_message(msg)
        smtp.quit()
    except Exception:
        self.handleError(record)


class Log(object):
    def __init__(self, name, mail=False):
        self.logger = logging.getLogger(name)  # 设置一个日志器
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

        file_handler = concurrent_log_handler.ConcurrentRotatingFileHandler(filename='wb_project/logging/' + name + '_log', maxBytes=3000000, encoding='utf8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # if mail:
        #     from_addr = '805071841@qq.com'
        #     password = 'nwqihodadverbedf'
        #     to_addr = ['805071841@qq.com']
        #     smtp_server = 'smtp.qq.com'
        #
        #     logging.handlers.SMTPHandler.emit = emit
        #     smtp_handler = logging.handlers.SMTPHandler((smtp_server, 465), from_addr, to_addr, "警告", credentials=(from_addr, password))
        #     smtp_handler.setLevel(logging.WARNING)
        #     smtp_handler.setFormatter(formatter)
        #     self.logger.addHandler(smtp_handler)

        # handler = logging.StreamHandler()
        # handler.setFormatter(formatter)
        # self.logger.addHandler(handler)


class CookieConvert(object):
    @staticmethod
    def str_to_jar(cookies):
        cookie_dict = {i.strip().split('=', 1)[0]: i.strip().split('=', 1)[1] for i in cookies.split(';') if '=' in i}
        # cookie_jar = requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)
        return cookie_dict

    @staticmethod
    def jar_to_str(cookiejar):
        cookie_dict = requests.utils.dict_from_cookiejar(cookiejar)
        cookies = '; '.join([key + '=' + value for key, value in cookie_dict.items()])
        return cookies


class PostData:
    @staticmethod
    def channel_info(data):
        data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        requests.post(url=URL_CHANNEL, data=data, headers={'Content-type': 'application/json'})

    @staticmethod
    def ask(data):
        data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        response = requests.post(url=URL_GENTER, data=data, headers={'Content-type': 'application/json'})
        if '"status":true' in response.text:
            return True

    @staticmethod
    def submit(data):
        data = json.dumps(data, ensure_ascii=False).encode('utf-8')
        requests.post(url=URL_RESULT, data=data, headers={'Content-type': 'application/json'})
