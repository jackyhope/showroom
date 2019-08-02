import logging
import logging.handlers
import concurrent_log_handler




class Log(object):
    def __init__(self, name, mail=False):
        self.logger = logging.getLogger(name)  # 设置一个日志器
        self.logger.setLevel(logging.INFO)

        formatter = logging.Formatter('%(asctime)s [%(name)s] %(levelname)s: %(message)s')

        file_handler = concurrent_log_handler.ConcurrentRotatingFileHandler(filename='xq_project/' + name + '_log', encoding='utf8')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


