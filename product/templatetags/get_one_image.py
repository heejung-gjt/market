# -*- coding: utf-8 -*-

from django import template
import re

from product.models import Article

register = template.Library()

@register.filter
def get_one_image(photo):
    photo =  photo.all()[0].image
    
    return photo
