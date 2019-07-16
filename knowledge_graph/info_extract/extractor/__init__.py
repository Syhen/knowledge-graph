# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/7/9 上午10:27
"""
from itertools import chain
import os

import matplotlib.pyplot as plt


class ExtractCurve(object):
    def __init__(self, base_path):
        self._curve = []
        dir_names = os.listdir(base_path)
        filenames = [list(zip([dir_name] * len(os.listdir(os.path.join(base_path, dir_name))),
                              os.listdir(os.path.join(base_path, dir_name)))) for dir_name in dir_names]
        self.base_path = base_path
        self.filenames = list(chain.from_iterable(filenames))

    def _extract_before(self, extract_function, n):
        total_entities = []
        for dir_name, filename in self.filenames[:n]:
            with open(os.path.join(self.base_path, dir_name, filename), "r") as f:
                text = f.read()
            entities = extract_function(text)
            total_entities.extend(entities)
        return len(set(total_entities))

    def extract_curve(self, extract_function, bins=(50, 100, 150, 200, 250, 300)):
        self._curve = []
        for b in bins:
            if b > len(self.filenames):
                break
            self._curve.append(self._extract_before(extract_function, b))
        return self._curve

    def plot(self):
        plt.plot(self._curve)
        plt.show()


if __name__ == '__main__':
    from knowledge_graph.info_extract.extractor.check import extract_checks
    from knowledge_graph.info_extract.extractor.disease import extract_diseases
    from knowledge_graph.info_extract.extractor.symptom import extract_symptoms

    def extract_b_symptoms(text):
        text = "\n".join([line for line in text.split("\n") if any(line.startswith(i) for i in ("现病史", "既往史", " "))])
        return extract_symptoms(text)

    curve_extractor = ExtractCurve("/home/heyao/Desktop/dataset/电子病历/")
    curve_extractor.extract_curve(extract_diseases, bins=range(0, 100000, 1000))
    curve_extractor.plot()
