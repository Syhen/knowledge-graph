# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/7/4 下午1:31
"""
import re

# ====================== 日期周期 ==========================
decimal = r"[\d半]+[\.\-\+]?[\d]*[\+]?"
date_units = ["小时", "分钟", "秒", "天", "周", "星期", "月", "年"]
units = "|".join(date_units)
# fr"[^年月](({decimal}({units}))[前后来|至]))[^\d]+"
PATTERN_DATE_RANGE = re.compile(fr"[^年月](({decimal}({units}))(前|后|来|至({decimal}({units}))))")

# ======================== 时间 ============================
year = r"((19|20)\d{2})"
month = r"(1[012]|0?[1-9])"
day = r"([12]\d|30|31|0?[1-9])"
PATTERN_DATE_TIME = re.compile(fr"(({year}[年\-\.\/]{month}[月]?([\-\./]?{day}[日]?)?)|({month}月{day}日))")

str_yin_yang = r"([\(（](\d{1,3}%)?(阴性|阳性|阴|阳|\+\+\+|\+\+|\+|---|--|-)[\)）]?)|(阴性|阳性)"
PATTERN_YIN_YANG = re.compile(str_yin_yang)

units = [
    "cm", "dm", "mm", "厘米", "分米", "毫米"
]
units = r"|".join(units)
decimal = r"\d+[\.\-\+/×xX\*]?[\d]*[\+]?"
chineses = r"一二三四五六七八九十零百千壹贰叁肆伍陆柒捌玖拾佰仟〇"
chinese_decimal = fr"[\d{chineses}]+[\.\-\+/]?[\d{chineses}]*[\+]?"
str_area = fr"[^xX\*×](({chinese_decimal})({units})?[×xX\*]({chinese_decimal})({units}))[^xX\*/×]"
str_area_2 = fr"(({chinese_decimal})(cm2|dm2|mm2|平方毫米|平方厘米|平方分米))"
PATTERN_AREA = re.compile(fr"{str_area}|{str_area_2}")
# TODO: Area这种正则需要特殊的方法

units = [
    "mmHg", "mmol", "bpm", "ml", "Gy", "dl", "kg", "mg", "g", "%", "％", "次", "两",
    "支", "片", "秒", "℃", "包", "/L"
]
under_units = [
    "分钟", "周", "次", "l", "m2", "分", "dl", "日", "月", "天", "mmHg"
]
sci_decimal = r"\d+[\.\-\+/]?[\d？]*[xX\*×]?\d*[\+]?"
decimal = r"\d+[\.\-\+/]?[\d？]*[\+]?"
units = r"|".join(units)
under_units = r"|".join(under_units)
# r"[^xX\*](\d+[\.\-\+]?[\d]?[\+]?)(mmHg|mmol|bpm|ml|dl|mm|cm|kg|mg|g|%|次|两|支|片)"
str_units = fr"[^xX\*/\(（]?(({sci_decimal})({units})([/／]({decimal})?({under_units}))?)[^\)\+）]"
PATTERN_UNITS = re.compile(str_units, re.IGNORECASE)


if __name__ == '__main__':
    text = "1月前。ER（50%），ERP（50%+），红细胞50%。征阴性。1月前。患者在2012年至2016年患者反复,2016年03月"
    print(PATTERN_UNITS.findall(text), "unit")
    print(PATTERN_YIN_YANG.findall(text), "yin_yang")
    print(PATTERN_DATE_RANGE.findall(text), "date_range")
