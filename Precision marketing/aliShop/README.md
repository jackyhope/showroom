# aliShop
获取阿里巴巴中文站上的店铺信息


1.config.py：根据1688网站上的城市码表、搜索的类目，重新整合成用于店铺搜索的关键字【城市(省-市),搜索类别(三级类目)】，形成meta.json文件

2.从meta.json文件中读取搜索关键字，拼接成url，使用requests库获取到当前类目的返回页数，生成此词条下所有的页面并入start_urls列表中

3.使用scrapy框架，本搜索页面访问用到了代理，使用的是阿布云的代理，代理需在设置里开启，请求之间的间隔时间按代理质量自行配置

4.返回items内容如下，将数据暂存储在mongoDb数据库中


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
