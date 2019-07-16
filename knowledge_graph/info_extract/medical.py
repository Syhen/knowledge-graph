# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/6/28 下午1:44
"""
import re

import jieba

text = "患者20+天前无明显诱因出现头昏，时感昏昏沉沉，不清爽，无明显头痛。伴乏力、行走不稳及踩棉花感，记忆力、计算力有所下降，无视物模糊及视物旋转，无黑朦、耳鸣，无恶心、呕吐，无偏瘫、失语，无抽搐及大小便失禁，无胸痛及心悸，无口角歪斜，无眩晕、流涎，无心悸、胸闷、气促，无发热、寒战，无厌油、纳差，无腹痛、腹胀、腹泻。无尿频、尿急、尿痛等不适，现为求进一步治疗就诊于我院，门诊以“脑梗死”收入我科，患者病来饮食尚可，精神、睡眠差，大小便正常，体重未见明显增减。"
text = "患者4+年前自检发现左乳包块于本院就诊，考虑乳腺肿物，于2013-10-20行肿物切除术，术后病理提示：乳腺浸润癌。后为进一步治疗，于2013-11-04就诊于中山大学附属肿瘤医院门诊，行病理会诊：（左侧乳腺）浸润性导管癌（II级：伴癌旁纤维囊性乳腺病），免疫组化：ER（100%+），ER-β（5%+）,PR（45%+），Her-2（-），E-Cad（+++），P53（+），TOPIIa（-），EGFR（-），VEGF(+++),SMA、Calponin、CK5/6、CD10及P63均（-），34βE12（+++）。后于2013-11-07于中山大学附属肿瘤医院住院行乳腺癌根治术及化疗治疗，化疗结束后患者定期体检。1+月前体检时发现右乳有一大小约0.3*0.3cm大小结节，无乳房疼痛，表面皮肤无红肿、破溃，无乳头溢液、溢血，上肢无肿胀、麻木，无低热盗汗、恶心、呕吐、头晕、头痛、咳嗽、咳痰、咳血、发热、腹痛、腹泻，就诊于我院门诊，在门诊拟诊断为“右乳包块”收入院。患者自患病以来，精神状态良好，体力情况良好，食欲食量良好，睡眠情况良好，体重无明显变化，大便正常，小便正常。"
# text = "现病史:患者因“发现左乳无痛性包块1+月”于2017.09.26入院，排除手术禁忌后于9月28日行左乳肿物切除术+组织筋膜瓣成形术。术后病理：“左乳”结合HE组织形态及免疫组化标记结果支持浸润性导管癌伴导管内癌。免疫组化标记结果：肿瘤细胞呈：PR+、ER+、P63部分+、P120膜+、Ki67+5%、PCNA+70%、CK+、CK5/6+、E-cadherin+、BRCA1点+、S-100灶+、P53-、Her-2-、GST-π；于2017年10月18日左乳癌根治术+左腋窝前哨淋巴结活检术。术后诊断：左乳癌。根治术后病理：“左腋窝前哨淋巴结”淋巴结3枚，未见肿瘤转移。“左腋窝前哨淋巴结周围组织”淋巴结2枚，未见肿瘤转移。“左乳”肿瘤已被切除，未见癌残留；皮肤及“胸肌间组织”未见癌累及。结合患者包块病理、免疫组化结果及根治术后淋巴结转移情况，告知患方病情，患方选择继续行术后化疗，告知患方化疗方案及风险，于2017年11月6日行术后第一次化疗，方案为4期多西他赛100mg；环磷酰胺0.7g；于2017年11月28日行术后第二次化疗，方案为多西他赛100mg；环磷酰胺按0.8g；于2017年12月20日行术后第三次化疗，用药量为多西他赛100mg；环磷酰胺按0.8g；现患者为行术后第四次化疗就诊于门诊，门诊拟“左乳癌术后”收入我科。患者自上次化疗结束至今，精神状态良好，体力情况良好，食欲食量良好，睡眠情况良好，体重无明显变化，大便正常，小便正常。"
print(text)

# 词库
corpus_bodies = [
    "全身", "颜面部", "面部"
]
# 词库
corpus_diseases = [
    "咳嗽", "胸闷", "咳痰", "气促", "发热", "喘息", "疼痛", "呼吸困难", "流血", "乳腺浸润癌", "伴癌旁纤维囊性乳腺病"
]
# 正则
corpus_date_range = [
    "5月", "3天", "50+年", "2年", "3天", "3+年", "10+天", "1月", "6小时",
    "1+年", "1周", "30+年", "3+天"
]
# 词库
corpus_degree = [
    "加重", "反复", "增多", "再发"
]
# 需要词库
corpus_check = [
    "ER", "ER-β", "PR", "Her-2", "E-Cad", "P53", "TOPIIa", "EGFR", "VEGF", "SMA", "Calponin", "CK5/6",
    "CD10", "P63", "34βE12"
]

decimal = r"\d+[\.\-\+]?[\d]*[\+]?"
date_units = ["小时", "分钟", "秒", "天", "周", "星期", "月", "年"]
units = "|".join(date_units)
PATTERN_DATE_RANGE = re.compile(fr"[^年月](({decimal}({units}))[前后]?)[^\d]+")
print(PATTERN_DATE_RANGE.findall(text + "，2016年3月4日，2016年3月，3月4日，3月，"))
print(PATTERN_DATE_RANGE.search(text).span(1))

year = r"((19|20)\d{2})"
month = r"(1[012]|0?[1-9])"
day = r"([12]\d|30|31|0?[1-9])"
PATTERN_DATE_TIME = re.compile(fr"(({year}[年\-\.\/]{month}[月]?([\-\./]?{day}[日]?)?)|({month}月{day}日))")
print(PATTERN_DATE_TIME.findall(text + "，2016年3月4日，2016年3月，3月4日，3月，"))
print(PATTERN_DATE_TIME.search(text).span(1))

str_yin_yang = r"([\(（](阴性|阳性|阴|阳|\+\+\+|\+\+|\+|---|--|-)[\)）]?)|(阴性|阳性)"
PATTERN_YIN_YANG = re.compile(str_yin_yang)
PATTERN_YIN_YANG.findall("(-)")
print(PATTERN_YIN_YANG.findall(text))
print(PATTERN_YIN_YANG.search(text).span(1))

corpus_check = set(corpus_check)


def max_tokenize(text, lens=(8, 6, 5, 4, 3, 2)):
    start_idx = 0
    while start_idx < len(text):
        for l in lens:
            end_idx = start_idx + l
            word = text[start_idx: end_idx]
            if word not in corpus_check:
                continue
            yield word, start_idx, end_idx
            start_idx = end_idx
            break
        else:
            start_idx += 1


for word in ["颜面部", "再发", "为求"] + ["视物", "黑朦", "大小便失禁", "厌油"]:
    jieba.add_word(word, 100)

for seg in [("稳", "及")]:
    jieba.suggest_freq(seg, True)


class ZhuSuTokenizer(object):
    placeholder = "$"

    def __init__(self, corpus_body, corpus_disease, corpus_degree, pattern_date_range, pattern_date_time,
                 pattern_yinyang):
        self.corpus_body = set(corpus_body)
        self.corpus_disease = set(corpus_disease)
        self.corpus_degree = set(corpus_degree)
        self.date_ranges = None
        self.pattern_date_range = pattern_date_range
        self.pattern_date_time = pattern_date_time
        self.pattern_yinyang = pattern_yinyang
        self._init_tokenizer()

    def _init_tokenizer(self):
        for word in self.corpus_disease:
            jieba.add_word(word, 100)
        for word in self.corpus_degree:
            jieba.add_word(word, 100)

    def _find_ranges(self, pattern, text):
        pos = 0
        while 1:
            search_result = pattern.search(text, pos=pos)
            if not search_result:
                break
            start_idx, end_idx = search_result.span(1)
            date_range = search_result.group(1)
            yield date_range, start_idx, end_idx
            pos = end_idx

    def _find_date_ranges(self, text):
        return self._find_ranges(self.pattern_date_range, text)

    def _find_date_time(self, text):
        return self._find_ranges(self.pattern_date_time, text)

    def _find_yinyang(self, text):
        return self._find_ranges(self.pattern_yinyang, text)

    def _replace_with_placeholder(self, text, replace_tokens):
        text_short = 0
        for content, start_idx, end_idx in replace_tokens:
            text = text[:start_idx - text_short] + self.placeholder + text[end_idx - text_short:]
            text_short += (end_idx - start_idx - 1)
        return text

    def tokenize(self, text):
        replace_tokens = []
        for func in (self._find_date_ranges, max_tokenize, self._find_date_time, self._find_yinyang):
            replace_tokens.extend(list(func(text)))
        replace_tokens = list(sorted(replace_tokens, key=lambda x: x[1]))
        text = self._replace_with_placeholder(text, replace_tokens)
        special_words = [i[0] for i in replace_tokens]
        words_gen = jieba.cut(text)
        words = []
        idx = 0
        for word in words_gen:
            if word == "$":
                words.append(special_words[idx])
                idx += 1
            else:
                words.append(word)
        self.special_words = special_words
        return words


zhusu_tokenizer = ZhuSuTokenizer(
    corpus_bodies,
    corpus_diseases,
    corpus_degree,
    PATTERN_DATE_RANGE,
    PATTERN_DATE_TIME,
    PATTERN_YIN_YANG
)
# text = "手术疼痛8年后，面部疼痛4+小时"
print(text)
print("=" * 80)
words = list(zhusu_tokenizer.tokenize(text))
print("tokens:", words)
# print("date ranges:", zhusu_tokenizer.date_ranges)
# print("extract infos:", list(zhusu_tokenizer.extract(text)))
i = 100000
print("".join(words)[:i] == text[:i])
