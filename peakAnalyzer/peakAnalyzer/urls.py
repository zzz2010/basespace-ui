from django.conf.urls import patterns, include, url
from peakAnalyzer import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'peakAnalyzer.views.home', name='home'),
    # url(r'^peakAnalyzer/', include('peakAnalyzer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

     url(r'^basespace/', include('basespace.urls')),
     url(r'^jobserver/', include('jobserver.urls')),
    # Uncomment the next line to enable the admin:
     
     url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$', 'django.views.static.serve',  
         {'document_root':     settings.STATIC_ROOT}),
          (r'^userdata/(?P<path>.*)$', 'django.views.static.serve',  
         {'document_root':     settings.MEDIA_ROOT}),
    )