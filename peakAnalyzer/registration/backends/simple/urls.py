"""
URLconf for registration and activation, using django-registration's
one-step backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.simple.urls')),

This will also automatically set up the views in
``django.contrib.auth`` at sensible default locations.

If you'd like to customize the behavior (e.g., by passing extra
arguments to the various views) or split up the URLs, feel free to set
up your own URL patterns for these views instead.

"""


from django.conf.urls.defaults import *
#from django.views.generic.simple import direct_to_template
from django.views.generic import TemplateView

from registration.views import activate
from registration.views import register

class DirectTemplateView(TemplateView):
    extra_context = None
    def get_context_data(self, **kwargs):
        context = super(self.__class__, self).get_context_data(**kwargs)
        if self.extra_context is not None:
            for key, value in self.extra_context.items():
                if callable(value):
                    context[key] = value()
                else:
                    context[key] = value
        return context

urlpatterns = patterns('',
                       url(r'^register/$',
                           register,
                           {'backend': 'registration.backends.simple.SimpleBackend'},
                           name='registration_register'),
                       url(r'^register/closed/$',
                           DirectTemplateView.as_view(template_name='registration/registration_closed.html'),
              #             {'template': 'registration/registration_closed.html'},
                           name='registration_disallowed'),
                       (r'', include('registration.auth_urls')),
                       )
