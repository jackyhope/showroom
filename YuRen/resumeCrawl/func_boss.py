import requests
from settings import *
from al_qf import *
import logging

py_ini_path = os.getcwd() + os.sep + 'Mod_Pyth' + os.sep + 'Py_Config.ini'
conf_ini = configparser.ConfigParser(strict=False, allow_no_value=True)
conf_ini.read(py_ini_path, encoding='utf-8')
try:
    API_URL = conf_ini.get("INIT_START", "API_URL")
    PLUGIN_LOGIN_URL = conf_ini.get("INIT_START", "PLUGIN_LOGIN_URL")
    RESUME_DOWNLOAD_URL = conf_ini.get("INIT_START", "RESUME_DOWNLOAD_URL")
    RESUME_CODES_URL = conf_ini.get("INIT_START", "RESUME_CODES_URL")
    RESUME_PLUGIN_URL = conf_ini.get("INIT_START", "RESUME_PLUGIN_URL")
    RESUME_SAVE_URL = conf_ini.get("INIT_START", "RESUME_SAVE_URL")
    POP_OUT_URL = conf_ini.get("INIT_START", "POP_OUT_URL")
    AccessKeyId = conf_ini.get("INIT_START", "AccessKeyId")
    AccessKeySecret = conf_ini.get("INIT_START", "AccessKeySecret")
    BucketName = conf_ini.get("INIT_START", "BucketName")
    BucketUrl = conf_ini.get("INIT_START", "BucketUrl")
    MYSQL_HOST = conf_ini.get("INIT_START", "MYSQL_HOST")
    MYSQL_USER = conf_ini.get("INIT_START", "MYSQL_USER")
    MYSQL_PASSWD = conf_ini.get("INIT_START", "MYSQL_PASSWD")
    MYSQL_DB = conf_ini.get("INIT_START", "MYSQL_DB")
    CLEAN_RESUME_URL = conf_ini.get("INIT_START", "CLEAN_RESUME_URL")
    TIME_RANGE_URL = conf_ini.get("INIT_START", "TIME_RANGE_URL")
    SEARCH_STATUS_URL = conf_ini.get("INIT_START", "SEARCH_STATUS_URL")
    CLEAN_JOB_URL = conf_ini.get("INIT_START", "CLEAN_JOB_URL")
except:
    pass

wu_jl_url = RESUME_DOWNLOAD_URL
wu_jlxw_url = SEARCH_STATUS_URL


class Module_boss(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Module_boss, cls).__new__(cls)
        return cls.__instance

    def __init__(self, cookies):
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict(Cookie_str2dict(cookies).merge(), cookiejar=None, overwrite=True)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.79 Safari/537.36',
        }

    # boss登录判断
    def login_judge_boss(self):
        home_url = 'https://www.zhipin.com/boss/user/info.html'
        response = self.session.get(url=home_url, headers=self.headers)
        if '登录BOSS直聘' not in response.text:
            return True
        else:
            a = 1/0

