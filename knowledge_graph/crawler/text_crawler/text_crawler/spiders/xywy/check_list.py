# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/27 下午1:54
"""
from datetime import datetime
import json

import scrapy

from text_crawler.items import CheckItem
from text_crawler.spiders.base import BaseSpider


class XYWYCheckSpider(BaseSpider):
    name = 'xywy_check_list'
    redis_key = 'check:list:xywy'

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
        check_list = response.xpath('//ul[@class="clearfix letterli letterlito fYaHei"]/li')
        for check in check_list:
            item = CheckItem()
            item.update(response.meta['extra_data'])
            check_url = response.urljoin(check.xpath("./a/@href").extract()[0])
            item["source_id"] = "xywy"
            item["check_url"] = check_url
            item["check_id"] = check_url.split("/")[-1].split(".")[0].split("_")[-1]
            item["check_name"] = check.xpath("./a/@title").extract()[0]
            item['created_at'] = datetime.now()
            yield item
