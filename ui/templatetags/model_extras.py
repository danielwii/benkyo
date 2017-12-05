# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.simple_tag
def count(var, **kwargs):
    return len(var)


@register.filter
def eq(var1, var2):
    return var1 == var2
