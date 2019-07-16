# -*- coding: utf-8 -*-
"""
Author: @heyao

Created On: 2019/7/9 上午9:16
"""
import json
import os

from tqdm import tqdm

from knowledge_graph.info_extract.extractor.symptom import extract_symptoms


data = []
path = "/home/heyao/Desktop/dataset/电子病历"
for folder_name in tqdm(os.listdir(path)):
    for filename in os.listdir(os.path.join(path, folder_name)):
        with open(os.path.join(path, folder_name, filename)) as f:
            text = f.read()
        text = "\n".join([line for line in text.split("\n") if any(line.startswith(i) for i in ("现病史", "既往史", " "))])
        try:
            symptoms = extract_symptoms(text)
        except IndexError:
            print(folder_name, filename)
            continue
        data.append({"folder": folder_name, "filename": filename, "symptoms": symptoms})

with open("/home/heyao/Desktop/symptoms_2.json", "w") as f:
    json.dump(data, f, ensure_ascii=False)
