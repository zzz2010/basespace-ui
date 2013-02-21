'''
Created on 2012-12-24

@author: zhangzhizhuo
'''
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('jobserver.views',
    url(r'^(?P<user_id>\d+)/listjob/$', 'listjob'),
     url(r'^(?P<job_id>\d+)/viewresult/$', 'viewresult'),
)
