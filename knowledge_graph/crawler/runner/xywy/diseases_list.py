# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/24 下午2:09
"""
import requests
from lxml.etree import HTML
from urllib.parse import urljoin

from knowledge_graph.crawler.runner.base import BaseRunner


class XYWYDiseaseListRunner(BaseRunner):
    URL = 'http://jib.xywy.com/html/bi.html'

    def __init__(self, redis_connection, redis_key='disease:list:xywy', mongo_db=None, query=None):
        super(XYWYDiseaseListRunner, self).__init__(redis_connection, redis_key, mongo_db, query)

    def _get_total_diseases(self):
        diseases = []
        response = requests.get(self.URL)
        sel = HTML(response.content)
        bodys = sel.xpath('//li[@class="pr"]')
        for body in bodys:
            sub_body = body.xpath("./ul/li")
            body_name = body.xpath("./a/text()")[0]
            if not sub_body:
                url = urljoin(self.URL, body.xpath("./a/@href")[0])
                diseases.append((url, body_name, ""))
                continue
            for sub in sub_body:
                sub_body_name = sub.xpath("./a/text()")[0]
                url = urljoin(self.URL, sub.xpath("./a/@href")[0])
                diseases.append((url, body_name, sub_body_name))

        # 根据字母
        for char in 'abcdefghijklmnpqrstuwxyz':
            diseases.append(("http://jib.xywy.com/html/%s.html" % char, "", ""))
        return diseases

    def run(self, disease_info):
        """
        :param disease_info: if None, all page will get. list of tuple
            url, disease_name, body, sub_body
        :return:
        """
        if disease_info is None:
            disease_info = self._get_total_diseases()
        for url, body, sub_body in disease_info:
            self.queue.push({
                'url': url,
                'disease_body': body,
                'disease_body_sub': sub_body
            })
        return disease_info


if __name__ == '__main__':
    from knowledge_graph.pools import redis_connection

    xywy_disease_list_runner = XYWYDiseaseListRunner(redis_connection)
    xywy_disease_list_runner.run(disease_info=None)
