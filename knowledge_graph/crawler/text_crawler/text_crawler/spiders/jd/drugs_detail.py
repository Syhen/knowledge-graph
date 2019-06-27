# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/26 下午1:52
"""
from datetime import datetime
import json

import scrapy

from text_crawler.items import DrugsItem
from text_crawler.spiders.base import BaseSpider


class JDDrugDetailSpider(BaseSpider):
    name = 'jd_drug_detail'
    redis_key = 'drug:detail:jd'

    def make_request_from_data(self, data):
        """make request from redis data
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
        item['drug_name'] = response.xpath('//dl[contains(., "产品名称")]/dd/text()').extract_first("")
        item['drug_product_name'] = response.xpath('//dl[contains(., "药品商品名")]/dd/text()').extract_first("")
        item['drug_common_name'] = response.xpath('//dl[contains(., "药品通用名")]/dd/text()').extract_first("")
        item['drug_html'] = response.text
        item['updated_at'] = datetime.now()
        yield item
