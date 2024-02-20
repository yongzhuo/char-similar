# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/1/20 21:56
# @author  : Mo
# @function: path of char-similar


import sys
import os
path_root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(path_root)


# path of basic
path_char_component = os.path.join(path_root, "data/char_component.dict")
path_char_fourangle = os.path.join(path_root, "data/char_fourangle.dict")
path_char_frequency = os.path.join(path_root, "data/char_frequency.dict")
path_char_number = os.path.join(path_root, "data/char_number.dict")
path_char_pinyin = os.path.join(path_root, "data/char_pinyin.dict")
path_char_stroke = os.path.join(path_root, "data/char_stroke.dict")
path_char_struct = os.path.join(path_root, "data/char_struct.dict")
path_char_order = os.path.join(path_root, "data/char_order.dict")

