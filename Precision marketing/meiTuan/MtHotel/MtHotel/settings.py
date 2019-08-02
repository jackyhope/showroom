# -*- coding: utf-8 -*-

# Scrapy settings for MtHotel project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html


BOT_NAME = 'MtHotel'

SPIDER_MODULES = ['MtHotel.spiders']
NEWSPIDER_MODULE = 'MtHotel.spiders'

LOG_FILE = "hotel.log"
LOG_LEVEL = "INFO"


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'MtHotel (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS ={
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36',
       }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'MtHotel.middlewares.MthotelSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
'''代理'''
# DOWNLOADER_MIDDLEWARES = {
#    'MtHotel.middlewares.ProxyMiddleware': 1,
# }

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html

'''设置item存储对象'''
ITEM_PIPELINES = {
   'MtHotel.pipelines.MthotelPipeline': 300,
}

'''设置redis为 item pipline'''
# ITEM_PIPELINES = {
#     'scrapy_redis.pipelines.RedisPipeline': 300
# }


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html

'''限速'''
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1  #初始下载延时
DOWNLOAD_DELAY = 1            #请求间隔时间


'''mongo数据库'''
MONGO_URI = 'mongodb://localhost:27017'
MONGO_DB = "meituan"



'''scrapy-redis 配置'''

#确保request存储到redis中
SCHEDULER = "scrapy_redis.scheduler.Scheduler"

#确保所有爬虫共享相同的去重指纹
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

#在redis中保持scrapy-redis用到的队列，不会清除redis中的队列，从而实现暂停和恢复的功能
SCHEDULER_PERSIST = True


# redis配置(下面有两种方式)

REDIS_DB=1
# 方式一：没有密码
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

# #方式二：有密码
# REDIS_URL = 'redis://user:pass@hostname:6379'


#redis字符集设定
REDIS_ENCODING = 'utf8'




# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'




