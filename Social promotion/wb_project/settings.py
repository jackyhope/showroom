MYSQL_HOST = '******'
MYSQL_PORT = 3306
MYSQL_USER = '*****'
MYSQL_PASSWD = '*****'
MYSQL_DB = '******'

MYSQL_KEY = "mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8".format(
    user=MYSQL_USER, passwd=MYSQL_PASSWD, host=MYSQL_HOST, port=MYSQL_PORT, db=MYSQL_DB)

POOL_SIZE = 5
POOL_RECYCLE = 7200    # 连接池中的空闲连接超过1小时自动释放。
POOL_TIMEOUT = 30


PROXY_HOST = "http-dyn.abuyun.com"
PROXY_PORT = "9020"
PROXY_USER = '********'
PROXY_PASS = '********'

RETRY_TIMES = 5
DOWNLOAD_TIMEOUT = 10
