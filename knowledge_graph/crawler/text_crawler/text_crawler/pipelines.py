# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.utils.project import get_project_settings


class MongoPipeline(object):
    def __init__(self):
        settings = get_project_settings()
        self.settings = settings

    def open_spider(self, spider):
        self.mongo_client = pymongo.MongoClient(
            self.settings.get("MONGO_HOST", "localhost"),
            self.settings.get("MONGO_PORT", 27017)
        )
        self.mongo_db = self.mongo_client[self.settings.get("MONGO_DB_NAME")]
        auth = self.settings.get("MONGO_AUTH")
        if auth:
            self.mongo_db.authenticate(**auth)

    def close_spider(self, spider):
        self.mongo_client.close()


class TextCrawlerPipeline(MongoPipeline):
    def process_item(self, item, spider):
        if spider.__class__.name != 'baidubaike_lemma':
            return item
        _id = "%s_%s" % (item['lemma_type_id'], item['lemma_id'])
        self.mongo_db["lemmas"].update_one({"_id": _id}, {'$setOnInsert': item}, upsert=True)
        return item
