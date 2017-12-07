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
    model.next_check_point = next_check_point(model.last_checked_at, next_level)

    model.save()
    return model
