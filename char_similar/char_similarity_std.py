# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/1/20 21:56
# @author  : Mo
# @function: char similarity


import traceback
import time
import json
import sys
import os

path_sys = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path_sys)
# print(path_sys)

from char_similar.const_dict import dict_char_component, dict_char_fourangle
from char_similar.const_dict import dict_char_frequency, dict_char_number
from char_similar.const_dict import dict_char_pinyin, dict_char_stroke
from char_similar.const_dict import dict_char_struct, dict_char_order
from char_similar.const_dict import load_json, save_json


def sim_fourangle(char1, char2, code=4):
    """ 计算两汉字相似度, 通过四角码(只计算前4位)
    calculate similarity of two chars, by judge wether is the same fourangle
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.5
    """
    char1_f4 = dict_char_fourangle.get(char1, "")
    char2_f4 = dict_char_fourangle.get(char2, "")
    result = 0
    if char1_f4 and char2_f4:
        same_count = sum(1 for cf1, cf2 in zip(char1_f4[:code],
                           char2_f4[:code]) if cf1 == cf2)
        result = same_count / code
    return result

def sim_pinyin(char1, char2, code=4):
    """ 计算两汉字相似度, 通过两个字拼音(拼音/声母/韵母/声调)
    calculate similarity of two chars, by char pinyin
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.75
    """
    char1_pi = dict_char_pinyin.get(char1, [])
    char2_pi = dict_char_pinyin.get(char2, [])
    result = 0
    if char1_pi and char2_pi:
        same_count = sum(1 for cp1, cp2 in zip(char1_pi, char2_pi) if cp1 == cp2)
        result = same_count / code
    return result

def sim_component(char1, char2):
    """ 计算两汉字相似度, 通过偏旁部首
    calculate similarity of two chars, by judge wether is the same component
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: int, eg. 1 or 0
    """
    char1_component = dict_char_component.get(char1, "")
    char2_component = dict_char_component.get(char2, "")
    result = 0
    if char1_component and char1_component == char2_component:
        result = 1
    return result

def sim_frequency(char1, char2):
    """ 计算两汉字相似度, 通过两个字频log10的(1- 绝对值差/最大值)
    calculate similarity of two chars, by char frequency
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.75
    """
    char1_fr = dict_char_frequency.get(char1, 0)
    char2_fr = dict_char_frequency.get(char2, 0)
    result = 0
    if char1_fr and char2_fr:
        result = 1 - abs((char1_fr - char2_fr) / max(char1_fr, char2_fr))
    return result

def sim_number(char1, char2):
    """ 计算两汉字相似度, 通过两个字笔画数的(1- 绝对值差/最大值)
    calculate similarity of two chars, by char number of stroke
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.75
    """
    char1_nu = dict_char_number.get(char1, 0)
    char2_nu = dict_char_number.get(char2, 0)
    result = 0
    if char1_nu and char2_nu:
        result = 1 - abs((char1_nu - char2_nu) / max(char1_nu, char2_nu))
    return result

def sim_stroke(char1, char2):
    """ 计算两汉字相似度, 通过两个字拆字的(相同元素/所有元素)
    calculate similarity of two chars, by char count of stroke
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.75
    """
    char1_st = dict_char_stroke.get(char1, [])
    char2_st = dict_char_stroke.get(char2, [])
    result = 0
    if char1_st and char2_st:
        count_and = len(set(char1_st) & set(char2_st))
        count_union = len(set(char1_st) | set(char2_st))
        result = count_and / count_union
    return result

def sim_struct(char1, char2):
    """ 计算两汉字相似度, 通过两个字构造结构
    calculate similarity of two chars, by char struct
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: int, 0 or 1, eg. 1
    """
    char1_st = dict_char_struct.get(char1, "")
    char2_st = dict_char_struct.get(char2, "")
    result = 0
    if char1_st and char2_st and char1_st == char2_st:
        result = 1
    return result

def sim_order(char1, char2):
    """ 计算两汉字相似度, 通过两个字笔顺(相同元素/所有元素)
    calculate similarity of two chars, by char struct
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.6
    """
    char1_or = dict_char_order.get(char1, "")
    char2_or = dict_char_order.get(char2, "")
    result = 0
    if char1_or and char2_or:
        count_and = len(set(list(char1_or)) & set(list(char2_or)))
        count_union = len(set(list(char1_or)) | set(list(char2_or)))
        result = count_and / count_union
    return result

def sim_w2v(char1, char2):
    """ 计算两汉字相似度, 通过词向量
    calculate similarity of two chars, by char struct
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.6
    """
    import macropodus
    result = macropodus.sim(char1, char2, type_sim="cosine")
    return result


def cal_sim_by_shape(char1, char2, rounded=4, code=4, rate_fourangle=7,
    rate_component=2, rate_frequency=5, rate_number=6, rate_stroke=4,
    rate_struct=8, rate_order=3):
    """ 计算两汉字相似度(字形重点)
    calculate similarity of two chars, by char shape
    rate(text-char-similar): 造字结构 8 四角编码 7 笔画数 6 字频log10 5 拆字集合 4 笔画集合 3 偏旁部首 2
    rate(nlp-hanzi-similar): 造字结构 10 四角编码 8 拆字 6 偏旁部首 6 笔画数 2  拼音 1
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.6
    """
    # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
    score_fourangle = sim_fourangle(char1, char2, code=code)
    # 偏旁部首, 相同为1
    score_component = sim_component(char1, char2)
    # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
    score_frequency = sim_frequency(char1, char2)
    # 笔画数, 1-(差的绝对值/两数中的最大值)
    score_number = sim_number(char1, char2)
    # 拆字, 集合的与 / 集合的并
    score_stroke = sim_stroke(char1, char2)
    # 构造结构, 相同为1
    score_struct = sim_struct(char1, char2)
    # 笔顺(实际为最小的集合), 集合的与 / 集合的并
    score_order = sim_order(char1, char2)
    # 得分*权重
    result = score_fourangle * rate_fourangle + score_component * rate_component \
             + score_frequency * rate_frequency + score_number * rate_number \
             + score_stroke * rate_stroke + score_struct * rate_struct \
             + score_order * rate_order
    rate_all = rate_fourangle + rate_component + rate_frequency + rate_number\
               + rate_stroke + rate_struct + rate_order
    result = round(result/rate_all, rounded)
    return result


def cal_sim_by_pinyin(char1, char2, rounded=4, code=4, rate_fourangle=7,
    rate_component=2, rate_frequency=5, rate_number=6, rate_stroke=4,
    rate_struct=8, rate_order=3, rate_pinyin=35):
    """ 计算两汉字相似度(拼音重点)
    calculate similarity of two chars, by char shape
    rate(text-char-similar): 拼音 35 造字结构 8 四角编码 7 笔画数 6 字频log10 5 拆字集合 4 笔画集合 3 偏旁部首 2
    rate(nlp-hanzi-similar): 造字结构 10 四角编码 8 拆字 6 偏旁部首 6 笔画数 2  拼音 1
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.6
    """
    # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
    score_fourangle = sim_fourangle(char1, char2, code=code)
    # 拼音(code=4, 共4位), 统计四个数字中的相同数(拼音/声母/韵母/声调)/4
    score_pinyin = sim_pinyin(char1, char2, code=code)
    # 偏旁部首, 相同为1
    score_component = sim_component(char1, char2)
    # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
    score_frequency = sim_frequency(char1, char2)
    # 笔画数, 1-(差的绝对值/两数中的最大值)
    score_number = sim_number(char1, char2)
    # 拆字, 集合的与 / 集合的并
    score_stroke = sim_stroke(char1, char2)
    # 构造结构, 相同为1
    score_struct = sim_struct(char1, char2)
    # 笔顺(实际为最小的集合), 集合的与 / 集合的并
    score_order = sim_order(char1, char2)
    # 得分*权重
    result = score_fourangle * rate_fourangle + score_component * rate_component \
             + score_frequency * rate_frequency + score_number * rate_number \
             + score_stroke * rate_stroke + score_struct * rate_struct \
             + score_order * rate_order + score_pinyin * rate_pinyin
    rate_all = rate_fourangle + rate_component + rate_frequency + rate_number\
               + rate_stroke + rate_struct + rate_order + rate_pinyin
    result = round(result/rate_all, rounded)
    return result


def cal_sim_by_w2v(char1, char2, rounded=4, code=4, rate_fourangle=7,
    rate_component=2, rate_frequency=5, rate_number=6, rate_stroke=4,
    rate_struct=8, rate_order=3, rate_w2v=35):
    """ 计算两汉字相似度(字形重点)
    calculate similarity of two chars, by char shape
    rate(text-char-similar): 字义 35 造字结构 8 四角编码 7 笔画数 6 字频log10 5 拆字集合 4 笔画集合 3 偏旁部首 2
    rate(nlp-hanzi-similar): 造字结构 10 四角编码 8 拆字 6 偏旁部首 6 笔画数 2  拼音 1
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.6
    """
    # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
    score_fourangle = sim_fourangle(char1, char2, code=code)
    # 偏旁部首, 相同为1
    score_component = sim_component(char1, char2)
    # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
    score_frequency = sim_frequency(char1, char2)
    # 笔画数, 1-(差的绝对值/两数中的最大值)
    score_number = sim_number(char1, char2)
    # 拆字, 集合的与 / 集合的并
    score_stroke = sim_stroke(char1, char2)
    # 构造结构, 相同为1
    score_struct = sim_struct(char1, char2)
    # 笔顺(实际为最小的集合), 集合的与 / 集合的并
    score_order = sim_order(char1, char2)
    # 词向量, char-word2vec, cosine
    score_w2v = sim_w2v(char1, char2)
    # 得分*权重
    result = score_fourangle * rate_fourangle + score_component * rate_component \
             + score_frequency * rate_frequency + score_number * rate_number \
             + score_stroke * rate_stroke + score_struct * rate_struct \
             + score_order * rate_order + score_w2v * rate_w2v
    rate_all = rate_fourangle + rate_component + rate_frequency + rate_number\
               + rate_stroke + rate_struct + rate_order + rate_w2v
    result = round(result/rate_all, rounded)
    return result


def cal_sim_by_all(char1, char2, rounded=4, code=4, rate_fourangle=7,
    rate_component=2, rate_frequency=5, rate_number=6, rate_stroke=4,
    rate_struct=8, rate_order=3, rate_pinyin=35, rate_w2v=35):
    """ 计算两汉字相似度(字形-拼音-语义)
    calculate similarity of two chars, by char shape
    rate(text-char-similar): 字义 35 拼音 35 造字结构 8 四角编码 7 笔画数 6 字频log10 5 拆字集合 4 笔画集合 3 偏旁部首 2
    rate(nlp-hanzi-similar): 造字结构 10 四角编码 8 拆字 6 偏旁部首 6 笔画数 2  拼音 1
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
    Returns:
        result: float, 0-1, eg. 0.6
    """
    # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
    score_fourangle = sim_fourangle(char1, char2, code=code)
    # 拼音(code=4, 共4位), 统计四个数字中的相同数(拼音/声母/韵母/声调)/4
    score_pinyin = sim_pinyin(char1, char2, code=code)
    # 偏旁部首, 相同为1
    score_component = sim_component(char1, char2)
    # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
    score_frequency = sim_frequency(char1, char2)
    # 笔画数, 1-(差的绝对值/两数中的最大值)
    score_number = sim_number(char1, char2)
    # 拆字, 集合的与 / 集合的并
    score_stroke = sim_stroke(char1, char2)
    # 构造结构, 相同为1
    score_struct = sim_struct(char1, char2)
    # 笔顺(实际为最小的集合), 集合的与 / 集合的并
    score_order = sim_order(char1, char2)
    # 词向量, char-word2vec, cosine
    score_w2v = sim_w2v(char1, char2)
    # 得分*权重
    result = score_fourangle * rate_fourangle + score_component * rate_component \
             + score_frequency * rate_frequency + score_number * rate_number \
             + score_stroke * rate_stroke + score_struct * rate_struct \
             + score_order * rate_order + score_pinyin * rate_pinyin \
             + score_w2v * rate_w2v
    rate_all = rate_fourangle + rate_component + rate_frequency + rate_number\
               + rate_stroke + rate_struct + rate_order + rate_pinyin + rate_w2v
    result = round(result/rate_all, rounded)
    return result


def std_cal_sim(char1, char2, rounded=4, kind="shape"):
    """ 计算两汉字相似度(字形-拼音-语义)
    calculate similarity of two chars, by char shape
    rate-shape(text-char-similar): 造字结构 8 四角编码 7 笔画数 6 字频log10 5 拆字集合 4 笔画集合 3 偏旁部首 2
    rate-pinyin(text-char-similar): 拼音 35 造字结构 8 四角编码 7 笔画数 6 字频log10 5 拆字集合 4 笔画集合 3 偏旁部首 2
    rate-w2v(text-char-similar): 字义 35 造字结构 8 四角编码 7 笔画数 6 字频log10 5 拆字集合 4 笔画集合 3 偏旁部首 2
    rate-all(text-char-similar): 字义 35 拼音 35 造字结构 8 四角编码 7 笔画数 6 字频log10 5 拆字集合 4 笔画集合 3 偏旁部首 2
    rate(nlp-hanzi-similar): 造字结构 10 四角编码 8 拆字 6 偏旁部首 6 笔画数 2  拼音 1
    Args:
        char1: string, eg. "一"
        char2: string, eg. "而"
        rounded： int, eg. 4
        kind: string, eg. "shape" or "pinyin" or "w2v" or "all"
    Returns:
        result: float, 0-1, eg. 0.6
    """

    if kind.upper() == "PINYIN":
        result = cal_sim_by_pinyin(char1, char2, rounded)
    elif kind.upper() == "W2V":
        result = cal_sim_by_w2v(char1, char2, rounded)
    elif kind.upper() == "ALL":
        result = cal_sim_by_all(char1, char2, rounded)
    else:
        result = cal_sim_by_shape(char1, char2, rounded)
    return result


if __name__ == "__main__":
    myz = 0

    # "shape"-字形; "all"-汇总字形/词义/拼音; "w2v"-词义优先+字形; "pinyin"-拼音优先+字形
    kind = "shape"  # "all"  # "w2v"  # "pinyin"  # "shape"
    rounded = 4
    char1 = "我"
    char2 = "他"
    time_start = time.time()
    res = std_cal_sim(char1, char2, rounded=rounded, kind=kind)
    time_end = time.time()
    print(time_end-time_start)
    print(res)
    while True:
        try:
            print("请输入char1: ")
            char1 = input()
            print("请输入char2: ")
            char2 = input()
            res = std_cal_sim(char1, char2, rounded=rounded, kind=kind)
            print(res)
        except Exception as e:
            print(traceback.print_exc())


