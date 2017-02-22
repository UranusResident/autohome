# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import csv

class CardataPipeline(object):
	def __init__(self):
		self.file=codecs.open('car_data.json','w',encoding='utf-8')
	def process_item(self, item, spider):
		line=json.dumps(dict(item),ensure_ascii=False)+'\n'
		self.file.write(line)
		return item
	def spider_closed(self,spider):
		self.file.closed()


###mysql
# def dbHandle():
# 	conn=MySQLdb.connect(
# 		host="",
# 		user="",
# 		passwd="",
# 		charset="utf8",
# 		db="",
# 		use_unicode=False
# 		)
# 	return conn

# class CardataMysqlPipeline(object):
# 	def process_item(self,item,spider):
# 		dbObject=dbHandle()
# 		cursor=dbObject.cursor()

# 		sql='INSERT INTO table_name (key1,key2,key3,key4,key5,key6,key7,key8,key9,key10,key11,key12,\
# 			key13,key14,key15,key16,key17,key18) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
# 		param=(item['value'],item['value'],item['value'],item['value'],item['value'],item['value'],item['value'],
# 				item['value'],item['value'],item['value'],item['value'],item['value'],item['value'],item['value'],
# 				item['value'],item['value'],item['value'],item['value'])

# 		try:
# 			cursor.execute(sql,param)


# 			dbObject.commit()

# 		except Exception as e:
# 			print e
# 			dbObject.rollback()
# 		return item




###redis
# class RedisPipeline(object):

#     def __init__(self):
#         self.r = redis.StrictRedis(host='localhost', port=6379)

#     def process_item(self, item, spider):
#         if not item['id']:
#             print 'no id item!!'

#         str_recorded_item = self.r.get(item['id'])
#         final_item = None
#         if str_recorded_item is None:
#             final_item = item
#         else:
#             ritem = eval(self.r.get(item['id']))
#             final_item = dict(item.items() + ritem.items())
#         self.r.set(item['id'], final_item)

#     def close_spider(self, spider):
#         return
