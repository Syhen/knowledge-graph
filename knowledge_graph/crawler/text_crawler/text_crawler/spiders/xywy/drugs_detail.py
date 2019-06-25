# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/25 下午2:47
"""
from datetime import datetime
import json

import scrapy

from text_crawler.items import DrugsItem
from text_crawler.spiders.base import BaseSpider


class XYWYDrugDetailSpider(BaseSpider):
    name = 'xywy_drug_detail'
    redis_key = 'drug:detail:xywy'

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
        must_have_keys = ('url',)
        self._check_data_keys(must_have_keys, data)
        url = data.pop('url', )
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }
        return scrapy.Request(
            url,
            callback=self.parse,
            meta={'extra_data': data},
            dont_filter=True,
            headers=self.headers
        )

    def parse(self, response):
        item = DrugsItem()
        item.update(response.meta['extra_data'])
        item['drug_relate_disease'] = response.xpath('//dl[contains(., "相关疾病：")]//a/text()').extract()
        item['updated_at'] = datetime.now()
        yield item
