# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/26 上午10:07
"""
import json
import re
from urllib.parse import urlparse, parse_qs

import requests
from lxml.etree import HTML

from knowledge_graph.crawler.runner.base import BaseRunner


class JDDrugListRunner(BaseRunner):
    URL = 'https://yiyao.jd.com/'
    URL_FORMAT = 'https://list.jd.com/list.html?cat={cat}&page={page}&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main'

    def __init__(self, redis_connection, redis_key='drug:list:jd', mongo_db=None, query=None):
        super(JDDrugListRunner, self).__init__(redis_connection, redis_key, mongo_db, query)
        self.PATTERN_DRUG_CATEGORY = re.compile(r"menu:(.*),(.*)submenu", re.RegexFlag.MULTILINE)

    def _get_category(self, url):
        parse_result = urlparse(url)
        cat = parse_qs(parse_result.query)['cat'][0]
        return cat

    def _get_total_drug_page(self, url):
        response = requests.get(url)
        sel = HTML(response.content)
        total_pages = int(sel.xpath('//span[@class="p-skip"]/em/b/text()')[0])
        return total_pages

    def _get_total_drug_info(self, drug_category):
        # response = requests.get(self.URL)
        for ele_category in drug_category:
            for drug in ele_category["children"]:
                category_name = drug["NAME"]
                category_url = drug["URL"]
                total_pages = self._get_total_drug_page(category_url)
                cat = self._get_category(category_url)
                for page in range(1, total_pages + 1):
                    yield self.URL_FORMAT.format(cat=cat, page=page), category_name

    def run(self, drug_category=None):
        """
        :param drug_category:
            url, drug_category
        :return:
        """
        drug_info = self._get_total_drug_info(drug_category)
        for url, category in drug_info:
            self.queue.push({
                'url': url,
                'drug_category': category
            })
        return drug_info


if __name__ == '__main__':
    from knowledge_graph.pools import redis_connection

    drug_category = [
        {'NAME': '滋补调养', 'URL': '//www.jd.com', 'id': '174380', 'children': [
            {'NAME': '补肾壮阳', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,12634', 'id': '174381', 'o2': 1},
            {'NAME': '维矿物质', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,13240', 'id': '174382', 'o2': 1},
            {'NAME': '风湿骨外伤', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,12642', 'id': '174383', 'o2': 1},
            {'NAME': '心脑血管', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,12646', 'id': '174384', 'o2': 1},
            # {'NAME': '安神助眠', 'URL': 'https://list.jd.com/list.html?tid=1006319', 'id': '174385', 'o2': 1},
            {'NAME': '补气养血', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,12635', 'id': '174386', 'o2': 1}
        ]},
        {'NAME': '家庭常备', 'URL': '//www.jd.com', 'id': '174387', 'children': [
            {'NAME': '耳鼻喉用药', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,12637', 'id': '174388',
             'o2': 1},
            {'NAME': '眼科用药', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,12638', 'id': '174389',
             'o2': 1},
            {'NAME': '皮肤用药', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,12640', 'id': '174390',
             'o2': 1},
            {'NAME': '止痛镇痛', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,12636', 'id': '174391',
             'o2': 1},
            {'NAME': '肠胃消化', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,12641', 'id': '174392',
             'o2': 1},
            {'NAME': '感冒咳嗽', 'URL': 'https://list.jd.com/list.html?cat=9192,12632,12633', 'id': '174393',
             'o2': 1}]}, {'NAME': '男科用药', 'URL': '//www.jd.com', 'id': '174394', 'children': [
            {'NAME': '脾肾亏损',
             'URL': 'https://list.jd.com/list.html?cat=9192,12632,12634&ev=3397%5F82294&sort=sort%5Ftotalsales15%5Fdesc&trans=1&JL=2_1_0#J_crumbsBar',
             'id': '174396', 'o2': 1},
            # {'NAME': '生发固发', 'URL': 'https://list.jd.com/list.html?tid=1001205', 'id': '174397', 'o2': 1},
            {'NAME': '尿路感染',
             'URL': 'https://list.jd.com/list.html?cat=9192,12632,12643&ev=3397%5F82262&sort=sort%5Ftotalsales15%5Fdesc&trans=1&JL=3_%E9%80%82%E7%94%A8%E7%B1%BB%E5%9E%8B_%E5%B0%BF%E8%B7%AF%E6%84%9F%E6%9F%93#J_crumbsBar',
             'id': '174398', 'o2': 1},
            {'NAME': '前列腺增生',
             'URL': 'https://list.jd.com/list.html?cat=9192,12632,12634&ev=3397%5F79362&sort=sort%5Ftotalsales15%5Fdesc&trans=1&JL=2_1_0#J_crumbsBar',
             'id': '174399', 'o2': 1},
            {'NAME': '阳痿不育',
             'URL': 'https://list.jd.com/list.html?cat=9192,12632,12634&ev=3397%5F82290&sort=sort%5Ftotalsales15%5Fdesc&trans=1&JL=3_%E9%80%82%E7%94%A8%E7%B1%BB%E5%9E%8B_%E9%98%B3%E7%97%BF%E4%B8%8D%E8%82%B2#J_crumbsBar',
             'id': '174400', 'o2': 1}]},
        {'NAME': '妇科用药', 'URL': '//www.jd.com', 'id': '174401', 'children':
            [{'NAME': '妇科炎症',
              'URL': 'https://list.jd.com/list.html?cat=9192,12632,12644&ev=3397%5F79370&sort=sort%5Ftotalsales15%5Fdesc&trans=1&JL=2_1_0#J_crumbsBar',
              'id': '174402', 'o2': 1},
             {'NAME': '更年期',
              'URL': 'https://list.jd.com/list.html?cat=9192,12632,12644&ev=3397%5F37790&sort=sort%5Ftotalsales15%5Fdesc&trans=1&JL=2_1_0#J_crumbsBar',
              'id': '174403', 'o2': 1},
             {'NAME': '孕产期',
              'URL': 'https://list.jd.com/list.html?cat=9192,12632,12644&ev=3397%5F79374&sort=sort%5Ftotalsales15%5Fdesc&trans=1&JL=2_1_0#J_crumbsBar',
              'id': '174404', 'o2': 1},
             {'NAME': '阴道炎',
              'URL': 'https://list.jd.com/list.html?cat=9192,12632,12644&ev=3397%5F82286&sort=sort%5Ftotalsales15%5Fdesc&trans=1&JL=2_1_0#J_crumbsBar',
              'id': '174405', 'o2': 1},
             {'NAME': '月经不调',
              'URL': 'https://list.jd.com/list.html?cat=9192,12632,12644&ev=3397%5F79371&sort=sort%5Ftotalsales15%5Fdesc&trans=1&JL=3_%E9%80%82%E7%94%A8%E7%B1%BB%E5%9E%8B_%E6%9C%88%E7%BB%8F%E4%B8%8D%E8%B0%83#J_crumbsBar',
              'id': '174406', 'o2': 1},
             {'NAME': '避孕用药',
              'URL': 'https://list.jd.com/list.html?cat=9192,12632,13241',
              'id': '174407', 'o2': 1}]}]

    runner = JDDrugListRunner(redis_connection)
    url = "https://list.jd.com/list.html?cat=9192,12632,13240&page=2&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main"
    # runner.run(drug_category=[(url, '维矿物质')])
    runner.run(drug_category=drug_category)
