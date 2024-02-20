# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/1/20 21:56
# @author  : Mo
# @function: 构建2w+字的最相似字形


from tqdm import tqdm
import json
import sys
import os

path_sys = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path_sys)
print(path_sys)


from char_similar.const_dict import load_json, save_json, txt_write, txt_read
from char_similar import std_cal_sim


def tet_2w_to_2w_line_by_line_v2_shape():
    """   2w数据一一比对, 获取最相似的, 单行数据line写入   """
    ### 2w字一一对比
    dict_char_fourangle = load_json("data/char_fourangle.dict")
    list_chat_all_1 = list(dict_char_fourangle.keys()) # [:16]
    list_chat_all_2 = list(dict_char_fourangle.keys())
    kind = "shape"  # "shape"  # "all"  # "shape" # "all"   "w2v"  "pinyin"
    fw_128 = open(f"c2c_{kind}_128.dict", "a+", encoding="utf-8")
    fw = open(f"c2c_{kind}.dict", "a+", encoding="utf-8")

    for k in tqdm(list_chat_all_1, desc="data"):
        v_score = []
        for v in list_chat_all_2:
            score = std_cal_sim(k, v, rounded=4, kind=kind)
            v_score.append((v, score))
        v_score_sorted = sorted(iter(v_score), key=lambda x:x[-1], reverse=True)
        # res_dict[k] = v_score_sorted[:128]
        res_dict_128 = {k: "".join([v[0] for v in v_score_sorted][:128])}
        res_dict = {k: v_score_sorted}
        fw_128.write(json.dumps(res_dict_128, ensure_ascii=False) + "\n")
        fw.write(json.dumps(res_dict, ensure_ascii=False) + "\n")

    fw_128.close()
    fw.close()
    # save_json(res_dict_128, f"c2c_{kind}_128.dict")
    # save_json(res_dict, f"c2c_{kind}.dict")


def tet_2w_to_2w_line_by_line_v2_pinyin():
    """   2w数据一一比对, 获取最相似的, 单行数据line写入   """
    ### 2w字一一对比
    dict_char_fourangle = load_json("data/char_fourangle.dict")
    list_chat_all_1 = list(dict_char_fourangle.keys()) # [:16]
    list_chat_all_2 = list(dict_char_fourangle.keys())
    kind = "pinyin"  # "shape"  # "all"  # "shape" # "all"   "w2v"  "pinyin"
    fw_128 = open(f"c2c_{kind}_128.dict", "a+", encoding="utf-8")
    fw = open(f"c2c_{kind}.dict", "a+", encoding="utf-8")

    for k in tqdm(list_chat_all_1, desc="data"):
        v_score = []
        for v in list_chat_all_2:
            score = std_cal_sim(k, v, rounded=4, kind=kind)
            v_score.append((v, score))
        v_score_sorted = sorted(iter(v_score), key=lambda x:x[-1], reverse=True)
        # res_dict[k] = v_score_sorted[:128]
        res_dict_128 = {k: "".join([v[0] for v in v_score_sorted][:128])}
        res_dict = {k: v_score_sorted}
        fw_128.write(json.dumps(res_dict_128, ensure_ascii=False) + "\n")
        fw.write(json.dumps(res_dict, ensure_ascii=False) + "\n")

    fw_128.close()
    fw.close()
    # save_json(res_dict_128, f"c2c_{kind}_128.dict")
    # save_json(res_dict, f"c2c_{kind}.dict")


def clean_and_filter_2w_to_2w():
    """  整理和过滤相似字形的数据  """
    # 转成标准字典dict
    path_dict = "data/www_char_to_shape_128_2w.dict"
    list_2w = txt_read(path_dict)
    char2shape_dict = {}
    for w in list_2w:
        w_dict = json.loads(w.strip())
        for k, v in w_dict.items():
            char2shape_dict[k] = v[1:]
    save_json(char2shape_dict, path_dict.replace("data/", "")+".json")

    # 过滤level_1
    path_level_1 = "data/wiki_std_2013_level_1.txt.char"
    char_level_1 = txt_read(path_level_1)
    char_level_1_dict = {}
    for c in char_level_1:
        c_strip = c.strip()
        c_strip_v = char2shape_dict.get(c_strip)
        if c_strip_v:
            char_level_1_dict[c_strip] = c_strip_v
        else:
            print(c)
    # 过滤level_2
    path_level_2 = "data/wiki_std_2013_level_2.txt.char"
    char_level_2 = txt_read(path_level_2)
    char_level_2_dict = {}
    for c in char_level_2:
        c_strip = c.strip()
        c_strip_v = char2shape_dict.get(c_strip)
        if c_strip_v:
            char_level_2_dict[c_strip] = c_strip_v
        else:
            print(c)
    save_json(char_level_1_dict, path_level_1.replace("data/", "")+".json")
    save_json(char_level_2_dict, path_level_2.replace("data/", "")+".json")
    char_level_1_dict.update(char_level_2_dict)
    save_json(char_level_1_dict, "wiki_std_2013_level_12.txt.char.json")
    """
    󠄁

1

㧐

㧟

䏝

𬉼

㤘

𠳐

䥽

1

䁖

2

3

𥻗

䦃

4

㸆
    """



if __name__ == "__main__":
    myz = 0

    # # (字形shape)2w数据一一比对, 获取最相似的, 单行数据line写入
    # tet_2w_to_2w_line_by_line_v2_shape()

    # # (拼音pinyin)2w数据一一比对, 获取最相似的, 单行数据line写入
    # tet_2w_to_2w_line_by_line_v2_pinyin()

    # # 转成json并过滤
    clean_and_filter_2w_to_2w()



# nohup python tet_char_similarity.py > tc.tet_char_similarity.py.log 2>&1 &
# tail -n 10000 -f tc.tet_char_similarity.py.log


"""
output:

tail -n 1000 -f tc.tet_char_similarity.v3.py.log
nohup: ignoring input
data: 100%|██████████| 20959/20959 [1:19:22<00:00,  4.18it/s]
/home

"""

