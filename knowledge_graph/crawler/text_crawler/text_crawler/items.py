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


class DrugsItem(scrapy.Item):
    _id = scrapy.Field()  # 主键 {source_id}_{drug_id}
    drug_title = scrapy.Field()  # 链接的标题，在没有药物名的时候保留
    source_id = scrapy.Field()  # 来源
    drug_id = scrapy.Field()  # 药品id
    drug_url = scrapy.Field()  # 药品url
    drug_img_url = scrapy.Field()  # 封面图
    drug_name = scrapy.Field()  # 名称
    drug_common_name = scrapy.Field()  # 通用名称
    drug_product_name = scrapy.Field()  # 商品名称
    drug_category = scrapy.Field()  # 分类
    drug_sub_category = scrapy.Field()  # 次级分类
    drug_type = scrapy.Field()  # 类型
    drug_has_medical_insurance = scrapy.Field()  # 是否有医保
    # drug_price = scrapy.Field()  # 价格
    drug_producer = scrapy.Field()  # 生产商（公司）
    # drug_package = scrapy.Field()  # 包装
    drug_dosage_form = scrapy.Field()  # 剂型
    drug_is_external = scrapy.Field()  # 是否外用药
    drug_validity_period = scrapy.Field()  # 有效期
    drug_country = scrapy.Field()  # 国家
    drug_usage = scrapy.Field()  # 用法用量
    drug_composition = scrapy.Field()  # 主要成分
    drug_description = scrapy.Field()  # 适应症（描述）
    drug_adverse_reactions = scrapy.Field()  # 不良反应
    drug_ban = scrapy.Field()  # 禁忌
    drug_relate_disease = scrapy.Field()  # 相关疾病
    drug_precautions = scrapy.Field()  # 注意事项
    drug_pregnant = scrapy.Field()  # 孕妇及哺乳期妇女用药
    drug_interaction = scrapy.Field()  # 互相作用
    drug_html = scrapy.Field()  # 药品页面源代码
    created_at = scrapy.Field()  # 创建时间
    updated_at = scrapy.Field()  # 更新时间


class DiseaseItem(scrapy.Item):
    _id = scrapy.Field()  # 主键 {source_id}_{disease_id}
    source_id = scrapy.Field()  # 来源
    disease_body = scrapy.Field()  # 部位 如：头部
    disease_body_sub = scrapy.Field()  # 二级部位 如：耳
    disease_id = scrapy.Field()  # 疾病id
    disease_url = scrapy.Field()  # 疾病url
    disease_name = scrapy.Field()  # 名称
    disease_description = scrapy.Field()  # 描述
    disease_department = scrapy.Field()  # 科室
    disease_symptom = scrapy.Field()  # 症状
    disease_easy_get = scrapy.Field()  # 好发人群，易感人群
    disease_need_check = scrapy.Field()  # 需做检查
    disease_occur = scrapy.Field()  # 引发疾病
    disease_check_method = scrapy.Field()  # 检查方式
    disease_treatment = scrapy.Field()  # 治疗方法
    disease_common_drug = scrapy.Field()  # 常用药物
    disease_contagious_ways = scrapy.Field()  # 传染方式
    disease_get_rate = scrapy.Field()  # 患病比例
    disease_cure_rate = scrapy.Field()  # 治愈率
    disease_treatment_range = scrapy.Field()  # 治疗周期
    disease_is_medical_insurance = scrapy.Field()  # 是否医保疾病
    disease_complication = scrapy.Field()  # 并发症

    updated_at = scrapy.Field()
    created_at = scrapy.Field()


class SymptomItem(scrapy.Item):
    _id = scrapy.Field()  # 主键 {source_id}_{symptom_id}
    source_id = scrapy.Field()
    symptom_id = scrapy.Field()
    symptom_url = scrapy.Field()
    symptom_body = scrapy.Field()
    symptom_body_sub = scrapy.Field()
    symptom_name = scrapy.Field()
    symptom_description = scrapy.Field()

    created_at = scrapy.Field()
    updated_at = scrapy.Field()
