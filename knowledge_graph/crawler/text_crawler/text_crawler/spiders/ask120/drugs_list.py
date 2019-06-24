# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/24 上午9:17
"""
from datetime import datetime
import json

import scrapy

from text_crawler.items import DrugsItem
from text_crawler.spiders.base import BaseSpider


class Ask120DrugsSpider(BaseSpider):
    name = 'ask120_drugs_list'
    redis_key = 'drugs:list:ask120'

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
        url = data.pop('url')
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
        }
        return scrapy.Request(url, callback=self.parse, meta={'extra_data': data}, dont_filter=True, headers=headers)

    def parse(self, response):
        drug_list = response.xpath('//div[@class="Sort-list Drug-store"]/ul/li')
        for drug in drug_list:
            item = DrugsItem()
            item.update(response.meta['extra_data'])
            drug_url = response.urljoin(drug.xpath("./a/@href").extract()[0])
            item["source_id"] = "ask120"
            item["drug_url"] = drug_url
            item["drug_id"] = drug_url.split("/")[-1].split(".")[0]
            item["drug_img_url"] = response.urljoin(drug.xpath("./a/img/@src").extract()[0])
            item["drug_name"] = drug.xpath("./div/i/a/@title").extract()[0]
            item['created_at'] = datetime.now()
            yield item
