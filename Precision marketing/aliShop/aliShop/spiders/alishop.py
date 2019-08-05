# -*- coding: utf-8 -*-
import scrapy
from aliShop.config import get_dict,XH_REQ,LIST_COOKIE,XH_REQ_1
import logging
from urllib import parse
from urllib.request import quote,unquote
import random
from aliShop.settings import DEFAULT_REQUEST_HEADERS
from aliShop.items import AlishopItem
from scrapy import Selector
import json
import time


class AlishopSpider(scrapy.Spider):
    name = 'alishop'
    allowed_domains = ['1688.com']
    start_urls = ['http://1688.com/']
    list_meta = get_dict(r'table\meta.json')

    def parse(self, response):
        '''按城市、类别分别创建url'''

        for index, dict_meta in enumerate(self.list_meta[510:550]):
            logging.info('{}:{}'.format(index, dict_meta))
            keywords=quote((dict_meta['SecondCate']+' '+dict_meta['ThirdCate']).encode('gbk'))
            province=quote((dict_meta['province']).encode('gbk'))
            city=quote((dict_meta['city']).encode('gbk'))
            params_search = {
                'filt':'y',
                'n': 'y',
                'netType': '1,11',
                'pageSize': '30',
                'offset': '3',
            }
            url_basic='https://s.1688.com/company/company_search.htm?keywords={}&province={}&city={}&'.format(keywords,province,city)
            url_search=url_basic+parse.urlencode(params_search)
            try:
                totalPage = self.totalPage(url=url_search, dict_meta=dict_meta)
                logging.info('【{}】共：{}页'.format(url_search,totalPage))
                for page in range(1,totalPage+1):
                    url_referer=url_search+'&beginPage={}'.format(str(page))
                    dict_meta['urlReferer'] = url_referer
                    print(url_referer)
                    yield scrapy.Request(url=url_referer,meta=dict_meta,callback=self.parse_search,priority=10)
            except:
                continue
    def parse_search(self,response):
        meta=response.meta
        sel = Selector(text=response.text)
        for company_item in sel.xpath('//li[@class="company-list-item"]'):
            dict_shop=self.jixi(company_item)
            dict_shop['FirstCate']=meta['FirstCate']
            dict_shop['SecondCate']=meta['SecondCate']
            dict_shop['ThirdCate']=meta['ThirdCate']
            dict_shop['province']=meta['province']
            dict_shop['city']=meta['city']
            dict_shop['urlReferer']=meta['urlReferer']
            if dict_shop['shopLink'].endswith('1688.com'):
                url_contactinfo=dict_shop['shopLink']+'/page/contactinfo.htm?'
                dict_shop['urlProfile']=dict_shop['shopLink']+'/page/creditdetail.htm?'
            else:
                url_contactinfo = dict_shop['shopLink'].split('?')[0] + '/page/contactinfo.htm?'
                dict_shop['urlProfile'] = dict_shop['shopLink'].split('?')[0] + '/page/creditdetail.htm?'

            yield scrapy.Request(url=url_contactinfo,meta=dict_shop,callback=self.contactinfo,priority=20)
    def shop_info(self,item,meta):

        item['_id']=meta['_id']
        item['province']=meta['province']
        item['city']=meta['city']
        item['FirstCate']=meta['FirstCate']
        item['SecondCate']=meta['SecondCate']
        item['ThirdCate']=meta['ThirdCate']
        item['companyName']=meta['companyName']
        item['shopName']=meta['shopName']
        item['shopLink']=meta['shopLink']
        item['locArea']=meta['locArea']
        item['itemId']=meta['itemId']
        item['honestyMember']=meta['honestyMember']
        item['honestyYear']=meta['honestyYear']
        item['tipTitle']=meta['tipTitle']
        item['mainProduct']=meta['mainProduct']
        item['processingMethods']=meta['processingMethods']
        item['companyNumber']=meta['companyNumber']
        item['factoryArea']=meta['factoryArea']
        item['certificate']=meta['certificate']
        item['factoryReport']=meta['factoryReport']
        item['hotProduct']=meta['hotProduct']
        item['businessModel']=meta['businessModel']
        item['urlReferer']=meta['urlReferer']

        item['contactSeller']=meta['contactSeller']
        item['sex']=meta['sex']
        item['position']=meta['position']
        item['department']=meta['department']
        item['mobilephone']=meta['mobilephone']
        item['phone']=meta['phone']
        item['wangWang']=meta['wangWang']
        item['fax']=meta['fax']
        item['medal']=meta['medal']
        item['turnaroundRate']=meta['turnaroundRate']
        item['grade']=meta['grade']

        item['registeredCapital']=meta['registeredCapital']
        item['representative']=meta['representative']
        item['scope']=meta['scope']
        item['foundedTime']=meta['foundedTime']
        item['address']=meta['address']
        item['integrityIndex']=meta['integrityIndex']
        item['totalVolume']=meta['totalVolume']
        item['totalBuyer']=meta['totalBuyer']

        return item
    def contactinfo(self,response):
        logging.info(response.url)

        '''解析商铺的联系页面'''
        meta=response.meta

        text=response.text
        sel = Selector(text=text)

        try:
            nickName = sel.xpath('string(//div[@class="ext-info"]/span/@data-nick)').extract()[0].strip()
            meta['wangWang'] = unquote(nickName)
        except:
            meta['wangWang'] = ''
        try:
            meta['medal'] = str(len(text.split('交易勋章-')[1].split('级')[0]))
        except:
            meta['medal'] = '0'
        try:
            meta['grade'] = {}
            meta['grade']['goodsDescription'] = ''
            meta['grade']['response'] = ''
            meta['grade']['delivery'] = ''
            meta['turnaroundRate '] = ''
            for description in sel.xpath('//div[@class="bsr  topbar-bsr fd-clr"]/div'):
                name = description.xpath('string(div[1])').extract()[0].strip()
                value = description.xpath('string(div[2]/div[@style="display:none"]/span)').extract()[0].strip()
                type = description.xpath('string(div[2]/div[@style="display:none"]/@class)').extract()[0].strip()
                if '货描' in name:
                    if 'higher' in type:
                        meta['grade']['goodsDescription'] = '低于同行：' + value
                    else:
                        meta['grade']['goodsDescription'] = '高于同行：' + value
                elif '响应' in name:
                    if 'higher' in type:
                        meta['grade']['response'] = '低于同行：' + value
                    else:
                        meta['grade']['response'] = '高于同行：' + value
                elif '发货' in name:
                    if 'higher' in type:
                        meta['grade']['delivery'] = '低于同行：' + value
                    else:
                        meta['grade']['delivery'] = '高于同行：' + value
                elif '回头率' in name:
                    meta['turnaroundRate'] = description.xpath('string(div[2]/span[2])').extract()[
                        0].strip()
        except:
            pass
        try:
            meta['department'] = ''
            meta['position'] = ''
            meta['contactSeller'] = ''
            meta['sex'] = ''
            contactSeller = sel.xpath('string(//div[@class="contact-info"]/dl/dd)').extract()[0].strip()
            try:
                meta['contactSeller'] = contactSeller.split('\xa0')[0].strip()
                meta['sex'] = contactSeller.split('\xa0')[1].strip()
            except:
                pass
            if '（' in meta:
                try:
                    meta['department'] = contactSeller.split('（')[1].split('）')[0].split(' ')[0].strip()
                    meta['position'] = contactSeller.split('）')[0].split('（')[1].split(' ')[1].strip()
                except:
                    pass
        except:
            pass
        try:
            meta['phone'] = ''
            meta['mobilephone'] = ''
            meta['fax'] = ''
            for dl in sel.xpath('//div[@class="contcat-desc"]/dl'):
                name = dl.xpath('string(dt)').extract()[0].strip()
                value = dl.xpath('string(dd)').extract()[0].strip()
                if '电      话' in name:
                    meta['phone'] = value
                elif '移动电话' in name:
                    meta['mobilephone'] = value
                elif '传      真' in name:
                    meta['fax'] = dl.xpath('string(dd)').extract()[0].strip()
        except:
            pass
        meta=self.profile(meta)
        item = AlishopItem()
        item = self.shop_info(item, meta)
        yield item
    def profile(self,meta):
        time.sleep(random.uniform(3,5))
        url_profile=meta['urlProfile']
        headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': random.choice(LIST_COOKIE),
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
        }
        html=XH_REQ_1(url=url_profile,headers=headers,data='')
        sel = Selector(text=html)
        meta['foundedTime'] = ''
        for li in sel.xpath('//div[@class="info-box info-right"]/table/tr'):
            try:
                tb_key = li.xpath('string(td[@class="tb-key"]/p)').extract()[0].strip()
                tb_value = li.xpath('string(td[@class="tb-info tb-value"]//span[@class="tb-value-data"])').extract()[
                    0].strip()
                if '成立时间' in tb_key:
                    try:
                        year = tb_value.split('年')[0]
                        month = tb_value.split('年')[1].split('月')[0]
                        day = tb_value.split('月')[1].split('日')[0]
                        meta['foundedTime'] = '{}-{}-{}'.format(year, month, day)
                    except:
                        pass
                elif '注册资本' in tb_key:
                    meta['registeredCapital'] = tb_value
                elif '经营范围' in tb_key:
                    meta['scope'] = tb_value
                elif '注册地址' in tb_key:
                    meta['address'] = tb_value

            except:
                pass
        meta['honestyNumber'] = ''
        meta['totalVolume'] = ''
        meta['totalBuyer'] = ''
        meta['repeatedRate'] = ''
        meta['refundRate'] = ''
        meta['serviceRate'] = ''
        meta['disputeRate'] = ''

        for rise in sel.xpath('//div[@id="J_CompanyTradeCreditRecord"]/ul/li'):
            try:
                record_name = rise.xpath('string(p[@class="record-name"])').extract()[0].strip()
                record_num = rise.xpath('string(p[2])').extract()[0].strip()
                if '累计成交数' in record_name:
                    meta['totalVolume'] = record_num
                elif '累计买家数' in record_name:
                    meta['totalBuyer'] = record_num
                elif '重复采购率' in record_name:
                    meta['repeatedRate'] = record_num
                elif '近90天退款率' in record_name:
                    meta['refundRate'] = record_num
                elif '近90天客服介入率' in record_name:
                    meta['serviceRate'] = record_num
                elif '近90天纠纷率' in record_name:
                    meta['disputeRate'] = record_num
            except:
                pass

        meta['representative']=''
        meta['integrityIndex']=''

        try:
            url_xinyong = sel.xpath('string(//div[@class="credit-open-view"]/iframe/@src)').extract()[0].strip()
            acnt =url_xinyong.split('acnt=')[1].split('&')[0].strip()
            logging.info('acnt:{}'.format(acnt))
            url_score='https://xinyong.1688.com/credit/score/get.json?acnt={}'.format(acnt)
            del headers['cookie']
            html_score=XH_REQ(url=url_score,headers=headers,data='')
            dict_score=json.loads(html_score)
            meta['representative']=dict_score['data']['score']['legalOwnerName']
            meta['integrityIndex']=dict_score['data']['score']['creditScore']
        except:
            pass

        return meta
    def jixi(self,company_item):

        dict_shop = {}
        dict_shop['shopLink'] = \
        company_item.xpath('string(div/div/div[@class="list-item-title"]/a/@href)').extract()[0].strip()
        dict_shop['_id']=dict_shop['shopLink'].split('//')[1].split('.1688.com')[0].strip()
        dict_shop['companyName'] = \
        company_item.xpath('string(div/div/div[@class="list-item-title"]/a/@title)').extract()[0].strip()
        dict_shop['shopName'] = company_item.xpath('string(div/div/div[@class="list-item-icons"]/span)').extract()[
            0].replace('｜', '').strip()
        dict_shop['itemId'] = company_item.xpath('string(@itemid)').extract()[0].strip()  # 旺旺id

        if '阿里巴巴建议您优先选择诚信通会员' in company_item.extract():
            dict_shop['honestyMember'] = '1'  # 诚信通会员
        else:
            dict_shop['honestyMember'] = '0'
        dict_shop['tipTitle'] = []
        dict_shop['honestyYear'] = '0'
        for title in company_item.xpath('div/div/div[@class="list-item-icons"]/a'):
            tip_title = title.xpath('string(@title)').extract()[0].strip()
            if '诚信通会员' in tip_title:
                dict_shop['honestyYear'] = title.xpath('string(em)').extract()[0].strip()
                continue
            if '先行赔付' in tip_title:
                tip_title = '先行赔付'
            elif '实力商家' in tip_title:
                tip_title = '实力商家'
            dict_shop['tipTitle'].append(tip_title)

        try:
            mainProduct = \
            company_item.xpath('string(div/div/div[@class="list-item-detail"]/div/div[1]/a)').extract()[0].strip()
            dict_shop['mainProduct'] = mainProduct.replace('\n', '').replace(' ', '')
        except:
            dict_shop['mainProduct'] = ''

        try:
            dict_shop['locArea'] = \
            company_item.xpath('string(div/div/div[@class="list-item-detail"]/div/div[2]/a/@title)').extract()[
                0].strip()
        except:
            dict_shop['locArea'] = ''
        try:
            dict_shop['companyNumber'] = \
            company_item.xpath('string(div/div/div[@class="list-item-detail"]/div/div[3]/a)').extract()[0].replace(
                ' ', '')
        except:
            dict_shop['companyNumber'] = ''
        try:
            dict_shop['certificate'] = company_item.xpath(
                'string(div/div/div[@class="list-item-detail"]/div/div[4]/a[@offer-stat="certificate"]/@href)').extract()[
                0].strip()
        except:
            dict_shop['certificate'] = ''
        try:
            dict_shop['factoryReport'] = company_item.xpath(
                'string(div/div/div[@class="list-item-detail"]/div/div[4]/a[@offer-stat="factory"]/@href)').extract()[
                0].strip()
        except:
            dict_shop['factoryReport'] = ''

        try:
            dict_shop['processingMethods'] = ''
            dict_shop['factoryArea'] = ''
            for detail_right in company_item.xpath(
                    'div/div/div[@class="list-item-detail"]/div[@class="detail-right"]/div'):
                title = detail_right.xpath('string(span)').extract()[0].strip()
                if '经营模式' in title:
                    try:
                        dict_shop['businessModel'] = detail_right.xpath('string(b)').extract()[0].strip()
                    except:
                        dict_shop['businessModel'] = ''
                elif '加工方式' in title:
                    try:
                        dict_shop['processingMethods'] = detail_right.xpath('string(a)').extract()[0].strip()
                    except:
                        dict_shop['processingMethods'] = ''
                elif '厂房面积' in title:
                    try:
                        dict_shop['factoryArea'] = detail_right.xpath('string(a)').extract()[0].strip()
                    except:
                        dict_shop['factoryArea'] = ''
        except:
            pass

        try:
            dict_shop['hotProduct'] = []
            for li in company_item.xpath(
                    'div[@class="list-item-right"]/div/div[@class="list-item-itemsWrap"]/ul/li'):
                try:
                    dict_hot = {}
                    try:
                        if 'data-lazyload-src' in li.extract():
                            dict_hot['picture'] = li.xpath('string(a/img/@data-lazyload-src)').extract()[0].strip()
                        else:
                            dict_hot['picture'] = li.xpath('string(a/img/@src)').extract()[0].strip()
                    except:
                        pass
                    dict_hot['title'] = li.xpath('string(a/img/@alt)').extract()[0].strip()
                    dict_hot['price'] = li.xpath('string(div/span[@class="price"]/@title)').extract()[0].strip()
                    dict_hot['volume'] = li.xpath('string(div/span[@class="volume"]/@title)').extract()[0].strip()
                    dict_shop['hotProduct'].append(dict_hot)
                except:
                    pass
        except:
            pass

        return dict_shop
    def totalPage(self,url,dict_meta):
        try:
            html=XH_REQ(url=url,headers=DEFAULT_REQUEST_HEADERS,data='')
            sel=Selector(text=html)
            if '缩短或修改您的搜索词，重新搜索'in html:
                totalPage=0
            elif '下一页' in html:
                totalPage = sel.xpath('string(//div[@class="page-op"]/span[@class="total-page"])').extract()[0].strip()
                totalPage = int(totalPage.replace('共', '').replace('页', ''))
            else:
                totalPage=1
            return totalPage
        except:
            logging.error('词条获取失败：{}'.format(dict_meta))
            pass


if __name__ == '__main__':
    pass