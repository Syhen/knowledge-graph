# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/25 下午1:19
"""
from knowledge_graph.crawler.runner.base import BaseRunner


class XYWYDrugListRunner(BaseRunner):
    URL = 'http://yao.xywy.com/class.htm'

    def __init__(self, redis_connection, redis_key='drug:list:xywy', mongo_db=None, query=None):
        super(XYWYDrugListRunner, self).__init__(redis_connection, redis_key, mongo_db, query)

    def run(self):
        """
        :return:
        """
        self.queue.push({
            'url': self.URL,
        })


if __name__ == '__main__':
    from knowledge_graph.pools import redis_connection

    runner = XYWYDrugListRunner(redis_connection)
    runner.run()
