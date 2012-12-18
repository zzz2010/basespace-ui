from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('basespace.views',
	url(r'^$', 'createSession'),
	url(r'^(?P<session_id>\d+)/listFiles/$', 'listFiles'),
	url(r'^(?P<session_id>\d+)/(?P<ar_id>\d+)/listarFiles/$', 'listAppResultFiles'),
	url(r'^(?P<session_id>\d+)/(?P<sa_id>\d+)/listsaFiles/$', 'listSampleFiles'),
	url(r'^(?P<session_id>\d+)/listFolders/$', 'listFolders'),
	url(r'^(?P<user_id>\d+)/demo/$', 'demo'),
)
