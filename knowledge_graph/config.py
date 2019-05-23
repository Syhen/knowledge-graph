# -*- coding: utf-8 -*-
"""
@Created on: 2019/5/23 16:23

@Author: heyao

@Description: 
"""
import os
import warnings

from knowledge_graph.local_config import DevelopmentConfig

try:
    from knowledge_graph.production_config import ProductionConfig
except ImportError:
    warnings.warn("you dont have production config")
    ProductionConfig = {}

config = dict(
    default=DevelopmentConfig,
    development=DevelopmentConfig,
    production=ProductionConfig
)

env_name = os.environ.get("KG_CONFIG_NAME", "default")
print("you are on {env_name} server".format(env_name=env_name))
config = config[env_name]
