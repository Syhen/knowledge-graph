# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/7/3 上午11:16
"""
import re
from itertools import chain

import jieba

from knowledge_graph.info_extract.word_category import *
from knowledge_graph.info_extract.corpus import *


def max_tokenize(text, corpus_check, maxlen=8):
    start_idx = 0
    while start_idx < len(text):
        for l in range(maxlen, 1, -1):
            end_idx = start_idx + l
            word = text[start_idx: end_idx]
            if word not in corpus_check:
                continue
            yield word, start_idx, end_idx
            start_idx = end_idx
            break
        else:
            start_idx += 1


class ZhuSuTokenizer(object):
    placeholder = "$"
    PATTERN_SYMPTOM = re.compile(r"[\.,，。“”](无|未|未见)([一-龘、]+)[，。,]")
    PATTERN_SPLITTER = re.compile(r"[、及与]")

    def __init__(self,
                 corpus_body,
                 corpus_symptom,
                 corpus_disease,
                 corpus_degree,
                 corpus_negative,
                 corpus_conjunction,
                 corpus_location,
                 corpus_punctuation,
                 corpus_surgery,
                 corpus_check_targets,
                 corpus_check,
                 corpus_color,
                 corpus_special_word,
                 pattern_date_range,
                 pattern_date_time,
                 pattern_yinyang,
                 pattern_area,
                 pattern_unit):
        self.corpus_body = set(corpus_body)
        self.corpus_symptom = set(corpus_symptom)
        self.corpus_disease = set(corpus_disease)
        self.corpus_degree = set(corpus_degree)
        self.corpus_negative = set(corpus_negative)
        self.corpus_conjunction = set(corpus_conjunction)
        self.corpus_location = set(corpus_location)
        self.corpus_punctuation = set(corpus_punctuation)
        self.corpus_surgery = set(corpus_surgery)
        self.corpus_check_targets = set(corpus_check_targets)
        self.corpus_check = set(corpus_check)
        self.corpus_color = set(corpus_color)
        self.corpus_special_word = set(corpus_special_word)
        self.info = {}
        self.pattern_date_range = pattern_date_range
        self.pattern_date_time = pattern_date_time
        self.pattern_yinyang = pattern_yinyang
        self.pattern_area = pattern_area
        self.pattern_unit = pattern_unit
        self._init_tokenizer()
        self._token_category = None
        self._cached_words = None

    def _init_tokenizer(self):
        add_words = self.corpus_disease.copy()
        add_words.update(self.corpus_degree)
        add_words.update(self.corpus_symptom)
        add_words.update(self.corpus_body)
        add_words.update(self.corpus_location)
        add_words.update(self.corpus_check_targets)
        for word in add_words:
            jieba.add_word(word, 100)
        segs = [
            ("少", "易"),
        ]
        for seg in segs:
            jieba.suggest_freq(seg, True)

    def _find_absolute_symptom(self, text):
        symptoms = self.PATTERN_SYMPTOM.findall(text)
        return list(chain.from_iterable([self.PATTERN_SPLITTER.split(i[-1]) for i in symptoms]))

    def _find_ranges(self, pattern, text, search_idxs=(1,)):
        pos = 0
        assert search_idxs, "assert error"
        while 1:
            search_result = pattern.search(text, pos=pos)
            if not search_result:
                break
            for idx in search_idxs:
                start_idx, end_idx = search_result.span(idx)
                date_range = search_result.group(idx)
                if end_idx != -1:
                    break
            yield date_range, start_idx, end_idx
            pos = end_idx

    def _find_date_ranges(self, text):
        return self._find_ranges(self.pattern_date_range, text)

    def _find_date_time(self, text):
        return self._find_ranges(self.pattern_date_time, text)

    def _find_yinyang(self, text):
        return self._find_ranges(self.pattern_yinyang, text, search_idxs=(1, 4))

    def _find_area(self, text):
        return self._find_ranges(self.pattern_area, text)

    def _find_unit(self, text):
        return self._find_ranges(self.pattern_unit, text)

    def _find_check_targets(self, text):
        return max_tokenize(text, self.corpus_check_targets, maxlen=9)

    def _replace_with_placeholder(self, text, replace_tokens):
        text_short = 0
        for content, start_idx, end_idx in replace_tokens:
            text = text[:start_idx - text_short] + self.placeholder + text[end_idx - text_short:]
            text_short += (end_idx - start_idx - 1)
        return text

    def tokenize(self, text):
        self._cached_words = None
        self.info = {}
        replace_tokens = []
        funcs = [
            (self._find_date_ranges, DATE_RANGE),
            (self._find_check_targets, CHECK_TARGET),
            (self._find_date_time, DATE_TIME),
            (self._find_yinyang, YIN_YANG),
            (self._find_area, AREA),
            (self._find_unit, UNIT)
        ]
        for func, cat in funcs:
            info = list(func(text))
            self.info[cat] = info
            replace_tokens.extend(info)
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
        self._cached_words = words
        return words

    @property
    def token_category(self):
        if self._cached_words is None:
            raise RuntimeError("run `tokenize` first")
        if self._token_category is not None:
            return self._token_category
        self._token_category = {}
        for cat, words in self.info.items():
            for word in words:
                self._token_category[word[0]] = cat
        corpuses = [
            (self.corpus_disease, DISEASE),
            (self.corpus_symptom, SYMPTOM),
            (self.corpus_body, BODY),
            (self.corpus_degree, DEGREE),
            (self.corpus_negative, NEGATIVE),
            (self.corpus_conjunction, CONJUNCTION),
            (self.corpus_location, LOCATION),
            (self.corpus_punctuation, PUNCTUATION),
            (self.corpus_surgery, SURGERY),
            (self.corpus_check_targets, CHECK_TARGET),
            (self.corpus_check, CHECK),
            (self.corpus_color, COLOR),
            (self.corpus_special_word, SPECIAL_WORD)
        ]
        for word in self._cached_words:
            if word in self._token_category:
                continue
            for corpus, cat in corpuses:
                if word in corpus:
                    self._token_category[word] = cat
                    break
        return self._token_category

    @token_category.setter
    def token_category(self, item):
        raise RuntimeError("can't set token category")


if __name__ == '__main__':
    import textwrap
    from collections import OrderedDict

    from pprint import pprint

    from knowledge_graph.info_extract.utils import merge_partial_words
    from knowledge_graph.info_extract.patterns import PATTERN_DATE_RANGE, PATTERN_AREA, PATTERN_DATE_TIME
    from knowledge_graph.info_extract.patterns import PATTERN_UNITS, PATTERN_YIN_YANG

    text = "患者4+年前自检发现左乳包块于本院就诊，考虑乳腺肿物，于2013-10-20行肿物切除术，术后病理提示：乳腺浸润癌。后为进一步治疗，于2013-11-04就诊于中山大学附属肿瘤医院门诊，行病理会诊：（左侧乳腺）浸润性导管癌（II级：伴癌旁纤维囊性乳腺病），免疫组化：ER（100%+），ER-β（5%+）,PR（45%+），Her-2（-），E-Cad（+++），P53（+），TOPIIa（-），EGFR（-），VEGF(+++),SMA、Calponin、CK5/6、CD10及P63均（-），34βE12（+++）。后于2013-11-07于中山大学附属肿瘤医院住院行乳腺癌根治术及化疗治疗，化疗结束后患者定期体检。1+月前体检时发现右乳有一大小约0.3*0.3cm大小结节，无乳房疼痛，表面皮肤无红肿、破溃，无乳头溢液、溢血，上肢无肿胀、麻木，无低热盗汗、恶心、呕吐、头晕、头痛、咳嗽、咳痰、咳血、发热、腹痛、腹泻，就诊于我院门诊，在门诊拟诊断为“右乳包块”收入院。患者自患病以来，精神状态良好，体力情况良好，食欲食量良好，睡眠情况良好，体重无明显变化，大便正常，小便正常。"
    # text = "患者3+天前因受凉后出现流清涕，伴咳嗽，咳白色粘液痰，痰不易咳出，反复寒战、发热，体温波动在36.8℃-40℃,感乏力不适，无头晕、头痛，无胸痛、咯血，无心慌、胸闷、呼吸困难，无腹痛、腹泻，无尿频、尿痛、尿不尽等症状。遂就诊于当地医院，诊断“发热”，予输液治疗后上述症状稍好转（具体药物不祥），反复发作，为进一步诊治就诊我院，查胸片示：双肺纹理增多，未见实变影；血常规：中性粒细胞百分比：77.30%，淋巴细胞百分比：15.2%，嗜酸性粒细胞百分比：0.0%。急诊以“发热原因：急性上呼吸道感染？”收入我科。患者病来精神、饮食、睡眠稍欠佳。3天未解大便，小便正常，体重无明显改变。"
    # text = "患者于5年前，因膀胱癌复发就诊于我院，在我院行放疗治疗，放疗后出现血尿，经对症处理后，病情好转出院。5年来反复发作，无大汗、恶心、呕吐、头晕、头痛、咳嗽、咳痰、发热、腹痛、腹泻,患者一直在院外口服药物治疗（具体不详），未见明显好转后多次就诊于我院住院止血，经治疗好后出院。2周前，患者 再次出现血尿并感血尿较前稍加重，呈深红色，伴血凝块，无尿频、尿急、尿痛及发热，无头晕、头痛、全身乏力、恶心、呕吐等不适，发病后自行口服药物治疗，具体不详，未见明显缓解，现为进一步诊治来我院就医，在门诊拟诊断为膀胱癌收入院。患者自患病以来，精神状态一般，体力情况一般，食欲食量一般，睡眠情况一般，体重无明显变化，大便正常。"
    # text = "患者于11月前因产检发现右肾结石并积水，无畏寒、发热，无咳嗽、咳痰，无胸闷、气促，无明显腰腹部疼痛，无明显尿频、尿痛及肉眼血尿，发现后患者未行特殊治疗。现患者产后3月复查CT提示右肾结石并重度积水，现为进一步诊治就诊于我院，在门诊拟诊断为“右肾结石并积水”收入院。患者自患病以来，精神状态良好，体力情况良好，食欲食量良好，睡眠情况良好，体重无明显变化，大便正常，小便正常。"
    # text = "患者于8年前无明显诱因出现右腰腹部疼痛，疼痛为持续性胀痛，无明显腹部放射痛，无畏寒、发热，无胸闷、气促，无恶心、呕吐，无明显尿频、尿急、尿痛及肉眼血尿，发病后就诊于我院行彩超提示肾结石，予反复体外冲击波碎石治疗，后患者反复出现上述情况，返院反复再次予体外冲击波碎石并予自服中药治疗效果不佳，现患者为进一步诊治来我院就医，在门诊拟诊断为“右肾结石并肾盂积水”收入院。患者自患病以来，精神状态良好，体力情况良好，食欲食量一般，睡眠情况良好，体重无明显变化，大便正常，小便正常。"
    # text = "发育正常，营养中等，意识清晰，语言正常，声音洪亮，正常面容，自主体位，步行进入病房，查体合作。无苍白，无出血，无皮疹，体毛分布正常，皮肤弹性正常。淋巴结未触及肿大。头颅无畸形、肿物、压痛，头发无光泽、分布均匀。结膜无苍白，巩膜无黄染，角膜透明，瞳孔D=3mm，双侧瞳孔等大同圆、对光反射正常，角膜反射存在。口角无歪斜，口唇无发绀，口腔无特殊气味，伸舌无偏斜，口腔黏膜光滑无溃疡，无咽部充血双侧扁桃体无肿大。颈部双侧对称，颈软，颈静脉无怒张，颈静脉回流征阴性，颈动脉无异常搏动，气管居中，甲状腺无肿大、对称。胸廓对称无畸形，双侧呼吸运动正常，肋间隙正常。两侧语颤音相等，语音振颤对称、无增强或减弱，无胸膜摩擦感，双肺叩诊呈清音，胸骨无叩痛，双肺呼吸音清，未闻及干性罗音，未闻及湿性罗音，无胸膜摩擦音。心前区无局部隆起，未触及心前区震颤，无心包摩擦感，心浊音界无扩大，叩诊正常，心率81次/分，律齐，心音有力，A2>P2,各瓣膜听诊区未及病理性杂音，无心包摩擦音周围血管征阴性。腹软，腹部无明显压痛反跳痛及肌紧张。肛门及外生殖器无异常。"
    text = "1月前患者出现发热症状，以低热为主，最高体温最高达37.9℃，痰多，呈白色粘痰，不易咳出，胸闷、气促活动时明显，伴全身乏力，无畏寒、寒战，无咽痛、鼻塞、流涕，无腹痛、腹泻，无尿频、尿急、尿痛，无头痛、恶心、呕吐，就诊于我院，诊断为肺部感染，痰培养+涂片提示多重耐药菌株及真菌感染，予替加环素、伊替米星、莫西沙星及氟康唑等药物治疗后病情好转，患者于2018.03.16拒绝复查胸部CT后自请出院，出院后自服“氟康唑分散片、莫西沙星片”治疗，今日自行停药后6小时前再次出现发热，体温最高38.2℃，伴有畏寒，无咳嗽、咳痰，无腹痛、腹泻，无尿频、尿急、尿痛，为求诊治再次就诊于我院，遂以“肺炎”收入我科，病来精神欠佳，饮食、睡眠尚可，大小便无特殊，体重无明显变化。"
    text = "3+年前患者因受凉后出现间歇性咳嗽、咳痰，为白色泡沫痰，痰少易咳出，无痰中带血，无咯血、呕血，无恶心、呕吐，无畏寒、发热，无盗汗、纳差及消瘦，无胸闷、气促，无夜间阵发性呼吸困难及端坐呼吸，未重视及正规诊治，3+年来上述症状长期易反复。10+天前患者因受凉后出现咳嗽、咳痰，痰量少，为白色脓痰，不易咳出，感胸闷、气促，活动后加重，能平卧，无恶心、呕吐，无畏寒、发热，无咯血、盗汗，无心悸、胸痛，无腹痛、腹泻及腹胀，无腰痛，无夜间阵发性呼吸困难，无端坐呼吸及双下肢水肿不适，院外于当地诊所输液（头孢药物，具体药名不详）治疗后，上述症状稍有好转，并自行开中药服用后出现腹泻。无腹痛、腹泻，无畏寒、发热，无恶心、呕吐，无乏力、纳差，无心悸、胸痛，无腰痛，无双下肢水肿。现为进一步诊治遂就诊于我院，门诊以“1.肺部感染2.高血压3.心功能不全”收住我科，患者病后精神、饮食、睡眠尚可，大小便如常。体重无明显增减。"
    text = "3+年前患者因受凉后出现间歇性咳嗽、咳痰，为白色泡沫痰，痰少易咳出，无痰中带血，无咯血、呕血，无恶心、呕吐，无畏寒、发热，无盗汗、纳差及消瘦，无胸闷、气促，无夜间阵发性呼吸困难及端坐呼吸，未重视及正规诊治，3+年来上述症状长期易反复。10+天前患者因受凉后出现咳嗽、咳痰，痰量少，为白色脓痰，不易咳出，感胸闷、气促，活动后加重，能平卧，无恶心、呕吐，无畏寒、发热，无咯血、盗汗，无心悸、胸痛，无腹痛、腹泻及腹胀，无腰痛，无夜间阵发性呼吸困难，无端坐呼吸及双下肢水肿不适，院外于当地诊所输液（头孢药物，具体药名不详）治疗后，上述症状稍有好转，并自行开中药服用后出现腹泻。无腹痛、腹泻，无畏寒、发热，无恶心、呕吐，无乏力、纳差，无心悸、胸痛，无腰痛，无双下肢水肿。现为进一步诊治遂就诊于我院，门诊以“1.肺部感染2.高血压3.心功能不全”收住我科，患者病后精神、饮食、睡眠尚可，大小便如常。体重无明显增减。"
    text = "5月前患者因突发言语不清于我院住院治疗，诊断为“脑出血、高血压、肺炎、急性呼吸衰竭”，并于2017-09-29行气管切开，之后一直有咳嗽、咳痰症状；3天前患者无明显诱因开始出现气促，伴咳嗽、咳痰，痰多、为白色粘痰、不易咳出，无畏寒、发热，无胸痛、咯血，无潮热、盗汗、纳差、乏力，无心悸、心前区疼痛，无双下肢浮肿，无意识障碍，患者家属自行予吸痰处理后患者痰仍多，气促无明显改善，今为求进一步诊治遂来我院就诊，门诊以“肺部感染”收入我科。患者病来精神、饮食、睡眠欠佳，大小便正常、但不能自理，体重无明显变化。"
    text = "1周前患者受凉后出现咳嗽、咳痰，为白色粘液痰，痰不易咳出，感咽喉不适，感腰部不适，无畏寒、发热、多汗，无鼻塞、流涕，无头昏、头痛，无恶心、呕吐，无胸闷、气促，无夜间阵发性呼吸困难等不适，未予重视。今为系统诊治，遂就诊我院门诊行胸部CT回示考虑右肺炎性病变，门诊以“肺炎”收入我科。病来患者精神、饮食、睡眠可，大便正常，小便次数增加，近来体重无明显增减。"
    text = "#" + text

    zhusu_tokenizer = ZhuSuTokenizer(
        corpus_bodies,
        corpus_symptom,
        corpus_diseases,
        corpus_degree,
        corpus_negative,
        corpus_conjunction,
        corpus_location,
        corpus_punctuation,
        corpus_surgery,
        corpus_check_targets,
        corpus_check,
        corpus_color,
        corpus_special_word,
        PATTERN_DATE_RANGE,
        PATTERN_DATE_TIME,
        PATTERN_YIN_YANG,
        PATTERN_AREA,
        PATTERN_UNITS
    )
    print(text)
    print("=" * 80)
    words = list(zhusu_tokenizer.tokenize(text))
    print("tokens:", words)
    # print("date ranges:", zhusu_tokenizer.date_ranges)
    # print("extract infos:", list(zhusu_tokenizer.extract(text)))
    i = 100000
    print("".join(words)[:i] == text[:i])


    def add_info(info, key, value):
        if isinstance(info[key], list):
            info[key].append(value)
        else:
            info[key] = value


    info_keys = dict(
        NORMAL=None,
        DISEASE="disease",
        SYMPTOM="symptom",
        BODY="body",
        DEGREE="degree",
        NEGATIVE="negative",
        CONJUNCTION=None,
        LOCATION="location",
        PUNCTUATION="punctuation",
        DATE_RANGE="datetime",
        CHECK_TARGET="check_targets",
        DATE_TIME="datetime",
        YIN_YANG="value",
        AREA="size",
        SURGERY="surgery",
    )


    def extract_info(words):
        # 根据各种条件切换key
        STOP_PROPGATION_PUNCS = [",", "，", "。", "；", "等"]
        info = OrderedDict([
            ('datetime', None),
            ('disease', []),
            ('symptom', []),  # {"size": "", "value": "", "body": ""}
            ('location', None),
            ('doubt', None),
            ('degree', []),
            ('surgery', []),
            ('department', None),
            ('body', None),
            ('check_targets', []),
            ('note', []),
            ('negative', []),
        ])
        item = []
        key = None
        for word, cat in words:
            if cat == NORMAL:
                key = None if key in ("negative",) else key
                continue
            if cat in (DATE_RANGE, DATE_TIME):
                info["datetime"] = word
            elif cat in (LOCATION,):
                info["location"] = word
            elif word in STOP_PROPGATION_PUNCS:
                if key is not None and item:
                    add_info(info, key, item)
                item = []
                key = None
            elif cat == NEGATIVE:
                key = "negative"
            elif cat in (BODY, DISEASE, AREA,):
                # TODO: 前一个是body，后一个是symptom，key应该是symptom: OK
                # TODO: 合并symptom和surgery或disease和surgery: 在提取信息之前，进行token合并: OK
                # TODO: 上腹部阵痛，呈放射性痛，无扣击痛。（这种，句号分割，但是body传递了的）
                key = "disease" if key in (None, "degree") and cat == DISEASE else key
                item.append(word)
            elif cat in (BODY, SYMPTOM, AREA,):
                key = "symptom" if key in (None, "degree") and cat == SYMPTOM else key
                item.append(word)
            elif cat == CHECK_TARGET:
                key = "check_targets"
                item.append(word)
            elif cat == SURGERY:
                key = "surgery"
                item.append(word)
                if key is not None and item:
                    add_info(info, key, item)
                item = []
                key = None
            elif cat in (YIN_YANG, UNIT):
                item.append(word)
            elif cat == DEGREE:
                key = "degree" if key is None else key
                item.append(word)
        return info


    def extract_info_by_date(words):
        tmp_words = []
        for word, cat in words:
            if cat in (DATE_TIME, DATE_RANGE):
                info = extract_info(tmp_words)
                if any(i for i in info.values()):
                    yield info
                tmp_words = []
            tmp_words.append((word, cat))
        if tmp_words:
            yield extract_info(tmp_words)


    print(textwrap.fill(text, width=120))
    words = merge_partial_words(words, zhusu_tokenizer.token_category)
    pprint(list(extract_info_by_date(words)))
    """
    否定的格式：
        NEGATIVE + [BODY]? + SYMPTOM
        [BODY]? + NEGATIVE + SYMPTOM
        
    某处出现多大的病症：
        BODY + NORMAL? + AREA + NORMAL? + SYMPTOM
    头部上部分：
        BODY + BODY 需合并
    DISEASE/SYMPTOM + SURGERY 需合并为手术
    组合：部位+症状、部位+疾病、疾病、症状{"body": "", "value": ["乳腺浸润癌"]}, {"body": "", "value": ["发热", "头痛"]}
    1. 将文本按照时间、日期、N小时前等分割。在每个片段中，做：
        1. POSITION、DEPARTMENT单独入列；
        2. 遇到PUNCTUATION（，,。），停止连接词、部位词的传递，停止疾病、症状、SURGERY的结合；
        3. CHECK_TARGET + YIN_YANG -> {"check_targets": "", "value": ""}
        4. CHECK_TARGET + CONJUNCTION（连接词）{1,} + [NORMAL]? + YINYANG -> [{"check_targets": "", "value": ""}, {"check_targets": "", "value": ""}]
        5. NEGATIVE + (SYMPTOM + CONJUNCTION){1,} -> {"negative": []}
    """
    # TODO: 双肺纹理增多，未见实变影
    # TODO: 化疗结束后患者定期体检。  如何结构化？
    # TODO: 患者自患病以来，精神状态良好，体力情况良好，食欲食量良好，睡眠情况良好，体重无明显变化，大便正常，小便正常。
    # TODO: 现患者产后3月复查CT提示右肾结石并重度积水。(右肾结石与肾结石)
    # TODO: 放疗后出现血尿 与 有血尿 还是不一样
    # 痰少易咳出，未重视及正规诊治，
    # 活动后加重，能平卧
    # word_category_mapping[zhusu_tokenizer.token_category.get(word, NORMAL)]
    for word, cat in words:
        print(word, word_category_mapping[cat])
    # pprint([(word, word_category_mapping[cat]) for word, cat in words])
