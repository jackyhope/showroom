# -*- coding: utf-8 -*-
import scrapy
from MtHotel.config import *
import logging
import json
import requests
from MtHotel.items import MthotelItem
from scrapy_redis.spiders import RedisSpider

class MthotelSpider(RedisSpider):
    name = 'mtHotel'
    allowed_domains = ['meituan.com']
    redis_key = "mtHotel:start_url"
    page = 1

    def parse(self, response):
        try:
            dict_hotels=json.loads(response.text)
            totalCounts = dict_hotels['data']['totalcount']
            totalPage = int(totalCounts / 20) if int(totalCounts) % 20 == 0 else int(totalCounts / 15) + 1
            logging.info('总共：{},当前页共：{}条数据'.format(totalPage,str(len(dict_hotels['data']['searchresult']))))
            for dict_hotel in dict_hotels['data']['searchresult']:
                meta={}
                try:
                    meta['city']=dict_hotel['cityName']      #城市
                    meta['hotelName']=dict_hotel['name']     #商家名称
                    meta['hotelUrl']='https://hotel.meituan.com/{}/'.format(dict_hotel['realPoiId'])  #店铺网址
                    meta['address']=dict_hotel['addr']       #详细地址
                    meta['saleCount']=dict_hotel['historySaleCount'].replace('消费','')    #历史消费数量
                    meta['headUrl']=dict_hotel['frontImg'].replace('w.h','320.0')
                    meta['hotelType']=''      #酒店类型，暂无数据来源

                    # 该数据与搜索页面显示数据不一致
                    meta['areaName']=dict_hotel['areaName']                 #地区名
                    try:
                        meta['hotelStar']=DICT_STAR[dict_hotel['hotelStar']]    #星级
                    except:
                        meta['hotelStar']=''
                    # 评分
                    meta['score']=dict_hotel['avgScore']
                    # id
                    meta['_id']=dict_hotel['realPoiId']
                    try:
                        meta['brand']=DICT_BRAND[str(dict_hotel['brandId'])]    #品牌
                    except:
                        meta['brand'] = ''
                    #最低价
                    meta['lowestPrice'] = dict_hotel['lowestPrice']
                    yield scrapy.Request(meta['hotelUrl'], callback=self.parse_item, meta=meta)
                except:
                    logging.exception('Exception Logged')
                    logging.error('搜索页解析错误：{}'.format(dict_hotel))

            if self.page < totalPage:
                self.page = self.page + 1
                logging.info('第{}页'.format(self.page))
                yield scrapy.Request(self.basic + '&offset={}'.format(str((self.page - 1) * 20)), callback=self.parse)
        except:
            logging.error(response.url)

    def parse_item(self,response):

        meta = response.meta
        item = MthotelItem()
        html_info = response.text.split('window.__INITIAL_STATE__=')[1].split('</script>')[0].strip()[:-1]
        dict_info = json.loads(html_info)

        try:
            item['serviceIcons']=[]

            for dict_1 in dict_info['poiExt']['serviceIconsInfo']['serviceIcons']:
                item['serviceIcons'].append(dict_1['attrDesc'])

            item['phone']=dict_info['poiData']['phone']
            try:
                item['qualification']=dict_info['poiExt']['qualificationInfo']['qualificationURL']
            except:
                item['qualification']=''
            item['hotelName'],item['hotelUrl'],item['address']=meta['hotelName'],meta['hotelUrl'],meta['address']
            item['headUrl'],item['areaName'],item['hotelStar']=meta['headUrl'],meta['areaName'],meta['hotelStar']
            item['score'],item['brand'],item['_id'],item['lowestPrice']=meta['score'],meta['brand'],meta['_id'],meta['lowestPrice']

            yield item
        except:
            logging.exception('Exception Logged')
            logging.error('详情页解析错误：{}'.format(response.url))


