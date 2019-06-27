# -*- coding: utf-8 -*-

BOT_NAME = 'text_crawler'

SPIDER_MODULES = ['text_crawler.spiders']
NEWSPIDER_MODULE = 'text_crawler.spiders'

# USER_AGENT = ''

LOG_LEVEL = "ERROR"

ROBOTSTXT_OBEY = False

# CONCURRENT_REQUESTS = 32

# DOWNLOAD_DELAY = 3
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

COOKIES_ENABLED = False

ITEM_PIPELINES = {
    'text_crawler.pipelines.TextCrawlerPipeline': 300,
    'text_crawler.pipelines.DrugListPipeline': 310,
    'text_crawler.pipelines.DrugDetailPipeline': 315,
    'text_crawler.pipelines.DiseaseListPipeline': 320,
    'text_crawler.pipelines.DiseaseDetailPipeline': 330,
    'text_crawler.pipelines.CheckListPipeline': 340,
    'text_crawler.pipelines.CheckDetailPipeline': 350
}

# AUTOTHROTTLE_START_DELAY = 5
# AUTOTHROTTLE_MAX_DELAY = 60

BAIDU_BAIKE_LEMMA_DEFAULT_URL = 'https://baike.baidu.com/wikitag/api/getlemmas'

# scrapy_redis config
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER_SERIALIZER = "json"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'
# SCHEDULER_IDLE_BEFORE_CLOSE = 10
REDIS_ITEMS_KEY = '%(spider)s:items'
REDIS_ITEMS_SERIALIZER = 'json.dumps'
REDIS_URL = 'redis://localhost:6379'
REDIS_START_URLS_AS_SET = True
REDIS_START_URLS_KEY = '%(name)s:start_urls'

# Mongo config
MONGO_HOST = 'localhost'
MONGO_DB_NAME = 'knowledge_graph'
MONGO_AUTH = {}
