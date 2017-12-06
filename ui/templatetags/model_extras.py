# -*- coding: utf-8 -*-
from django import template
from django.utils.html import format_html

from core.utils import phonetic_wrapper
from dictionaries import models

register = template.Library()


@register.simple_tag
def count(var, **kwargs):
    return len(var)


@register.simple_tag
def characteristic(var):
    return models.CHARACTERISTIC_CHOICES.__getitem__(int(var))[1]


@register.filter
def eq(var1, var2):
    return var1 == var2

@register.simple_tag
def phonetic(model):
    wrapper = model.kanji
    try:
        wrapper = phonetic_wrapper(model.kana, model.kanji, model.marking)
    except Exception as e:
        print(e)
    print(wrapper)
    return format_html('<div class="phonetic-words">{}</div>', format_html(wrapper))
