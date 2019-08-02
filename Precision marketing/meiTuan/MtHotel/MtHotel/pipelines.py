# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import logging



class MthotelPipeline(object):


    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db
        self.collection = 'hotel'  # 表的名字

    @classmethod
    def from_crawler(cls, crawler):
        '''
            scrapy为我们访问settings提供了这样的一个方法，这里，
            我们需要从settings.py文件中，取得数据库的URI和数据库名称
        '''
        return cls(
            mongo_url=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        '''
        爬虫一旦开启，就会实现这个方法，连接到数据库
        '''
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]
        self.coll = self.db[self.collection]

    def close_spider(self, spider):
        '''
        爬虫一旦关闭，就会实现这个方法，关闭数据库连接
        '''
        self.client.close()

    def process_item(self, item, spider):
        postItem = dict(item)  # 把item转化成字典形式
        if self.coll.find_one({'_id':postItem['_id']}):
            logging.info('当前信息已入库')
            pass
        else:
            self.coll.insert(postItem)  # 向数据库插入一条记录
            logging.info('{}：入库成功'.format(postItem['hotelName']))
        return item



