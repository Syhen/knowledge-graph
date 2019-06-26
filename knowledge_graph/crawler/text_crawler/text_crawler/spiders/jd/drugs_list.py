# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/26 上午9:19
# url: https://list.jd.com/list.html?cat=9192,12632,12637
"""
from datetime import datetime
import json

import scrapy

from text_crawler.items import DrugsItem
from text_crawler.spiders.base import BaseSpider


class JDDrugListSpider(BaseSpider):
    name = 'jd_drug_list'
    redis_key = 'drug:list:jd'

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
        drug_list = response.xpath('//div[@id="plist"]/ul/li')
        extra_data = response.meta['extra_data']
        for drug in drug_list:
            item = DrugsItem()
            item.update(extra_data)
            drug_url = response.urljoin(drug.xpath('.//div[@class="p-name"]/a/@href').extract()[0])
            item["source_id"] = "jd"
            item["drug_url"] = drug_url
            item["drug_id"] = drug_url.split("/")[-1].split(".")[0]
            drug_title = drug.xpath('.//div[@class="p-name"]/a/em/text()').extract()[0].strip()
            item["drug_title"] = drug_title
            item['created_at'] = datetime.now()
            yield item
        # next_page = response.xpath('//a[@class="pn-next"]/@href').extract()
        # if next_page:
        #     next_page = response.urljoin(next_page[0])
        #     yield scrapy.Request(
        #         next_page,
        #         meta={'extra_data': extra_data},
        #         callback=self.parse,
        #         dont_filter=True
        #     )
