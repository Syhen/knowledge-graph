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
        if spider.__class__.name != 'baidubaike_entity':
            return item
        _id = "%s_%s" % (item['entity_type_id'], item['entity_id'])
        self.mongo_db["entities"].update_one({"_id": _id}, {'$setOnInsert': item}, upsert=True)
        return item


class DrugListPipeline(MongoPipeline):
    def process_item(self, item, spider):
        if spider.__class__.name not in ("ask120_drugs", "xywy_drugs"):
            return item
        _id = "%s_%s" % (item["source_id"], item["drug_id"])
        self.mongo_db["drugs_list"].update_one({"_id": _id}, {"$setOnInsert": item}, upsert=True)
        return item


class DiseaseListPipeline(MongoPipeline):
    def process_item(self, item, spider):
        if spider.__class__.name not in ("ask120_disease_list", "xywy_disease_list"):
            return item
        _id = "%s_%s" % (item["source_id"], item["disease_id"])
        self.mongo_db["diseases_list"].update_one({"_id": _id}, {"$setOnInsert": item}, upsert=True)
        return item


class DiseaseDetailPipeline(MongoPipeline):
    def process_item(self, item, spider):
        if spider.__class__.name not in ("ask120_disease_detail", "xywy_disease_detail"):
            return item
        _id = "%s_%s" % (item["source_id"], item["disease_id"])
        self.mongo_db["diseases_detail"].update_one({"_id": _id}, {"$set": item}, upsert=True)
        return item
