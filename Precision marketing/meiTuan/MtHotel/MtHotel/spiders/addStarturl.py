# -*- coding: utf-8 -*- 
# @Author : Zhy

'''服务端：将各城市的start_url入库'''

import redis
from urllib import parse
from datetime import datetime
import logging
from MtHotel.settings import *
from MtHotel.config import DICT_CITYS
redis_key = "mtHotel:start_url"

if __name__ == '__main__':

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    for city,value in DICT_CITYS.items():
        today = str(datetime.today())[:10].replace('-', '')
        data = {
            'utm_medium': 'pc',
            'version_name': '999.9',
            'cateId': '20',
            'attr_28': '129',
            'uuid': '74BA5310CB502E46768AFF8C2FCFFCD23BB9F81EDB3D518D385A9BB5C2A6E675',
            'cityId': value['id'],
            'limit': '20',
            'startDay': today,
            'endDay': today,
        }
        params = parse.urlencode(data)
        basic = 'https://ihotel.meituan.com/hbsearch/HotelSearch?' + params
        r.lpush(redis_key,basic)
        print(basic)




