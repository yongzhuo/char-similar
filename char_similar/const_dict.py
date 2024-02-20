# !/usr/bin/python
# -*- coding: utf-8 -*-
# @time    : 2024/1/20 21:56
# @author  : Mo
# @function: 偏旁部首/四角编码/字频log10/笔画数/拼音4/拆字/构造


from tqdm import tqdm
import traceback
import logging
import json
import os

from char_similar.conf.path_config import path_char_component, path_char_fourangle
from char_similar.conf.path_config import path_char_frequency, path_char_number
from char_similar.conf.path_config import path_char_pinyin, path_char_stroke
from char_similar.conf.path_config import path_char_struct, path_char_order


def txt_write(lines, path, model="w", encoding="utf-8"):
    """
    Write Line of list to file
    Args:
        lines: lines of list<str> which need save
        path: path of save file, such as "txt"
        model: type of write, such as "w", "a+"
        encoding: type of encoding, such as "utf-8", "gbk"
    """

    try:
        file = open(path, model, encoding=encoding)
        file.writelines(lines)
        file.close()
    except Exception as e:
        logging.info(str(e))

def txt_read(path, encoding="utf-8"):
    """
    Read Line of list form file
    Args:
        path: path of save file, such as "txt"
        encoding: type of encoding, such as "utf-8", "gbk"
    Returns:
        dict of word2vec, eg. {"macadam":[...]}
    """

    lines = []
    try:
        file = open(path, "r", encoding=encoding)
        lines = file.readlines()
        file.close()
    except Exception as e:
        logging.info(str(e))
    finally:
        return lines

def save_json(jsons, json_path, indent=4):
    """
        保存json
    Args:
        path[String]:, path of file of save, eg. "corpus/xuexiqiangguo.lib"
        jsons[Json]: json of input data, eg. [{"桂林": 132}]
        indent[int]: pretty-printed with that indent level, eg. 4
    Returns:
        None
    """
    with open(json_path, "w", encoding="utf-8") as fj:
        fj.write(json.dumps(jsons, ensure_ascii=False, indent=indent))
    fj.close()

def load_json(path, parse_int=None):
    """
        加载json
    Args:
        path_file[String]:, path of file of save, eg. "corpus/xuexiqiangguo.lib"
        parse_int[Boolean]: equivalent to int(num_str), eg. True or False
    Returns:
        data[Any]
    """
    with open(path, mode="r", encoding="utf-8") as fj:
        model_json = json.load(fj, parse_int=parse_int)
    return model_json


# 加载字典
dict_char_component = load_json(path_char_component)
dict_char_fourangle = load_json(path_char_fourangle)
dict_char_frequency = load_json(path_char_frequency)
dict_char_number = load_json(path_char_number)
dict_char_pinyin = load_json(path_char_pinyin)
dict_char_stroke = load_json(path_char_stroke)
dict_char_struct = load_json(path_char_struct)
dict_char_order = load_json(path_char_order)

