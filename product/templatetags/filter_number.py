# -*- coding: utf-8 -*-

from django import template
import re

register = template.Library()

@register.filter
def filter_numbers(value):
    value = value.__dict__['address']
    hangul = re.compile('[^ ㄱ-ㅣ가-힣]+')
    result = hangul.sub('',value).strip()
    return result
