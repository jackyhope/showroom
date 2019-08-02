# tbShop
获取淘宝上的店铺信息


1.config.py：根据淘宝网的城市码表、搜索的类目，重新整合成用于店铺搜索的关键字【城市(省-市),搜索类别(二级类目)】，形成meta.json文件

2.从meta.json文件中读取搜索关键字，拼接成url，使用requests库获取到当前类目的返回页数，生成此词条下所有的页面并入start_urls列表中

3.使用scrapy框架，本搜索页面访问需要淘宝cookie（长期访问有效，无需在线），根据cookie的数量控制每条请求之间的爬取间隔

4.返回items内容如下，将数据暂存储在mongoDb数据库中


    '''搜索页面字段'''
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
    urlReferer = scrapy.Field()    #当前搜索页面
    sellerName = scrapy.Field()    #掌柜名


    '''商铺页面字段'''
    openTime= scrapy.Field()       #经营时长
    mainInfo= scrapy.Field()       #营业资质
