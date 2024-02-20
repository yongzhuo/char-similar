# char-similar
>>> 汉字字形/拼音/语义相似度(单字, 可用于数据增强, CSC错别字检测识别任务(构建混淆集))

# 一、安装
```
0. 注意事项
   默认不指定numpy版本(标准版numpy==1.22.4), 过高或者过低的版本可能不支持
   标准版本的依赖包详见 requirements-all.txt
   
1. 通过PyPI安装
   pip install char-similar
   使用镜像源, 如：
   pip install -i https://pypi.tuna.tsinghua.edu.cn/simple char-similar
```

# 二、使用方式

## 2.1 快速使用
```python3
from char_similar import std_cal_sim
char1 = "我"
char2 = "他"
res = std_cal_sim(char1, char2)
print(res)
# output:
# 0.5821
```

## 2.2 详细使用
```python3
from char_similar import std_cal_sim
# "all"(字形:拼音:字义=1:1:1)  # "w2v"(字形:字义=1:1)  # "pinyin"(字形:拼音=1:1)  # "shape"(字形=1)
kind = "shape"
rounded = 4  # 保留x位小数
char1 = "我"
char2 = "他"
res = std_cal_sim(char1, char2, rounded=rounded, kind=kind)
print(res)
# output:
# 0.5821
```


## 2.3 多线程使用
```python3
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
```


## 2.4 多进程使用(不建议, 实现得较慢)
```python3
if __name__ == '__main__':
    from char_similar import multi_cal_sim
    # "all"(字形:拼音:字义=1:1:1)  # "w2v"(字形:字义=1:1)  # "pinyin"(字形:拼音=1:1)  # "shape"(字形=1)
    kind = "shape"
    rounded = 4  # 保留x位小数
    char1 = "我"
    char2 = "他"
    res = multi_cal_sim(char1, char2, rounded=rounded, kind=kind)
    print(res)
    # output:
    # 0.5821
```

# 三、技术原理
```
char-similar最初的使用场景是计算两个汉字的字形相似度(构建csc混淆集), 后加入拼音相似度,字义相似度,字频相似度...详见源码.

# 四角码(code=4, 共5位), 统计四个数字中的相同数/4
# 偏旁部首, 相同为1
# 词频log10, 统计大规模语料macropodus中词频log10的 1-(差的绝对值/两数中的最大值)
# 笔画数, 1-(差的绝对值/两数中的最大值)
# 拆字, 集合的与 / 集合的并
# 构造结构, 相同为1
# 笔顺(实际为最小的集合), 集合的与 / 集合的并
# 拼音(code=4, 共4位), 统计四个数字中的相同数(拼音/声母/韵母/声调)/4
# 词向量, char-word2vec, cosine
```


# 四、参考(部分字典来源以下项目)
 - [https://github.com/contr4l/SimilarCharacter](https://github.com/contr4l/SimilarCharacter)
 - [https://github.com/houbb/nlp-hanzi-similar](https://github.com/houbb/nlp-hanzi-similar)
 - [https://github.com/mozillazg/python-pinyin](https://github.com/mozillazg/python-pinyin)
 - [https://github.com/CNMan/UnicodeCJK-WuBi](https://github.com/CNMan/UnicodeCJK-WuBi)
 - [https://github.com/yongzhuo/Macropodus](https://github.com/yongzhuo/Macropodus)
 - [https://github.com/kfcd/chaizi](https://github.com/kfcd/chaizi)
 


# Reference
For citing this work, you can refer to the present GitHub project. For example, with BibTeX:
```
@misc{Macropodus,
    howpublished = {https://github.com/yongzhuo/char-similar},
    title = {char-similar},
    author = {Yongzhuo Mo},
    publisher = {GitHub},
    year = {2024}
}
```

