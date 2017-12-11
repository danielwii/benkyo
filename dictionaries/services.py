# -*- coding: utf-8 -*-
from django.utils import timezone

from core.mem_curve import calc_ranks, next_check_point
from dictionaries import models


def learn_word(model: models.SelectedWord, choice: int):
    next_level, next_ranks = calc_ranks(model.ranks, choice, model.review_times == 0)

    model.review_times += 1
    model.mem_level = next_level
    model.ranks = next_ranks
    model.last_checked_at = timezone.now()

    if choice >= 3:
        # 记忆正确时检查待 reviews 次数
        if model.last_review_times_needed > 0:
            # 需要 review 时建立一个 1 分钟后的下一个检查点
            model.last_review_times_needed -= 1

            model.next_check_point = timezone.now() + timezone.timedelta(minutes=1)
        else:
            # 根据所达等级计算检查点
            model.next_check_point = next_check_point(model.last_checked_at, next_level)
    else:
        # 增加短期复习次数，增加一个 1 分钟后的检查点
        model.last_review_times_needed = 3 if model.last_review_times_needed > 2 \
            else model.last_review_times_needed + 1
        model.next_check_point = timezone.now() + timezone.timedelta(minutes=1)

    model.save()
    return model
