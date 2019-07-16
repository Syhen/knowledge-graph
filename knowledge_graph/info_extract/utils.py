# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/7/4 上午9:01
"""
from knowledge_graph.info_extract.word_category import *


def merge_word(words: (list, tuple), token_category: dict) -> list:
    """将所有紧挨着的身体部位、疾病、症状、治疗方式、检查方式合并
    :param words: list. 词列表
    :param token_category: dict. 每个词的类型，默认为 `NORMAL`
    :return:
    """
    merged_words = []
    tmp_words = []
    tmp_cat = NORMAL
    for word in words:
        cat = token_category.get(word, NORMAL)
        if cat in (NORMAL, LOCATION, YIN_YANG, PUNCTUATION, CONJUNCTION, AREA, DATE_TIME,
                   DATE_RANGE, NEGATIVE, DEGREE):
            if len(tmp_words) >= 2:
                merged_words.append(("".join(tmp_words), tmp_cat))
            elif tmp_words:
                merged_words.append((tmp_words[0], tmp_cat))
            merged_words.append((word, cat))
            tmp_words = []
            continue
        # if word in (BODY, DISEASE, SYMPTOM, SURGERY, CHECK):
        tmp_words.append(word)
        tmp_cat = cat
    if len(tmp_words) >= 2:
        merged_words.append(("".join(tmp_words), tmp_cat))
    return merged_words


def merge_partial_words(words: (list, tuple), token_category: dict) -> list:
    merged_words = []
    tmp_words = []
    tmp_cats = []
    merge_cat_pairs = {(BODY, BODY), (DISEASE, SURGERY), (SYMPTOM, SURGERY), (COLOR, SYMPTOM)}
    for word in words:
        cat = token_category.get(word, NORMAL)
        if cat in (NORMAL, LOCATION, YIN_YANG, PUNCTUATION, CONJUNCTION, AREA, DATE_TIME,
                   DATE_RANGE, NEGATIVE, DEGREE):
            if len(tmp_words) >= 2:
                if tuple(tmp_cats) in merge_cat_pairs:
                    merged_words.append(("".join(tmp_words), tmp_cats[-1]))
                else:
                    merged_words.extend(list(zip(tmp_words, tmp_cats)))
            elif tmp_words:
                merged_words.append((tmp_words[0], tmp_cats[0]))
            merged_words.append((word, cat))
            tmp_words = []
            tmp_cats = []
            continue
        tmp_words.append(word)
        tmp_cats.append(cat)
    if len(tmp_words) >= 2:
        merged_words.append(("".join(tmp_words), tmp_cats[-1]))
    return merged_words


if __name__ == '__main__':
    from pprint import pprint

    from knowledge_graph.info_extract.tokenizer import word_category_mapping

    # pprint([(word, word_category_mapping[cat]) for word, cat in merge_word(words, zhusu_tokenizer.token_category)])
    # pprint([(word, word_category_mapping[cat]) for word, cat in merge_partial_words(words, zhusu_tokenizer.token_category)])
