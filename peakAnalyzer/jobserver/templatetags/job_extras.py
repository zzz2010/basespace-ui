'''
Created on 2012-12-24

@author: zhangzhizhuo
'''
from django import template

register = template.Library()


@register.filter
def lookup(dict, key):    
    return dict[key]