# -*- coding: utf-8 -*-
"""
@Created on: 2019/5/23 16:22

@Author: heyao

@Description: 
"""


class Config(object):
    REDIS_URL = "redis://localhost:6379"

    COL_LEMMAS = 'lemmas'


class DevelopmentConfig(Config):
    pass
