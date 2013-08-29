from django.conf.urls import patterns, include, url
from peakAnalyzer import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('help.views',
    url(r'aboutus/$', 'aboutus'),
     url(r'usage/$', 'howtouse'),
     url(r'doc/$', 'helpDoc'),
     url(r'result/$','jobserver_regular.views.viewDemoResult'),
)
