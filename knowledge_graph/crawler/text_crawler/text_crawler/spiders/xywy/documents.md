抓取实体：涉及实体、实体关系、实体属性等。

1. [疾病](http://jib.xywy.com/)
    
    ```python
    import scrapy
    
    class DiseaseItem(scrapy.Item):
       """疾病信息"""
        _id = scrapy.Field()  # 主键 {source_id}_{disease_id}
        source_id = scrapy.Field()  # 来源平台
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
    ```
2. [症状](http://zzk.xywy.com/)
3. [检查项目](http://jck.xywy.com/)
4. [药品](http://yao.xywy.com/)