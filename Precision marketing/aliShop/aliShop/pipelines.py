# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import json
import requests

class AlishopPipeline(object):
    list_item = []
    url_save = 'http://192.168.1.73:8088/pm/savePmShopDetails'

    def process_item(self, item, spider):

        logging.info(item)
        dict_item = dict(item)
        self.list_item.append(dict_item)
        if len(self.list_item) == 3:
            data = json.dumps(self.list_item)
            data = data.encode('utf-8')
            a = requests.post(url=self.url_save, data=data)
            logging.info(a.text)
            self.list_item = []


        return item
