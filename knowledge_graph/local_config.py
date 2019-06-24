# -*- coding: utf-8 -*-
"""
@Created on: 2019/5/23 16:22

@Author: heyao

@Description: 
"""


class Config(object):
    REDIS_URL = "redis://localhost:6379"

    COL_LEMMAS = 'lemmas'

    MONGO_URI = "mongodb://localhost:27017"
    MONGO_AUTH = {}
    MONGO_DB_NAME = "knowledge_graph"


class DevelopmentConfig(Config):
    pass
