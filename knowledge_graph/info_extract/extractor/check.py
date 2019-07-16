# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/7/9 上午10:28
"""
import re

yinyang = r"([\(（](\d{1,3}%)?(阴性|阳性|阴|阳|\+\+\+|\+\+|\+|---|--|-)[\)）]?)|(阴性|阳性)"
PATTERN_CHECK = re.compile(fr"[,：:，。](([a-zA-Z0-9\-/αβ ]{{2,30}}){yinyang})")


def extract_check(checks):
    return checks[1]


def extract_checks(text):
    return [extract_check(i) for i in PATTERN_CHECK.findall(text)]


if __name__ == '__main__':
    # print(fr"[,：:]([^一-龘]{{2, 30}}|[一-龘]{{2, 5}}){yinyang}")
    text = "CK5/6(-),CK7(+),P53(-),Bc 1-2(+),CerbB-2(1+),Ki67(40%),P170(-),S-100(-),CD31(-),TOPOIIa(+),P63(-),34βE12(-)，E-Cadherin(+),P120(-),EGFR(-),PR(-),ER(+60%中-强),D2-40(-),GCDFP-15(-),AR(+30%中)"
    print(extract_checks(text))
