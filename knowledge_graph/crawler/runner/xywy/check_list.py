# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/27 下午2:12
"""
import requests
from lxml.etree import HTML
from urllib.parse import urljoin

from knowledge_graph.crawler.runner.base import BaseRunner


class XYWYCheckListRunner(BaseRunner):
    URL = 'http://jck.xywy.com/b.html'

    def __init__(self, redis_connection, redis_key='check:list:xywy', mongo_db=None, query=None):
        super(XYWYCheckListRunner, self).__init__(redis_connection, redis_key, mongo_db, query)

    def _get_total_urls(self):
        checks = []
        for char in 'abcdefghjklmnopqrstwxyz':
            checks.append("http://jck.xywy.com/%s.html" % char)
        return checks

    def run(self, check_urls):
        """
        :param check_urls: if None, all page will get. list
            url
        """
        if check_urls is None:
            check_urls = self._get_total_urls()
        for url in check_urls:
            self.queue.push({
                'url': url
            })
        return check_urls


if __name__ == '__main__':
    from knowledge_graph.pools import redis_connection

    runner = XYWYCheckListRunner(redis_connection)
    runner.run(check_urls=None)
