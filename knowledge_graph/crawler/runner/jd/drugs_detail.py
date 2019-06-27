# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/26 下午2:01
"""
from knowledge_graph.crawler.runner.base import BaseRunner


class JDDrugDetailRunner(BaseRunner):
    URL = 'https://item.yiyaojd.com/3476280.html'

    def __init__(self, redis_connection, redis_key='drug:detail:jd', mongo_db=None, query=None):
        super(JDDrugDetailRunner, self).__init__(redis_connection, redis_key, mongo_db, query)
        self.query["source_id"] = "jd"

    def _get_total_drugs(self):
        if self.mongo_db is None:
            raise ValueError("mongo_db should not be None")
        proj = {
            "created_at": 0,
            "_id": 0,
            "updated_at": 0,
            "status": 0,
            "drug_title": 0
        }
        drugs = self.mongo_db["drugs_list"].find(self.query, proj)
        return drugs

    def run(self, drug_info):
        """
        :param drug_info: if None, all page will get. list of tuple
            url, drug_name, body, sub_body
        :return:
        """
        if drug_info is None:
            drug_info = self._get_total_drugs()
        for info in drug_info:
            url = info.pop("drug_url")
            info["url"] = url
            self.queue.push(info)
        return drug_info


if __name__ == '__main__':
    from knowledge_graph.pools import redis_connection, mongo_db

    query = {"status": {"$exists": 0}}
    runner = JDDrugDetailRunner(redis_connection, mongo_db=mongo_db, query=query)
    runner.run(drug_info=None)
