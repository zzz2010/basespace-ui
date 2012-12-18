'''
Created on Sep 15, 2012

@author: carl
'''
import pgsadmin.settings, os

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    
