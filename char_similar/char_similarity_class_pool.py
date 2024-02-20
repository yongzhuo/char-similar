# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/1/20 21:40
# @author  : Mo
# @function: concurrent.futures.ThreadPoolExecutor


from concurrent.futures import ThreadPoolExecutor as Pool
import concurrent
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


class PoolCalSimByShape:
    def __init__(self, processes=7):
        self.executor = Pool(max_workers=processes)

    def pool_cal_sim_by_shape(self, char1, char2, rounded=4, code=4, rate_fourangle=7,
                              rate_component=2, rate_frequency=5, rate_number=6,
                              rate_stroke=4, rate_struct=8, rate_order=3, timeout=1):
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
        future_1 = self.executor.submit(lambda p: sim_fourangle(*p),
                                   (char1, char2, code))
        future_2 = self.executor.submit(lambda p: sim_component(*p),
                                   (char1, char2))
        future_3 = self.executor.submit(lambda p: sim_frequency(*p),
                                   (char1, char2))
        future_4 = self.executor.submit(lambda p: sim_number(*p),
                                   (char1, char2))
        future_5 = self.executor.submit(lambda p: sim_stroke(*p),
                                   (char1, char2))
        future_6 = self.executor.submit(lambda p: sim_struct(*p),
                                   (char1, char2))
        future_7 = self.executor.submit(lambda p: sim_order(*p),
                                   (char1, char2))
        concurrent.futures.wait([future_1, future_2, future_3, future_4,
                                 future_5, future_6, future_7], timeout=timeout)
        # 获取两个服务的返回值
        score_fourangle = future_1.result()
        score_component = future_2.result()
        score_frequency = future_3.result()
        score_number = future_4.result()
        score_stroke = future_5.result()
        score_struct = future_6.result()
        score_order = future_7.result()
        # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
        # 偏旁部首, 相同为1
        # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
        # 笔画数, 1-(差的绝对值/两数中的最大值)
        # 拆字, 集合的与 / 集合的并
        # 构造结构, 相同为1
        # 笔顺(实际为最小的集合), 集合的与 / 集合的并
        # 得分*权重
        result = score_fourangle * rate_fourangle + score_component * rate_component \
                 + score_frequency * rate_frequency + score_number * rate_number \
                 + score_stroke * rate_stroke + score_struct * rate_struct \
                 + score_order * rate_order
        rate_all = rate_fourangle + rate_component + rate_frequency + rate_number \
                   + rate_stroke + rate_struct + rate_order
        result = round(result / rate_all, rounded)
        return result


class PoolCalSimByPinyin:
    def __init__(self, processes=8):
        self.executor = Pool(max_workers=processes)

    def pool_cal_sim_by_pinyin(self, char1, char2, rounded=4, code=4, rate_fourangle=7,
        rate_component=2, rate_frequency=5, rate_number=6, rate_stroke=4,
        rate_struct=8, rate_order=3, rate_pinyin=35, timeout=1):
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
        future_1 = self.executor.submit(lambda p: sim_fourangle(*p),
                                          (char1, char2, code))
        future_2 = self.executor.submit(lambda p: sim_component(*p),
                                          (char1, char2))
        future_3 = self.executor.submit(lambda p: sim_frequency(*p),
                                          (char1, char2))
        future_4 = self.executor.submit(lambda p: sim_number(*p),
                                       (char1, char2))
        future_5 = self.executor.submit(lambda p: sim_stroke(*p),
                                       (char1, char2))
        future_6 = self.executor.submit(lambda p: sim_struct(*p),
                                       (char1, char2))
        future_7 = self.executor.submit(lambda p: sim_order(*p),
                                      (char1, char2))
        future_8 = self.executor.submit(lambda p: sim_pinyin(*p),
                                   (char1, char2, code))

        concurrent.futures.wait([future_1, future_2, future_3, future_4,
                                 future_5, future_6, future_7, future_8],
                                timeout=timeout)
        # 获取两个服务的返回值
        score_fourangle = future_1.result()
        score_component = future_2.result()
        score_frequency = future_3.result()
        score_number = future_4.result()
        score_stroke = future_5.result()
        score_struct = future_6.result()
        score_order = future_7.result()
        score_pinyin = future_8.result()
        # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
        # 偏旁部首, 相同为1
        # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
        # 笔画数, 1-(差的绝对值/两数中的最大值)
        # 拆字, 集合的与 / 集合的并
        # 构造结构, 相同为1
        # 笔顺(实际为最小的集合), 集合的与 / 集合的并
        # 拼音(code=4, 共4位), 统计四个数字中的相同数(拼音/声母/韵母/声调)/4
        # 得分*权重
        result = score_fourangle * rate_fourangle + score_component * rate_component \
                 + score_frequency * rate_frequency + score_number * rate_number \
                 + score_stroke * rate_stroke + score_struct * rate_struct \
                 + score_order * rate_order + score_pinyin * rate_pinyin
        rate_all = rate_fourangle + rate_component + rate_frequency + rate_number\
                   + rate_stroke + rate_struct + rate_order + rate_pinyin
        result = round(result/rate_all, rounded)
        return result


class PoolCalSimByW2v:
    def __init__(self, processes=8):
        self.executor = Pool(max_workers=processes)

    def pool_cal_sim_by_w2v(self, char1, char2, rounded=4, code=4, rate_fourangle=7,
        rate_component=2, rate_frequency=5, rate_number=6, rate_stroke=4,
        rate_struct=8, rate_order=3, rate_w2v=35, timeout=1):
        """ 计算两汉字相似度(向量重点)
        calculate similarity of two chars, by char shape
        rate(text-char-similar): 字义 35 造字结构 8 四角编码 7 笔画数 6 字频log10 5 拆字集合 4 笔画集合 3 偏旁部首 2
        rate(nlp-hanzi-similar): 造字结构 10 四角编码 8 拆字 6 偏旁部首 6 笔画数 2  拼音 1
        Args:
            char1: string, eg. "一"
            char2: string, eg. "而"
        Returns:
            result: float, 0-1, eg. 0.6
        """
        future_1 = self.executor.submit(lambda p: sim_fourangle(*p),
                                          (char1, char2, code))
        future_2 = self.executor.submit(lambda p: sim_component(*p),
                                          (char1, char2))
        future_3 = self.executor.submit(lambda p: sim_frequency(*p),
                                          (char1, char2))
        future_4 = self.executor.submit(lambda p: sim_number(*p),
                                       (char1, char2))
        future_5 = self.executor.submit(lambda p: sim_stroke(*p),
                                       (char1, char2))
        future_6 = self.executor.submit(lambda p: sim_struct(*p),
                                       (char1, char2))
        future_7 = self.executor.submit(lambda p: sim_order(*p),
                                      (char1, char2))
        future_8 = self.executor.submit(lambda p: sim_w2v(*p),
                                   (char1, char2))

        concurrent.futures.wait([future_1, future_2, future_3, future_4,
                                 future_5, future_6, future_7, future_8],
                                timeout=timeout)
        # 获取两个服务的返回值
        score_fourangle = future_1.result()
        score_component = future_2.result()
        score_frequency = future_3.result()
        score_number = future_4.result()
        score_stroke = future_5.result()
        score_struct = future_6.result()
        score_order = future_7.result()
        score_w2v = future_8.result()
        # 四角码(code=4, 共5位), 统计四个数字中的相同数/4
        # 偏旁部首, 相同为1
        # 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
        # 笔画数, 1-(差的绝对值/两数中的最大值)
        # 拆字, 集合的与 / 集合的并
        # 构造结构, 相同为1
        # 笔顺(实际为最小的集合), 集合的与 / 集合的并
        # 词向量, char-word2vec, cosine
        # 得分*权重
        result = score_fourangle * rate_fourangle + score_component * rate_component \
                 + score_frequency * rate_frequency + score_number * rate_number \
                 + score_stroke * rate_stroke + score_struct * rate_struct \
                 + score_order * rate_order + score_w2v * rate_w2v
        rate_all = rate_fourangle + rate_component + rate_frequency + rate_number\
                   + rate_stroke + rate_struct + rate_order + rate_w2v
        result = round(result/rate_all, rounded)
        return result


class PoolCalSimByAll:
    def __init__(self, processes=9):
        self.executor = Pool(max_workers=processes)

    def pool_cal_sim_by_all(self, char1, char2, rounded=4, code=4, rate_fourangle=7,
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
        future_1 = self.executor.submit(lambda p: sim_fourangle(*p),
                                   (char1, char2, code))
        future_2 = self.executor.submit(lambda p: sim_component(*p),
                                   (char1, char2))
        future_3 = self.executor.submit(lambda p: sim_frequency(*p),
                                   (char1, char2))
        future_4 = self.executor.submit(lambda p: sim_number(*p),
                                   (char1, char2))
        future_5 = self.executor.submit(lambda p: sim_stroke(*p),
                                   (char1, char2))
        future_6 = self.executor.submit(lambda p: sim_struct(*p),
                                   (char1, char2))
        future_7 = self.executor.submit(lambda p: sim_order(*p),
                                   (char1, char2))
        future_8 = self.executor.submit(lambda p: sim_pinyin(*p),
                                   (char1, char2, code))
        future_9 = self.executor.submit(lambda p: sim_w2v(*p),
                                   (char1, char2))
        concurrent.futures.wait([future_1, future_2, future_3, future_4,
                                 future_5, future_6, future_7, future_8, future_9],
                                timeout=timeout)
        # 获取两个服务的返回值
        score_fourangle = future_1.result()
        score_component = future_2.result()
        score_frequency = future_3.result()
        score_number = future_4.result()
        score_stroke = future_5.result()
        score_struct = future_6.result()
        score_order = future_7.result()
        score_pinyin = future_8.result()
        score_w2v = future_8.result()
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
        result = score_fourangle * rate_fourangle + score_component * rate_component \
                 + score_frequency * rate_frequency + score_number * rate_number \
                 + score_stroke * rate_stroke + score_struct * rate_struct \
                 + score_order * rate_order + score_pinyin * rate_pinyin + score_w2v * rate_w2v
        rate_all = rate_fourangle + rate_component + rate_frequency + rate_number \
                   + rate_stroke + rate_struct + rate_order + rate_pinyin + rate_w2v
        result = round(result / rate_all, rounded)
        return result


def pool_cal_sim(char1, char2, rounded=4, kind="shape"):
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
        result = PoolCalSimByPinyin_1.pool_cal_sim_by_pinyin(char1, char2, rounded)
    elif kind.upper() == "W2V":
        result = PoolCalSimByW2v_1.pool_cal_sim_by_w2v(char1, char2, rounded)
    elif kind.upper() == "ALL":
        result = PoolCalSimByAll_1.pool_cal_sim_by_all(char1, char2, rounded)
    else:
        # result = pool_cal_sim_by_shape(char1, char2, rounded)
        result = PoolCalSimByShape_1.pool_cal_sim_by_shape(char1, char2, rounded)
    return result


# 初始化类class, 主要是Pool进程池
PoolCalSimByPinyin_1 = PoolCalSimByPinyin()
PoolCalSimByShape_1 = PoolCalSimByShape()
PoolCalSimByW2v_1 = PoolCalSimByW2v()
PoolCalSimByAll_1 = PoolCalSimByAll()


if __name__ == '__main__':
    myz = 0
    # "shape"-字形; "all"-汇总字形/词义/拼音; "w2v"-词义优先+字形; "pinyin"-拼音优先+字形
    kind = "shape"  # "all"  # "w2v"  # "pinyin"  # "shape"
    rounded = 4
    char1 = "我"
    char2 = "他"

    time_start = time.time()
    res = pool_cal_sim(char1, char2, rounded=rounded, kind=kind)
    time_end = time.time()
    print(time_end-time_start)
    print(res)
    while True:
        try:
            print("请输入char1: ")
            char1 = input()
            print("请输入char2: ")
            char2 = input()
            res = pool_cal_sim(char1, char2, rounded=rounded, kind=kind)
            print(res)
        except Exception as e:
            print(traceback.print_exc())


