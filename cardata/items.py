# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CardataItem(Item):

    #车主
    car_owner=Field()
    #购买车型
    car_type=Field()
    #购车地点
    buy_car_address=Field()
    #经销商
    buy_car_dealer=Field()
    #购车时间
    buy_car_date=Field()
    #油耗#目前行驶
    oil_wear=Field()


    #空间
    space=Field()
    #动力
    power=Field()
    #操控
    control=Field()
    #油耗（评分）
    oil_wear_star=Field()
    #舒适性
    confort=Field()
    #外观
    shape=Field()
    #内饰
    trim=Field()
    #性价比
    cost_effective=Field()
    #购车目的
    buy_car_aim=Field()


    comment_title=Field()
    comment_content=Field()
    
