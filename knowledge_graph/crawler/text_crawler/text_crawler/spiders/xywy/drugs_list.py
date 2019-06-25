# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/24 下午5:01
"""
from datetime import datetime
import json
import re

import scrapy

from text_crawler.items import DrugsItem
from text_crawler.spiders.base import BaseSpider


class XYWYDrugListSpider(BaseSpider):
    name = 'xywy_drug_list'
    redis_key = 'drug:list:xywy'

    PATTERN_TOTAL_PAGE = re.compile(r"count: (\d+),")

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
        extra_data = response.meta["extra_data"]
        drug_category_list = response.xpath('//div[@class="re-classify-wrap mt20"]')
        for drug_category in drug_category_list:
            # category = drug_category.xpath("./div[1]/h2/text()").extract()[0]
            drug_sub_category_list = drug_category.xpath('.//div[@class="re-sub-box"]')
            for drug_sub_category in drug_sub_category_list:
                sub_category = drug_sub_category.xpath("./div[1]/a/text()").extract()[0]
                drug_sub_sub_category_list = drug_sub_category.xpath("./div[2]/a")
                for drug_sub_sub_category in drug_sub_sub_category_list:
                    sub_sub_category = drug_sub_sub_category.xpath("./text()").extract()[0]
                    url = response.urljoin(drug_sub_sub_category.xpath("./@href").extract()[0])
                    extra_data["drug_category"] = sub_category
                    extra_data["drug_sub_category"] = sub_sub_category
                    yield scrapy.Request(
                        url,
                        meta={"extra_data": extra_data, "page": 1},
                        callback=self.parse_drug,
                        dont_filter=True
                    )

    def parse_drug(self, response):
        extra_info = response.meta['extra_data']
        page = response.meta["page"]
        total_page = response.meta.get("total_page", None)
        if total_page is None:
            total_page = int(self.PATTERN_TOTAL_PAGE.findall(response.body.decode('utf8', 'ignore'))[0])
        drug_list = response.xpath('//div[@class="h-drugs-item"]')
        for drug in drug_list:
            item = DrugsItem()
            item.update(extra_info)
            drug_url = response.urljoin(drug.xpath("./div[1]/a/@href").extract()[0])
            item["drug_url"] = drug_url
            item["drug_id"] = drug_url.split("/")[-1].split(".")[0]
            item["source_id"] = "xywy"
            item["drug_name"] = drug.xpath("./div[1]/a/text()").extract()[0].strip().split(" ", 1)[-1].replace(' ', '')
            item["drug_producer"] = drug.xpath("./div[1]/span/text()").extract()[0].strip()
            item["drug_img_url"] = drug.xpath("./div[2]/div[1]/a/img/@src").extract()[0]
            item["drug_description"] = drug.xpath("./div[2]/div[2]/div[2]/text()").extract()[0]
            item["created_at"] = datetime.now()
            yield item
        if drug_list:
            page += 1
            if page > total_page:
                return
            url = response.url.rsplit("-", 1)[0] + "-%s.htm" % page
            yield scrapy.Request(
                url,
                meta={'extra_data': extra_info, 'page': page, 'total_page': total_page},
                callback=self.parse_drug,
                dont_filter=True
            )
