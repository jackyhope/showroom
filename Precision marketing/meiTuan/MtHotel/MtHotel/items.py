# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MthotelItem(scrapy.Item):
    # define the fields for your item here like:
    city = scrapy.Field()
    hotelName = scrapy.Field()
    hotelUrl = scrapy.Field()
    address = scrapy.Field()
    headUrl = scrapy.Field()
    areaName = scrapy.Field()
    hotelStar = scrapy.Field()
    score = scrapy.Field()
    brand = scrapy.Field()
    _id = scrapy.Field()
    lowestPrice = scrapy.Field()
    serviceIcons = scrapy.Field()
    phone = scrapy.Field()
    qualification = scrapy.Field()


