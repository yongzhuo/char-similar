# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/1/20 21:56
# @author  : Mo
# @function: 线程池测试


import sys
import os

path_sys = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path_sys)
print(path_sys)


## 2.3 多线程使用
from char_similar import pool_cal_sim
# "all"(字形:拼音:字义=1:1:1)  # "w2v"(字形:字义=1:1)  # "pinyin"(字形:拼音=1:1)  # "shape"(字形=1)
kind = "shape"
rounded = 4  # 保留x位小数
char1 = "我"
char2 = "他"
res = pool_cal_sim(char1, char2, rounded=rounded, kind=kind)
print(res)
# output:
# 0.5821

