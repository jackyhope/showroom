# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AlishopItem(scrapy.Item):
    # define the fields for your item here like:

    '''搜索页面数据'''
    
    _id = scrapy.Field()               #商铺id
    province = scrapy.Field()          #省
    city = scrapy.Field()              #市
    FirstCate = scrapy.Field()         #一级搜索类目
    SecondCate = scrapy.Field()        #二级搜索类目
    ThirdCate = scrapy.Field()         #三级搜索类目
    companyName = scrapy.Field()       #公司名称
    shopName = scrapy.Field()          #商家名称
    shopLink = scrapy.Field()          #商家url
    locArea = scrapy.Field()           #商家地址
    itemId = scrapy.Field()            #旺旺Id
    honestyMember = scrapy.Field()     #是否诚信通会员
    honestyYear = scrapy.Field()       #年份
    tipTitle = scrapy.Field()          #服务标签
    mainProduct = scrapy.Field()       #主营产品
    processingMethods = scrapy.Field() #加工方式
    companyNumber = scrapy.Field()     #员工人数
    factoryArea = scrapy.Field()       #厂房面积
    certificate = scrapy.Field()       #资质证书（企业自传基本资格证书）
    factoryReport = scrapy.Field()     #深度认证（以上信息已通过深度验厂认证）
    hotProduct = scrapy.Field()        #热门产品（产品图片、对应价格、产品名称）
    businessModel = scrapy.Field()     #经营模式
    urlReferer = scrapy.Field()        #搜索页面地址

    '''店铺主页数据'''




