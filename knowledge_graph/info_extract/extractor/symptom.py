# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/7/8 下午6:22
"""
from itertools import chain
import re

negatives = ["无", "未见"]
conjunctions = ("、", "及", "与")

PATTERN_SYMPTOM = re.compile(fr"[\.,，。“”]({'|'.join(negatives)})([一-龘、]+)")
PATTERN_SPLITTER = re.compile(fr"[{''.join(conjunctions)}]")


def extract_symptom(text, end_char="等"):
    text = text[-1].rsplit(end_char, 1)[0]
    symptoms = PATTERN_SPLITTER.split(text)
    real_symptoms = []
    for symptom in symptoms:
        if not symptom and real_symptoms:
            real_symptoms[-1] = real_symptoms[-1] + "及"
            continue
        real_symptoms.append(symptom)
    return real_symptoms


def extract_symptoms(text, end_char="等"):
    symptoms = PATTERN_SYMPTOM.findall(text)
    return list(chain.from_iterable(extract_symptom(t, end_char) for t in symptoms))


if __name__ == '__main__':
    text = "患者于1月前无意间发现左腕关节一蚕豆样大小包块，活动后稍感酸胀，无红肿、疼痛，无左腕关节活动障碍，无、麻木，无畏寒、发热，无咳嗽、咳痰，无胸闷、气促，无心悸、心慌，无低热、盗汗、乏力，发病后曾就诊于当地医院，诊断为“左腕腱鞘囊肿”，建议其动态观察，现为进一步诊治就诊我院门诊，门诊予“左腕腱鞘囊肿”收入我科，发病以来，患者精神、饮食、睡眠良好，体重无明显变化，二便正常。"
    print(extract_symptoms(text))
