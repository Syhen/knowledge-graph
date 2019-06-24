# -*- coding: utf-8 -*-
"""
@Created on: 2019/5/23 16:19

@Author: heyao

@Description: 
"""
import pymongo
import redis

from knowledge_graph.config import config

redis_connection = redis.from_url(config.REDIS_URL)
client = pymongo.MongoClient(config.MONGO_URI)
mongo_db = client[config.MONGO_DB_NAME]
auth = config.MONGO_AUTH
if auth:
    mongo_db.authenticate(**auth)
