# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/24 上午10:38
"""
import requests
from lxml.etree import HTML

from knowledge_graph.crawler.runner.base import BaseRunner


class ASK120DrugsListRunner(BaseRunner):
    URL = 'https://yp.120ask.com/search/0-0-{page}--0-0-0-0.html'

    def __init__(self, redis_connection, redis_key='drugs:list:ask120', mongo_db=None, query=None):
        super(ASK120DrugsListRunner, self).__init__(redis_connection, redis_key, mongo_db, query)

    def _parse_total_page(self, text):
        sel = HTML(text)
        total_page = int(sel.xpath('//a[contains(., "尾页")]/@href')[0].split('/')[-1].split('-')[2])
        return total_page

    def _get_total_page(self):
        response = requests.get(
            self.URL.format(page=1),
            headers={'User-Agent': "PostmanRuntime/7.13.0"}
        )
        return self._parse_total_page(response.content)

    def run(self, total_page=None):
        """
        :param total_page: if None, all page will get
        :return:
        """
        if total_page is None:
            total_page = self._get_total_page()
        for page in range(1, total_page + 1):
            self.queue.push({
                'url': self.URL.format(page=page),
            })
        return total_page


if __name__ == '__main__':
    from knowledge_graph.pools import redis_connection

    ask120_drug_runner = ASK120DrugsListRunner(redis_connection)
    ask120_drug_runner.run(total_page=None)
