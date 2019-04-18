# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import pymongo


class ToutiaoPipeline(object):

    def __init__(self, mongo_url, mongo_db):
        self.mongo_url = mongo_url
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):  # 从settings中获取配置信息
        return cls(  # 返回给本类，初始化
                mongo_url=crawler.settings.get('MONGO_URL'),
                mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):  # 爬虫启动时
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        # print(item)
        self.db[spider.name].insert_one(dict(item))
        # self.db['toutiao2'].insert_one(dict(item))
        return item
