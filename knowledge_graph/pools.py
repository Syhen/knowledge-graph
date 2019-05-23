# -*- coding: utf-8 -*-
"""
@Created on: 2019/5/23 16:19

@Author: heyao

@Description: 
"""
import redis

from knowledge_graph.config import config

redis_connection = redis.from_url(config.REDIS_URL)
