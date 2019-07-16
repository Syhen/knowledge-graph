# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/7/4 下午1:33
"""
# 词库
corpus_bodies = [
    "全身", "颜面部", "面部", "左乳", "乳头", "右乳", "表面皮肤", "皮肤", "乳房", "乳腺", "左侧", "右侧", "上肢", "双肺", "右踝关节",
    "左踝关节", "踝关节", "右肾", "左肾", "腰腹部", "肺部", "左乳腺", "乳腺", "双下肢", "咽喉", "腰部"
]
# 颜色
corpus_color = [
    "白色",
]
# 词库 - 基于无这种去扩展
corpus_symptom = [
    "肿胀", "麻木", "咳嗽", "胸闷", "咳痰", "气促", "发热", "喘息", "疼痛", "呼吸困难", "流血", "包块", "咳血", "腹痛", "腹泻",
    "头晕", "头痛", "呕吐", "恶心", "盗汗", "低热", "溢血", "溢液", "破溃", "红肿", "结节", "肿物", "流清涕", "寒战", "胸痛",
    "咯血", "心慌", "呼吸困难", "尿频", "尿痛", "尿不尽", "乏力", "夜尿增多", "血尿", "大汗", "全身乏力", "呕吐", "结石", "积水",
    "畏寒", "咽痛", "尿急", "感染", "体温", "泡沫痰", "脓痰", "痰中带血", "夜间阵发性呼吸困难", "端坐呼吸", "水肿", "呕血",
    "粘液痰", "痰不易咳出",
]
# 词库
corpus_diseases = [
    "乳腺浸润癌", "伴癌旁纤维囊性乳腺病", "浸润性导管癌", "乳腺癌", "急性上呼吸道感染", "膀胱癌", "肾结石", "肺炎", "左乳腺癌", "肺部感染",
    "高血压", "心功能不全"
]
# 词库
corpus_degree = [
    "加重", "反复", "增多", "再发", "重度", "复发", "间歇性", "不适",
]
corpus_check = [
    "CT", "体检"
]
# 需要词库
corpus_check_targets = [
    "ER", "ER-β", "PR", "Her-2", "E-Cad", "P53", "TOPIIa", "EGFR", "VEGF", "SMA", "Calponin", "CK5/6",
    "CD10", "P63", "34βE12", "中性粒细胞百分比", "淋巴细胞百分比", "嗜酸性粒细胞百分比",
]
# 需要词库
corpus_negative = [
    "无", "未", "否认"
]
corpus_location = [
    "中山大学附属肿瘤医院", "本院", "我院"
]
corpus_conjunction = [
    "、", "及"
]
corpus_punctuation = [
    "，", "。", "（", "）", "：", ":", ",", "；"
]
corpus_surgery = [
    "切除术", "根治术", "化疗", "放疗", "放射治疗"
]
corpus_degree_word = [
    "一般", "正常", "良好", "变化", "尚可", "欠佳", "特殊", "不适",
]
corpus_special_word = [
    "等"
]
