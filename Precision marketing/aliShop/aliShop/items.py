# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AlishopItem(scrapy.Item):
    # define the fields for your item here like:
    shopId = scrapy.Field()             # 商铺id
    channelId = scrapy.Field()          # 渠道id
    province = scrapy.Field()           # 省份（省/自治区/直辖市）
    city = scrapy.Field()               # 城市（地级市/直辖市）
    county = scrapy.Field()             # 区域（县区/县级市）
    category = scrapy.Field()           # 分类
    secondCategory = scrapy.Field()     # 二级类目
    thirdCategory = scrapy.Field()      # 三级类目
    company = scrapy.Field()            # 商家名称（公司名称，检索词）
    website = scrapy.Field()            # 公司网站
    address = scrapy.Field()            # 地址
    name = scrapy.Field()               # 名字
    phone = scrapy.Field()              # 常用电话（移动电话）
    aliwangwang = scrapy.Field()        # 掌柜旺旺名
    mainProduct = scrapy.Field()        # 主营产品
    serviceTags = scrapy.Field()        # 服务标签
    certificate = scrapy.Field()        # 资质证书
    dsr = scrapy.Field()                # 店铺动态评分（毫描相符、响应速度、发货速度）
    legalRepresentative = scrapy.Field()# 法人代表
    fax = scrapy.Field()                # 传真
    popularProducts = scrapy.Field()     # 热门产品（图片、价格、产品名称）
    businessScope = scrapy.Field()      # 经营范围
    tradingMedal = scrapy.Field()       # 交易勋章
    registeredCapital = scrapy.Field()  # 注册资本
    gender = scrapy.Field()             # 性别
    shopName = scrapy.Field()           # 店铺名称
    duty = scrapy.Field()               # 职务
    registeredAddress = scrapy.Field()  # 公司注册地址
    alternatePhone = scrapy.Field()     # 备用电话（固话）
    aliIntegrityIndex = scrapy.Field()  # 阿里巴巴诚信指数
    transactionNumber = scrapy.Field()  # 成交数
    purchaserNumber = scrapy.Field()    # 买家数
    secondGlanceRate = scrapy.Field()   # 回头率
    businessModel = scrapy.Field()      # 经营模式
    department = scrapy.Field()         # 部门
    isChengxinTongMember = scrapy.Field()     # 是否诚信通会员
    chengxinTongYear = scrapy.Field()   # 诚信通年份
    processingMethod = scrapy.Field()   # 加工方式
    employeesNumber = scrapy.Field()    # 员工人数
    factoryArea = scrapy.Field()        # 厂房面积
    authentication = scrapy.Field()     # 深度认证（以上信息已通过深度验厂认证）
    weekCalledNumber = scrapy.Field()   # 本周通话被叫次数
    




    # '''搜索页面数据'''
    #
    # _id = scrapy.Field()               #商铺id
    # province = scrapy.Field()          #省
    # city = scrapy.Field()              #市
    # FirstCate = scrapy.Field()         #一级搜索类目
    # SecondCate = scrapy.Field()        #二级搜索类目
    # ThirdCate = scrapy.Field()         #三级搜索类目
    # companyName = scrapy.Field()       #公司名称
    # shopName = scrapy.Field()          #商家名称
    # shopLink = scrapy.Field()          #商家url
    # locArea = scrapy.Field()           #商家地址
    # itemId = scrapy.Field()            #旺旺Id
    # honestyMember = scrapy.Field()     #是否诚信通会员
    # honestyYear = scrapy.Field()       #年份
    # tipTitle = scrapy.Field()          #服务标签
    # mainProduct = scrapy.Field()       #主营产品
    # processingMethods = scrapy.Field() #加工方式
    # companyNumber = scrapy.Field()     #员工人数
    # factoryArea = scrapy.Field()       #厂房面积
    # certificate = scrapy.Field()       #资质证书（企业自传基本资格证书）
    # factoryReport = scrapy.Field()     #深度认证（以上信息已通过深度验厂认证）
    # hotProduct = scrapy.Field()        #热门产品（产品图片、对应价格、产品名称）
    # businessModel = scrapy.Field()     #经营模式
    # urlReferer = scrapy.Field()        #搜索页面地址
    #
    # '''店铺联系方式数据'''
    # contactSeller=scrapy.Field()       #联系人
    # sex=scrapy.Field()                 #性别
    # position=scrapy.Field()            #职务
    # department=scrapy.Field()          #部门
    # mobilephone=scrapy.Field()         #移动电话
    # phone=scrapy.Field()               #固话
    # wangWang=scrapy.Field()            #旺旺名
    # fax=scrapy.Field()                 #传真
    # medal=scrapy.Field()               #交易勋章
    # turnaroundRate=scrapy.Field()      #回头率
    # grade=scrapy.Field()               #店铺动态评分（毫描相符、响应速度、发货速度）
    #
    # '''店铺档案数据'''
    # registeredCapital=scrapy.Field()   #注册资本
    # representative=scrapy.Field()      #法定代表人
    # scope=scrapy.Field()               #经营范围
    # foundedTime=scrapy.Field()         #成立时间
    # address=scrapy.Field()             #注册地址
    # integrityIndex=scrapy.Field()      #阿里巴巴诚信指数
    # totalVolume=scrapy.Field()         #成交数
    # totalBuyer=scrapy.Field()          #买家数






