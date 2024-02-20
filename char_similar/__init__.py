# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/1/20 21:56
# @author  : Mo
# @function:


# macropodus
from char_similar.char_similarity_class_pool import pool_cal_sim
from char_similar.char_similarity_multi import multi_cal_sim
from char_similar.char_similarity_std import std_cal_sim
from char_similar.version import __version__  # 版本

# 机械分词
multi_cal_sim = multi_cal_sim  # 多进程(多次重复加载Pool, 很慢)
pool_cal_sim = pool_cal_sim  # 多线程(线程池, 比较快, concurrent.futures.ThreadPoolExecutor)
std_cal_sim = std_cal_sim  # 标准串行(串行, 很快)
