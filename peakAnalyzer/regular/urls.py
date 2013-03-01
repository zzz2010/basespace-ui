'''
Created on Feb 20, 2013

@author: soke may
'''
from django.conf.urls import *

urlpatterns = patterns('regular.views',
    url(r'^submitJob/$', 'submitJob'),
    url(r'^listUploadedFiles/$', 'listUploadedFiles'),
    url(r'^uploadFiles/$', 'uploadFiles'),
    url(r'^listProject/$', 'listProject'),
    url(r'^jobManagement/$', 'jobManagement'),
    url(r'^hello', 'hello'),
)