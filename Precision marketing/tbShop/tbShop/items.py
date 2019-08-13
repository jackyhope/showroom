# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TbshopItem(scrapy.Item):
    # define the fields for your item here like:

    shopId = scrapy.Field()          # 店铺id
    channelId = scrapy.Field()       # 渠道id
    province = scrapy.Field()        #省
    city = scrapy.Field()            #城市
    county = scrapy.Field()          #县区
    category = scrapy.Field()        #一级搜索类目
    secondCategory = scrapy.Field()  #二级搜索类目
    company = scrapy.Field()         #店铺名称
    website = scrapy.Field()         #商家url
    address = scrapy.Field()         #商家地址
    name = scrapy.Field()            #姓名（空字段）
    phone = scrapy.Field()           #常用电话（空字段）
    aliwangwang = scrapy.Field()     #掌柜旺旺名
    mainProduct = scrapy.Field()     #主营产品
    favorableRate = scrapy.Field()   #好评率
    serviceTags = scrapy.Field()     #卖家服务（“消费者保障”、“金牌卖家”）
    starLevel = scrapy.Field()       #店铺星级
    certificate = scrapy.Field()     #资质证书（爬取URL）
    dsr = scrapy.Field()             #店铺动态评分
    popularProduct = scrapy.Field()  #热门产品（四张图片、对应价格）
    builtShopYear = scrapy.Field()   #开店年份
    itemsNumber = scrapy.Field()     #宝贝数
    grossSales = scrapy.Field()      #销量（总销量）
    shopType = scrapy.Field()        #店铺类型（天猫店、淘宝店（金冠店、心级店等））



    # '''搜索页面字段'''
    # _id = scrapy.Field()           #店铺id
    # province = scrapy.Field()      #省
    # city = scrapy.Field()          #城市
    # county = scrapy.Field()        #县区
    # FirstCate = scrapy.Field()     #一级搜索类目
    # SecondCate = scrapy.Field()    #二级搜索类目
    # headPicture = scrapy.Field()   #商家头像
    # goodsNum = scrapy.Field()      #宝贝数
    # shopName = scrapy.Field()      #店铺名称
    # shopLink = scrapy.Field()      #商家url
    # locArea = scrapy.Field()       #商家地址
    # salesVolume = scrapy.Field()   #销量
    # score = scrapy.Field()         #店铺动态评分
    # isTmall = scrapy.Field()       #店铺类型（天猫店、淘宝店）
    # shopRank = scrapy.Field()      #店铺星级
    # mainBusiness = scrapy.Field()  #主营产品
    # itemId = scrapy.Field()        #旺旺Id
    # goodsShow = scrapy.Field()     #热门产品
    # icon = scrapy.Field()          #卖家服务
    # goodratePercent=scrapy.Field() #好评率
    #
    # urlReferer = scrapy.Field()    #当前搜索页面
    # sellerName = scrapy.Field()    #掌柜名
    #
    #
    # '''商铺页面字段'''
    # openTime= scrapy.Field()       #经营时长
    # mainInfo= scrapy.Field()       #营业资质


