# -*- coding: utf-8 -*-

# --------------------------------
# 记忆核心
# [[短期记忆]]（针对于不熟悉的单词）
#   :: 应用于初次记忆且不熟悉的单词
#   0   -> 5  min   : [ 0 ~ 10)
#   1   -> 30 min   : [10 ~ 20)
#   2   -> 9  hour  : [20 ~ 30)
# [[长期记忆]]
#   0,2 -> 1  day   : [30 ~ 45)
#   3   -> 2  day   : [45 ~ 60)
#   4   -> 4  day   : [60 ~ 75)
#   5   -> 7  day   : [75 ~ 90)
#   6   -> 15 day   : [90 ~
# --------------------------------

import math


def calc_ranks(ranks: int, choice: int, first: bool = False) -> tuple:
    """
    计算所处阶段及记忆程度
    :param ranks:
        当前程度
    :param choice:
        选择 = 阶段:记忆程度(符号表示需要计算)
        -> 0 = 0:  0 FIRST            完全不认识
        -> 1 = _: -5           ALWAYS 不记得
        -> 2 = 2:  0 FIRST(40) ALWAYS 模糊
        -> 3 = _: +5           ALWAYS 记得
        -> 4 = 3: 50 FIRST            熟悉
    :param first:
        是否是第一次
    :return:
        所处阶段, 记忆程度
    """
    if choice not in (0, 1, 2, 3, 4):
        raise ValueError("choice must be in 0,1,2,3,4")

    if first and choice not in (0, 2, 4):
        raise ValueError("choice must be in 0,2,4 while it's the first")

    if not first and choice not in (1, 2, 3):
        raise ValueError("choice must be in 1,2,3 while not the first")

    if first:
        _ranks = {
            0: lambda x: 0,
            2: lambda x: 40,
            4: lambda x: 50,
        }[choice](ranks)
    else:
        _ranks = {
            1: lambda x: x - 5,
            2: lambda x: x,
            3: lambda x: x + 5,
        }[choice](ranks)

    if _ranks < 0:
        _level = 0
    elif _ranks < 30:
        _level = int(_ranks / 10)
    else:
        _level = math.floor(_ranks / 15)
    return _level, _ranks
