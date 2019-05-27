# -*- coding: utf-8 -*-
"""
@Created on: 2019/5/23 15:18

@Author: heyao

@Description:
"""
from datetime import datetime
import json

import scrapy
from scrapy.utils.project import get_project_settings

from text_crawler.items import EntityItem
from text_crawler.spiders.base import BaseSpider


class BaiduBaikeEntitySpider(BaseSpider):
    name = 'baidubaike_entity'
    redis_key = 'entity:baidubaike'

    def make_request_from_data(self, data):
        """make request from redis data
        must have entity_type_id, entity_type_name and page
        page: int. start from 0
        entity_type_id: int. entity type
        entity_type_name: str. entity type name
        :param data: dict. redis data.
        :return:
        """
        data = json.loads(data)
        must_have_keys = ('entity_type_id', 'entity_type_name', 'page')
        self._check_data_keys(must_have_keys, data)
        settings = get_project_settings()
        url = data.pop('url', settings.get("BAIDU_BAIKE_entity_DEFAULT_URL"))
        body = {
            'limit': '24',
            'timeout': '3000',
            'filterTags': '[]',
            'tagId': str(data['entity_type_id']),
            'fromentity': 'false',
            'contentLength': '40',
            'page': str(data.pop('page'))
        }
        return scrapy.FormRequest(url, callback=self.parse, formdata=body, meta={'extra_data': data}, dont_filter=True)

    def parse(self, response):
        for i in json.loads(response.body)['lemmaList']:
            item = EntityItem()
            item.update(response.meta['extra_data'])
            item['platform'] = 'baidubaike'
            item['entity_id'] = i['lemmaId']
            item['entity_name'] = i['lemmaTitle']
            item['entity_url'] = i['lemmaUrl']
            item['created_at'] = datetime.now()
            item['updated_at'] = datetime.now()
            yield item
