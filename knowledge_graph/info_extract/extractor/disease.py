# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/7/9 下午4:00
"""
from itertools import chain
import re

PATTERN_DISEASE = re.compile(fr"“(.*?)”")


def extract_disease(checks):
    return checks.split("、")


def extract_diseases(text):
    return list(chain.from_iterable([extract_disease(i) for i in PATTERN_DISEASE.findall(text)]))


if __name__ == '__main__':
    text = "5月前患者因突发言语不清于我院住院治疗，诊断为“脑出血、高血压、肺炎、急性呼吸衰竭”，并于2017-09-29行气管切开，之后一直有咳嗽、咳痰症状；3天前患者无明显诱因开始出现气促，伴咳嗽、咳痰，痰多、为白色粘痰、不易咳出，无畏寒、发热，无胸痛、咯血，无潮热、盗汗、纳差、乏力，无心悸、心前区疼痛，无双下肢浮肿，无意识障碍，患者家属自行予吸痰处理后患者痰仍多，气促无明显改善，今为求进一步诊治遂来我院就诊，门诊以“肺部感染”收入我科。患者病来精神、饮食、睡眠欠佳，大小便正常、但不能自理，体重无明显变化。"
    print(extract_diseases(text))
