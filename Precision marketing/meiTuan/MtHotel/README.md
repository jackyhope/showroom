# MtHotel
获取美团酒店上的商铺信息


1.addStarturl.py：根据config.py中的城市码表生成起始url

2.本项目使用的scrapy-redis框架，由scrapy改动而来，将start_url存入了redis数据库中

3.使用scrapy框架，本搜索页面访问用到了代理，使用的是阿布云的代理，代理需在设置里开启，请求之间的间隔时间按代理质量自行配置

4.返回items内容如下，将数据暂存储在mongoDb数据库中


    '''搜索页面'''
    _id = scrapy.Field()              #店铺id
    city = scrapy.Field()             #城市
    hotelName = scrapy.Field()        #商家名称
    hotelUrl = scrapy.Field()         #店铺网址
    address = scrapy.Field()          #详细地址
    headUrl = scrapy.Field()          #历史消费数量
    areaName = scrapy.Field()         #地区名
    hotelStar = scrapy.Field()        #星级
    score = scrapy.Field()            #评分
    brand = scrapy.Field()            #品牌
    lowestPrice = scrapy.Field()      #最低价

    '''详情页面'''
    serviceIcons = scrapy.Field()     #可提供的服务项目
    phone = scrapy.Field()            #联系电话
    qualification = scrapy.Field()    #营业执照
