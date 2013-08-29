from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('help.views',
    url(r'aboutus/$', 'aboutus'),
     url(r'usage/$', 'howtouse'),
     url(r'doc/$', 'helpDoc'),
     url(r'result/$', 'viewDemoResult'),
)
