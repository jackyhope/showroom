# -*- coding: utf-8 -*-
import scrapy
from tbShop.config import get_dict,LIST_COOKIE,XH_REQ
import time
import json
from tbShop.items import TbshopItem
from tbShop.settings import DEFAULT_REQUEST_HEADERS
import logging
import random
import requests
import urllib
from scrapy import Selector

class TbshopSpider(scrapy.Spider):
    name = 'tbshop'
    allowed_domains = ['taobao.com']
    list_meta = get_dict(r'table\meta.json')
    start_urls = ['https://www.taobao.com']

    def parse(self, response):
        '''按城市、类别分别创建url'''

        for index,dict_meta in enumerate(self.list_meta[80:81]):
            logging.info('{}:{}'.format(index,dict_meta))
            loc=dict_meta['province'].split(',')[0] if dict_meta['city']=='' else dict_meta['city'].split(',')[0]
            params_search = {
                'q': '{} {}'.format(dict_meta['FirstCate'], dict_meta['SecondCate']),
                # 'imgfile': '',
                'js': '1',
                'style': 'grid',
                # 'stats_click': 'search_radio_all:1',
                'initiative_id': 'staobaoz_20190627',
                'ie': 'utf8',
                'loc': loc
            }
            url_search = 'https://shopsearch.taobao.com/search?'+urllib.parse.urlencode(params_search)
            try:
                totalPage=self.totalPage(url_search,dict_meta)
                logging.info('【{}】共：{}页'.format(url_search,totalPage))
                for page in range(1,totalPage+1):
                    url_referer=url_search+'&s={}'.format(str((page-1)*20))
                    dict_meta['urlReferer'] = url_referer
                    print(url_referer)
                    yield scrapy.Request(url=url_referer,meta=dict_meta,headers={'cookie':random.choice(LIST_COOKIE)},callback=self.parse_search,priority=10)
            except:
                continue
    def parse_search(self,response):
        try:
            meta=response.meta
            html_config = response.text.split('g_page_config =')[1].split('g_srp_loadCss()')[0].strip()[:-1]
            dict_config = json.loads(html_config)
            for auction in dict_config['mods']['shoplist']['data']['shopItems']:
                meta=self.jiexi(auction,meta)
                meta['_id']=meta['shopLink'].split('//')[1].split('.taobao.com')[0].strip()
                logging.info(meta['shopLink'])
                yield scrapy.Request(url=meta['shopLink'],meta=meta,headers={'cookie':random.choice(LIST_COOKIE)},callback=self.shop_info,priority=20)
        except:
            logging.exception('Exception Logged')
            logging.error('访问失败：{}'.format(response.url))
    def shop_info(self,response):
        '''店铺详情页面数据清洗'''

        meta=response.meta
        html=response.text
        meta['openTime'] = ''
        meta['mainInfo'] = ''

        if meta['isTmall']== '0':
            #淘宝页面
            if '<span class="open-time">' in html:
                meta['openTime'] = html.split('<span class="open-time">')[1].split('年')[0].strip()
        elif meta['isTmall'] == '1':
            #天猫页面
            sel = Selector(text=html)

            url_info = '//zhaoshang.tmall.com/'
            if url_info in html:
                try:
                    mainInfo = html.split('//zhaoshang.tmall.com/')[1].split('"')[0].strip()
                    meta['mainInfo'] = 'http:' + url_info + mainInfo
                except:
                    pass
            try:
                meta['openTime'] = sel.xpath('string(//span[@class="tm-shop-age-num"])').extract()[0].strip()
            except:
                pass

        self.save(meta)

    def jiexi(self,auction,dict_shop):
        '''店铺搜索页面数据清洗'''
        shopName = auction['title']
        try:
            dict_shop['goodratePercent'] = auction['goodratePercent']
        except:
            dict_shop['goodratePercent'] =''
        try:
            dict_shop['mainBusiness']=''
            dict_shop['itemId'] = auction['nid']
            dict_rank = ['心', '钻石', '皇冠', '金冠']
            dict_shop['shopName'] = shopName
            dict_shop['sellerName'] = auction['nick']
            iconClass = auction['shopIcon']['iconClass']
            dict_shop['shopRank'] = ''
            if iconClass == 'icon-service-tianmao-large':
                dict_shop['shopRank'] = ''
            elif 'rank seller-rank-' in iconClass:
                rank = int(iconClass.split('rank seller-rank-')[1].strip())
                rank_num = int((rank - 1) / 5)
                dict_shop['shopRank'] = str(rank - 5 * rank_num) + '颗' + dict_rank[rank_num]

            dict_shop['headPicture'] = auction['picUrl']
            if 'http' not in dict_shop['headPicture']:
                dict_shop['headPicture'] = 'http:' + dict_shop['headPicture']
            dict_shop['shopLink'] = auction['shopUrl']
            if 'http' not in dict_shop['shopLink']:
                dict_shop['shopLink'] = 'https:' + dict_shop['shopLink']
            dict_shop['locArea'] = auction['provcity']
            try:
                dict_shop['mainBusiness'] = auction['mainAuction'].split('0000')[0].strip()
            except:
                dict_shop['mainBusiness']=auction['mainAuction']
                pass
            if auction['isTmall']:
                dict_shop['isTmall'] = '1'
            else:
                dict_shop['isTmall'] = '0'

            dict_shop['goodsShow'] = []
            for goods in auction['auctionsInshop']:
                dict_goods = {}
                dict_goods['picture'] = goods['picUrl']
                if 'http' not in dict_goods['picture']:
                    dict_goods['picture'] = 'http:' + dict_goods['picture']
                dict_goods['price'] = goods['price']
                dict_goods['title'] = goods['title'].replace('<span class=H>', '').replace('</span>','').strip()
                dict_shop['goodsShow'].append(dict_goods)
            dict_shop['salesVolume'] = auction['totalsold']
            dict_shop['score'] = {}
            score_str = auction['dsrInfo']['dsrStr']
            score_str = json.loads(score_str)

            dict_shop['score']['describe'] = score_str['mas']
            dict_shop['score']['service'] = score_str['sas']
            dict_shop['score']['logistics'] = score_str['cas']  # 物流

            dict_shop['goodsNum'] = auction['procnt']
            dict_shop['icon'] = []
            for icon in auction['icons']:
                dict_shop['icon'].append(icon['text'])

            return dict_shop

        except:
            logging.error('商铺信息解析错误：{}'.format(shopName))
    def totalPage(self,url,dict_meta):

        try:
            time.sleep(random.uniform(20,40))
            DEFAULT_REQUEST_HEADERS.update(cookie=random.choice(LIST_COOKIE))

            html=XH_REQ(url=url,headers=DEFAULT_REQUEST_HEADERS,data='')
            html_config = html.split('g_page_config =')[1].split('g_srp_loadCss()')[0].strip()[:-1]
            dict_config = json.loads(html_config)
            totalCount = int(dict_config['mods']['sortbar']['data']['pager']['totalCount'])
            if totalCount==0:
                totalPage=0
            else:
                totalPage = int(dict_config['mods']['sortbar']['data']['pager']['totalPage'])
            return totalPage
        except:
            logging.error('词条获取失败：{}'.format(dict_meta))
            return 0

    def save(self,meta):
        item=TbshopItem()
        item['shopId'] = meta['_id']
        item['channelId'] = 'TB'
        item['province'] = meta['province'].split(',')[1]
        item['city'] = meta['city'].split(',')[1]
        item['county'] = ''
        item['category'] = meta['FirstCate']
        item['secondCategory'] = meta['SecondCate']
        item['company'] = meta['shopName']
        item['website'] = meta['shopLink']
        item['address'] = meta['locArea']
        item['name'] = ''
        item['phone'] = ''
        item['aliwangwang'] = meta['sellerName']+','+meta['itemId']
        item['mainProduct'] = meta['mainBusiness']
        item['favorableRate'] = meta['goodratePercent']
        item['serviceTags'] = meta['icon']
        item['starLevel'] = meta['shopRank']
        item['certificate'] = meta['mainInfo']
        item['dsr'] = meta['score']
        item['popularProduct'] = meta['goodsShow']
        item['builtShopYear'] = meta['openTime']
        item['itemsNumber'] = meta['goodsNum']
        item['grossSales'] = meta['salesVolume']
        item['shopType'] = meta['isTmall']

        logging.info(item)
        yield item












if __name__ == '__main__':
    url='https://shopsearch.taobao.com/search?ie=utf8&style=grid&js=1&loc=%E7%9F%B3%E5%AE%B6%E5%BA%84&initiative_id=staobaoz_20190627&q=%E4%B9%90%E5%99%A8+%E5%B0%A4%E5%85%8B%E9%87%8C%E9%87%8C'

    a=TbshopSpider().totalPage(url=url,dict_meta='')
    print(a)
    pass