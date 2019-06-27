# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/27 下午2:29
"""
from knowledge_graph.crawler.runner.base import BaseRunner


class XYWYCheckDetailRunner(BaseRunner):
    URL = 'http://jck.xywy.com/jc_1866.html'

    def __init__(self, redis_connection, redis_key='check:detail:xywy', mongo_db=None, query=None):
        super(XYWYCheckDetailRunner, self).__init__(redis_connection, redis_key, mongo_db, query)
        self.query["source_id"] = "xywy"

    def _get_total_drugs(self):
        if self.mongo_db is None:
            raise ValueError("mongo_db should not be None")
        proj = {
            "created_at": 0,
            "_id": 0,
            "updated_at": 0,
            "status": 0
        }
        drugs = self.mongo_db["check_list"].find(self.query, proj)
        return drugs

    def run(self, check_info):
        """
        :param check_info: if None, all page will get. list
            url, drug_name,
        :return:
        """
        if check_info is None:
            check_info = self._get_total_drugs()
        for info in check_info:
            url = info.get("check_url")
            info["url"] = url
            self.queue.push(info)
        return check_info


if __name__ == '__main__':
    from knowledge_graph.pools import redis_connection, mongo_db

    query = {"status": {"$exists": 0}}
    runner = XYWYCheckDetailRunner(redis_connection, mongo_db=mongo_db, query=query)
    runner.run(check_info=None)
