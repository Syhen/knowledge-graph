# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/24 下午4:01
"""
from knowledge_graph.crawler.runner.base import BaseRunner


class XYWYDiseaseDetailRunner(BaseRunner):
    URL = 'http://jib.xywy.com/html/bi.html'

    def __init__(self, redis_connection, redis_key='disease:detail:xywy', mongo_db=None, query=None):
        super(XYWYDiseaseDetailRunner, self).__init__(redis_connection, redis_key, mongo_db, query)

    def _get_total_diseases(self):
        if self.mongo_db is None:
            raise ValueError("mongo_db should not be None")
        proj = {
            "created_at": 0,
            "_id": 0,
            "updated_at": 0,
            "disease_url": 0
        }
        diseases = self.mongo_db["diseases_list"].find(self.query, proj)
        return diseases

    def run(self, disease_info):
        """
        :param disease_info: if None, all page will get. list of tuple
            url, disease_name, body, sub_body
        :return:
        """
        if disease_info is None:
            disease_info = self._get_total_diseases()
        categories = ("gaishu", "symptom", "inspect")
        for info in disease_info:
            for category in categories:
                url = "http://jib.xywy.com/il_sii/%s/%s.htm" % (category, info["disease_id"])
                info["url"] = url
                self.queue.push(info)
        return disease_info


if __name__ == '__main__':
    from knowledge_graph.pools import redis_connection, mongo_db

    query = {"status": {"$exists": 0}}
    xywy_disease_detail_runner = XYWYDiseaseDetailRunner(redis_connection, mongo_db=mongo_db, query=query)
    xywy_disease_detail_runner.run(disease_info=None)
