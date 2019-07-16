# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/25 下午5:15
"""
from datetime import datetime
import json

import scrapy

from text_crawler.items import SymptomItem
from text_crawler.spiders.base import BaseSpider


class XYWYSymptomListSpider(BaseSpider):
    name = 'xywy_symptom_list'
    redis_key = 'symptom:list:xywy'

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
        disease_list = response.xpath('//ul[@class="ks-ill-list clearfix mt10"]/li')
        if not disease_list:
            disease_list = response.xpath('//ul[@class="ks-zm-list clearfix mt10"]/li')
        for drug in disease_list:
            item = SymptomItem()
            item.update(response.meta['extra_data'])
            disease_url = response.urljoin(drug.xpath("./a/@href").extract()[0])
            item["source_id"] = "xywy"
            item["disease_url"] = disease_url
            item["disease_id"] = disease_url.split("/")[-1].split(".")[0].split("_")[-1]
            disease_name_list = drug.xpath("./a/@title").extract()
            if not disease_name_list:
                disease_name_list = drug.xpath("./a/text()").extract()
            disease_name = disease_name_list[0].strip()
            item["disease_name"] = disease_name
            item['created_at'] = datetime.now()
            yield item
