# -*- coding: utf-8 -*-
"""
@Created on: 2019/5/23 16:19

@Author: heyao

@Description: Base Runner
"""
import json

from hm_collections.queue.redis_queue import RedisSetQueue


class BaseRunner(object):
    def __init__(self, redis_key, redis_connection, mongo_db=None, query=None):
        self.mongo_db = mongo_db
        self.queue = RedisSetQueue(redis_connection, redis_key, serializer=json)
        self.query = query or {}

    def run(self, *args, **kwargs):
        raise NotImplementedError()
