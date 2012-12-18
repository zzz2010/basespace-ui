from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('basespace.views',
	url(r'^$', 'createSession'),
	url(r'^(?P<session_id>\d+)/listFiles/$', 'listFiles'),
	url(r'^(?P<user_id>\d+)/demo/$', 'demo'),
)
