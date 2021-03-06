# -*- coding: utf-8 -*-
"""
@Created on: 2019/5/23 16:16

@Author: heyao

@Description: 
"""
import requests

from knowledge_graph.crawler.runner.base import BaseRunner


class BaiduBaikeLemmaRunner(BaseRunner):
    URL = 'https://baike.baidu.com/wikitag/api/getlemmas'

    def __init__(self, redis_connection, redis_key='entity:baidubaike', mongo_db=None, query=None):
        super(BaiduBaikeLemmaRunner, self).__init__(redis_connection, redis_key, mongo_db, query)

    def get_total_page(self, lemma_type_id):
        response = requests.post(
            self.URL,
            data={
                'limit': '24',
                'timeout': '3000',
                'filterTags': '[]',
                'tagId': str(lemma_type_id),
                'fromLemma': 'false',
                'contentLength': '40',
                'page': '0'
            },
            headers={'User-Agent': "PostmanRuntime/7.13.0"}
        )
        return response.json()['totalPage']

    def run(self, entity_type_id=75953, total_page=None):
        """
        :param entity_type_id: 75953: 医疗疾病, 75954: 药物, 75956: 中医药, 75955: 诊疗技术
        :param total_page: if None, all page will get
        :return:
        """
        mapping = {
            75953: '医疗疾病',
            75954: '药物',
            75956: '中医药',
            75955: '诊疗技术'
        }
        entity_type_name = mapping.get(entity_type_id, None)
        if not entity_type_name:
            raise ValueError("invalid entity_type_id %s" % entity_type_id)
        if total_page is None:
            total_page = self.get_total_page(entity_type_id)
        for page in range(total_page):
            self.queue.push({
                'entity_type_id': entity_type_id,
                'entity_type_name': entity_type_name,
                'url': self.URL,
                'page': page
            })
        return total_page


if __name__ == '__main__':
    from knowledge_graph.pools import redis_connection

    baidubaike_lemma_runner = BaiduBaikeLemmaRunner(redis_connection)
    baidubaike_lemma_runner.run(entity_type_id=75953, total_page=None)
