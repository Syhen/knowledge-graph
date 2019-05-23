# -*- coding: utf-8 -*-
import scrapy


class LemmaItem(scrapy.Item):
    platform = scrapy.Field()
    lemma_type_id = scrapy.Field()
    lemma_type_name = scrapy.Field()
    lemma_id = scrapy.Field()
    lemma_name = scrapy.Field()
    lemma_url = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()
