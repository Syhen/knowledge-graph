# -*- coding: utf-8 -*-
import scrapy


class EntityItem(scrapy.Item):
    platform = scrapy.Field()
    entity_type_id = scrapy.Field()
    entity_type_name = scrapy.Field()
    entity_id = scrapy.Field()
    entity_name = scrapy.Field()
    entity_url = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()


class TextItem(scrapy.Item):
    platform = scrapy.Field()
    entity_url = scrapy.Field()

    created_at = scrapy.Field()
    updated_at = scrapy.Field()
