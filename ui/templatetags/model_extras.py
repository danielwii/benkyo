# -*- coding: utf-8 -*-
from django import template

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
