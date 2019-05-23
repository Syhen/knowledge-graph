# -*- coding: utf-8 -*-
"""
@Created on: 2019/5/23 15:38

@Author: heyao

@Description: 
"""
from scrapy_redis.spiders import RedisSpider


class BaseSpider(RedisSpider):
    name = ''

    def _check_data_keys(self, must_have_keys, data):
        if any(i not in data for i in must_have_keys):
            __error_format = "you dont have key: {keys}"
            keys = set(must_have_keys) - set(data.keys())
            raise ValueError(__error_format.format(keys=', '.join(keys)))
        return 1
