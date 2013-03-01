#from django.conf.urls import patterns, include, url
from django.conf.urls import *

#from django_consultants.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('basespace.views',
	url(r'^login/$', 'loginUser'),
	url(r'^$', 'createSession'),
	url(r'^(?P<session_id>\d+)/submitJob/$', 'submitJob'),
	url(r'^(?P<session_id>\d+)/listFiles/$', 'listFiles'),
	url(r'^(?P<session_id>\d+)/(?P<ar_id>\d+)/listAppResultFiles/$', 'listAppResultFiles'),
	url(r'^(?P<session_id>\d+)/(?P<sa_id>\d+)/listSampleFiles/$', 'listSampleFiles'),
	url(r'^(?P<session_id>\d+)/listUploadedFiles/$', 'listUploadedFiles'),
	url(r'^(?P<session_id>\d+)/uploadFiles/$', 'uploadFiles'),
	url(r'^(?P<session_id>\d+)/listProject/$', 'listProject'),
	url(r'^(?P<session_id>\d+)/jobManagement/$', 'jobManagement'),
	url(r'^(?P<user_id>\d+)/demo/$', 'demo'),
	url(r'^logout/$', 'logoutUser'),

)
