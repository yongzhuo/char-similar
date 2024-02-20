# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/1/20 21:56
# @author  : Mo
# @function: multiprocess.pool.Pool


# from multiprocessing import Manager
# from multiprocessing import Pool
from multiprocess.pool import Pool
import traceback
import time
import json
import sys
import os

path_sys = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path_sys)
# print(path_sys)

from char_similar.char_similarity_std import sim_fourangle, sim_pinyin, sim_component
from char_similar.char_similarity_std import sim_frequency, sim_number, sim_stroke
from char_similar.char_similarity_std import sim_struct, sim_order, sim_w2v


def multi_cal_sim_by_shape(char1, char2, rounded=4, code=4, rate_fourangle=7,
    rate_component=2, rate_frequency=5, rate_number=6, rate_stroke=4,
    rate_struct=8, rate_order=3, processes=7):
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
    t1 = time.time()
    pool = Pool(processes=processes)
    result_list = list()
    result_list.append(pool.apply_async(sim_fourangle,
                                        (char1, char2, code)))
    result_list.append(pool.apply_async(sim_component,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_frequency,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_number,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_stroke,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_struct,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_order,
                                        (char1, char2)))
    pool.close()
    pool.join()
    pool.terminate()
    # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
    # 偏旁部首, 相同为1
    # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
    # 笔画数, 1-(差的绝对值/两数中的最大值)
    # 拆字, 集合的与 / 集合的并
    # 构造结构, 相同为1
    # 笔顺(实际为最小的集合), 集合的与 / 集合的并
    # 得分*权重
    score_list = []
    for result in result_list:
        score_i = result.get()
        score_list.append(score_i)
    t2 = time.time()
    time_cost = round(t2 - t1, 6)
    rate_list = [rate_fourangle, rate_component, rate_frequency, rate_number,
                 rate_stroke, rate_struct, rate_order]
    result = 0
    for score_i, rate_i in zip(score_list, rate_list):
        result += score_i * rate_i
    result = round(result / sum(rate_list), rounded)
    return result


def multi_cal_sim_by_pinyin(char1, char2, rounded=4, code=4, rate_fourangle=7,
    rate_component=2, rate_frequency=5, rate_number=6, rate_stroke=4,
    rate_struct=8, rate_order=3, rate_pinyin=35, processes=8, timeout=1):
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
    t1 = time.time()
    pool = Pool(processes=processes)
    result_list = list()
    result_list.append(pool.apply_async(sim_fourangle,
                                        (char1, char2, code)))
    result_list.append(pool.apply_async(sim_component,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_frequency,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_number,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_stroke,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_struct,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_order,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_pinyin,
                                        (char1, char2, code)))
    pool.close()
    pool.join()
    # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
    # 偏旁部首, 相同为1
    # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
    # 笔画数, 1-(差的绝对值/两数中的最大值)
    # 拆字, 集合的与 / 集合的并
    # 构造结构, 相同为1
    # 笔顺(实际为最小的集合), 集合的与 / 集合的并
    # 拼音(code=4, 共4位), 统计四个数字中的相同数(拼音/声母/韵母/声调)/4
    # 得分*权重
    score_list = []
    for result in result_list:
        score_i = result.get()
        score_list.append(score_i)
    t2 = time.time()
    time_cost = round(t2 - t1, 6)
    rate_list = [rate_fourangle, rate_component, rate_frequency, rate_number,
                 rate_stroke, rate_struct, rate_order, rate_pinyin]
    result = 0
    for score_i, rate_i in zip(score_list, rate_list):
        result += score_i * rate_i
    result = round(result / sum(rate_list), rounded)
    # pool.terminate()
    return result


def multi_cal_sim_by_w2v(char1, char2, rounded=4, code=4, rate_fourangle=7,
    rate_component=2, rate_frequency=5, rate_number=6, rate_stroke=4,
    rate_struct=8, rate_order=3, rate_w2v=35, processes=8, timeout=1):
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
    t1 = time.time()
    pool = Pool(processes=processes)
    result_list = list()
    result_list.append(pool.apply_async(sim_fourangle,
                                        (char1, char2, code)))
    result_list.append(pool.apply_async(sim_component,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_frequency,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_number,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_stroke,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_struct,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_order,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_w2v,
                                        (char1, char2)))
    pool.close()
    pool.join()
    # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
    # 偏旁部首, 相同为1
    # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
    # 笔画数, 1-(差的绝对值/两数中的最大值)
    # 拆字, 集合的与 / 集合的并
    # 构造结构, 相同为1
    # 笔顺(实际为最小的集合), 集合的与 / 集合的并
    # 词向量, char-word2vec, cosine
    # 得分*权重
    score_list = []
    for result in result_list:
        score_i = result.get()
        score_list.append(score_i)
    t2 = time.time()
    time_cost = round(t2 - t1, 6)
    rate_list = [rate_fourangle, rate_component, rate_frequency, rate_number,
                 rate_stroke, rate_struct, rate_order, rate_w2v]
    result = 0
    for score_i, rate_i in zip(score_list, rate_list):
        result += score_i * rate_i
    result = round(result / sum(rate_list), rounded)
    return result


def multi_cal_sim_by_all(char1, char2, rounded=4, code=4, rate_fourangle=7,
    rate_component=2, rate_frequency=5, rate_number=6, rate_stroke=4,
    rate_struct=8, rate_order=3, rate_pinyin=35, rate_w2v=35,
    processes=9, timeout=1):
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
    t1 = time.time()
    pool = Pool(processes=processes)
    result_list = list()
    result_list.append(pool.apply_async(sim_fourangle,
                                        (char1, char2, code)))
    result_list.append(pool.apply_async(sim_component,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_frequency,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_number,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_stroke,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_struct,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_order,
                                        (char1, char2)))
    result_list.append(pool.apply_async(sim_pinyin,
                                        (char1, char2, code)))
    result_list.append(pool.apply_async(sim_w2v,
                                        (char1, char2)))
    pool.close()
    pool.join()
    # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
    # 偏旁部首, 相同为1
    # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
    # 笔画数, 1-(差的绝对值/两数中的最大值)
    # 拆字, 集合的与 / 集合的并
    # 构造结构, 相同为1
    # 笔顺(实际为最小的集合), 集合的与 / 集合的并
    # 拼音(code=4, 共4位), 统计四个数字中的相同数(拼音/声母/韵母/声调)/4
    # 词向量, char-word2vec, cosine
    # 得分*权重
    score_list = []
    for result in result_list:
        score_i = result.get()
        score_list.append(score_i)
    t2 = time.time()
    time_cost = round(t2 - t1, 6)
    rate_list = [rate_fourangle, rate_component, rate_frequency, rate_number,
                 rate_stroke, rate_struct, rate_order, rate_pinyin, rate_w2v]
    result = 0
    for score_i, rate_i in zip(score_list, rate_list):
        result += score_i * rate_i
    result = round(result / sum(rate_list), rounded)
    return result


def multi_cal_sim(char1, char2, rounded=4, kind="shape"):
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
        result = multi_cal_sim_by_pinyin(char1, char2, rounded)
    elif kind.upper() == "W2V":
        result = multi_cal_sim_by_w2v(char1, char2, rounded)
    elif kind.upper() == "ALL":
        result = multi_cal_sim_by_all(char1, char2, rounded)
    else:
        result = multi_cal_sim_by_shape(char1, char2, rounded)
    return result


if __name__ == '__main__':
    myz = 0
    # "shape"-字形; "all"-汇总字形/词义/拼音; "w2v"-词义优先+字形; "pinyin"-拼音优先+字形
    kind = "shape"  # "all"  # "w2v"  # "pinyin"  # "shape"
    rounded = 4
    char1 = "我"
    char2 = "他"

    time_start = time.time()
    res = multi_cal_sim(char1, char2, rounded=rounded, kind=kind)
    time_end = time.time()
    print(time_end-time_start)
    print(res)
    while True:
        try:
            print("请输入char1: ")
            char1 = input()
            print("请输入char2: ")
            char2 = input()
            res = multi_cal_sim(char1, char2, rounded=rounded, kind=kind)
            print(res)
        except Exception as e:
            print(traceback.print_exc())


