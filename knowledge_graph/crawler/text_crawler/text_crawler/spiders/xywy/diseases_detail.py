# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/24 下午3:32
"""
from datetime import datetime
import json

import scrapy

from text_crawler.items import DiseaseItem
from text_crawler.spiders.base import BaseSpider


class XYWYDiseaseDetailSpider(BaseSpider):
    name = 'xywy_disease_detail'
    redis_key = 'disease:detail:xywy'

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
        item = DiseaseItem()
        item.update(response.meta['extra_data'])
        if "gaishu" in response.url:
            item.update(self._parse_gaishu(response))
            return item
        if 'symptom' in response.url:
            item.update(self._parse_symptom(response))
            return item
        if 'inspect' in response.url:
            item.update(self._parse_inspect(response))
            return item

    def _parse_symptom(self, response):
        disease_symptom_ids = response.xpath('//span[@class="db f12 lh240 mb15 "]/a/@href').extract()
        disease_symptom_ids = [i.split('/')[-1].split('.')[0].split("_")[0] for i in disease_symptom_ids]
        disease_symptom_names = response.xpath('//span[@class="db f12 lh240 mb15 "]/a/text()').extract()
        item = {
            "disease_symptom": dict(zip(disease_symptom_ids, disease_symptom_names)),
            'updated_at': datetime.now()
        }
        return item

    def _parse_inspect(self, response):
        disease_symptom_names = response.xpath('//li[@class="check-item"]/a/text()').extract()
        item = {
            "disease_check_method": disease_symptom_names,
            'updated_at': datetime.now()
        }
        return item

    def _parse_gaishu(self, response):
        desc = response.xpath('//div[@class="jib-articl-con jib-lh-articl"]/p/text()').extract()[0].strip()
        desc = "\n".join(i.strip() for i in desc.split("\n"))
        item = {
            "disease_description": desc
        }
        item.update(self.__parse_common_sense(response))
        item.update(self.__parse_treatment(response))
        item['updated_at'] = datetime.now()
        return item

    def __parse_common_sense(self, response):
        common_sense = response.xpath('//div[@class="mt20 articl-know"][1]')
        item = {
            "disease_is_medical_insurance": common_sense.xpath("./p[1]/span[2]/text()").extract()[0].strip(),
            "disease_get_rate": common_sense.xpath("./p[2]/span[2]/text()").extract()[0].strip(),
            "disease_easy_get": common_sense.xpath("./p[3]/span[2]/text()").extract()[0].strip(),
            "disease_contagious_ways": common_sense.xpath("./p[4]/span[2]/text()").extract()[0].strip(),
            "disease_complication": common_sense.xpath("./p[5]/span[2]/a/text()").extract(),
        }
        return item

    def __parse_treatment(self, response):
        common_sense = response.xpath('//div[@class="mt20 articl-know"][2]')
        department = common_sense.xpath("./p[1]/span[2]/text()").extract()[0].strip().replace("  ", " ").split(" ")
        item = {
            "disease_department": department,
            "disease_treatment": common_sense.xpath("./p[2]/span[2]/text()").extract()[0].strip().split(),
            "disease_treatment_range": common_sense.xpath("./p[3]/span[2]/text()").extract()[0].strip(),
            "disease_cure_rate": common_sense.xpath("./p[4]/span[2]/text()").extract()[0].strip(),
            "disease_common_drug": common_sense.xpath("./p[5]/span[2]/a/text()").extract(),
        }
        return item
