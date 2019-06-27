# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/27 下午2:19
"""
from datetime import datetime
import json

import scrapy

from text_crawler.items import CheckItem
from text_crawler.spiders.base import BaseSpider


class XYWYCheckDetailSpider(BaseSpider):
    name = 'xywy_check_detail'
    redis_key = 'check:detail:xywy'

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
        item = CheckItem()
        item.update(response.meta['extra_data'])
        desc = response.xpath('//p[@class="baby-weeks-infor mt20 t2 lh28 f13 graydeep"]/text()').extract()[0].strip()
        item['check_description'] = desc
        item['check_category'] = response.xpath('//span[contains(., "专科分类：")]/a/text()').extract_first("")
        item['check_item_category'] = response.xpath('//span[contains(., "检查分类：")]/a/text()').extract_first("")
        item['check_gender'] = response.xpath('//span[contains(., "适用性别：")]/text()').extract()[0].split("：", 1)[-1]
        check_need_fasting = response.xpath('//span[contains(., "是否空腹：")]/text()').extract()[0].split("：", 1)[-1]
        item['check_need_fasting'] = check_need_fasting
        item['check_price'] = response.xpath('//span[contains(., "参考价格：")]/text()').extract()[0].split("：", 1)[-1]
        check_precautions = response.xpath('//div[contains(., "温馨提示：") and @class="clearfix"]/div[2]/text()').extract()[0].split("：", 1)[-1]
        item['check_precautions'] = check_precautions
        check_normal_range = "\n".join(i.strip() for i in response.xpath('//div[@class="target-txt pl20 pr20"]/p/text()').extract())
        item['check_normal_range'] = check_normal_range
        item['updated_at'] = datetime.now()
        yield item
