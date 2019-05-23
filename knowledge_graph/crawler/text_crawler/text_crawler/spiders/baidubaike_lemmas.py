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

from text_crawler.items import LemmaItem
from text_crawler.spiders.base import BaseSpider


class BaiduBaikeLemmasSpider(BaseSpider):
    name = 'baidubaike_lemma'
    redis_key = 'lemma:baidubaike'

    def make_request_from_data(self, data):
        """make request from redis data
        must have lemma_type_id, lemma_type_name and page
        page: int. start from 0
        lemma_type_id: int. entity type
        lemma_type_name: str. entity type name
        :param data: dict. redis data.
        :return:
        """
        data = json.loads(data)
        must_have_keys = ('lemma_type_id', 'lemma_type_name', 'page')
        self._check_data_keys(must_have_keys, data)
        settings = get_project_settings()
        url = data.pop('url', settings.get("BAIDU_BAIKE_LEMMA_DEFAULT_URL"))
        body = {
            'limit': '24',
            'timeout': '3000',
            'filterTags': '[]',
            'tagId': str(data['lemma_type_id']),
            'fromLemma': 'false',
            'contentLength': '40',
            'page': str(data.pop('page'))
        }
        return scrapy.FormRequest(url, callback=self.parse, formdata=body, meta={'extra_data': data}, dont_filter=True)

    def parse(self, response):
        for i in json.loads(response.body)['lemmaList']:
            item = LemmaItem()
            item.update(response.meta['extra_data'])
            item['lemma_id'] = i['lemmaId']
            item['lemma_name'] = i['lemmaTitle']
            item['lemma_url'] = i['lemmaUrl']
            item['created_at'] = datetime.now()
            item['updated_at'] = datetime.now()
            yield item
