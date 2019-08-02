# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TbshopItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()           #店铺id
    province = scrapy.Field()      #省
    city = scrapy.Field()          #城市
    county = scrapy.Field()        #县区
    FirstCate = scrapy.Field()     #一级搜索类目
    SecondCate = scrapy.Field()    #二级搜索类目
    headPicture = scrapy.Field()   #商家头像
    goodsNum = scrapy.Field()      #宝贝数
    shopName = scrapy.Field()      #店铺名称
    shopLink = scrapy.Field()      #商家url
    locArea = scrapy.Field()       #商家地址
    salesVolume = scrapy.Field()   #销量
    score = scrapy.Field()         #店铺动态评分
    isTmall = scrapy.Field()       #店铺类型（天猫店、淘宝店）
    shopRank = scrapy.Field()      #店铺星级
    mainBusiness = scrapy.Field()  #主营产品
    itemId = scrapy.Field()        #旺旺Id
    goodsShow = scrapy.Field()     #热门产品
    icon = scrapy.Field()          #卖家服务
    goodratePercent=scrapy.Field() #好评率

    urlReferer = scrapy.Field()      #当前搜索页面
    sellerName = scrapy.Field()      #掌柜名





    #经营时长
    #营业资质（爬取URL）
    #开店时间（只有淘宝有）
