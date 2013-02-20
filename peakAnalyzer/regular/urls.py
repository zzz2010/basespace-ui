'''
Created on Feb 20, 2013

@author: soke may
'''
from django.conf.urls import *

urlpatterns = patterns('regular.views',
    url(r'^login/$', 'loginUser'),
    url(r'^submitJob/$', 'submitJob'),
    url(r'^listFiles/$', 'listFiles'),
    url(r'^listUploadedFiles/$', 'listUploadedFiles'),
    url(r'^uploadFiles/$', 'uploadFiles'),
    url(r'^listProject/$', 'listProject'),
   # url(r'^logout/$', 'logoutUser'),
    url(r'^hello', 'hello'),
)