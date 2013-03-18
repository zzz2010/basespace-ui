"""
URLconf for registration and activation, using django-registration's
default backend.

If the default behavior of these views is acceptable to you, simply
use a line like this in your root URLconf to set up the default URLs
for registration::

    (r'^accounts/', include('registration.backends.default.urls')),

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
                       url(r'^activate/complete/$',
                          DirectTemplateView.as_view(template_name='registration/activation_complete.html'),
                           name='registration_activation_complete'),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_activate'),
                       url(r'^register/$',
                           register,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_register'),
                       url(r'^register/complete/$',
                           DirectTemplateView.as_view(template_name='registration/registration_complete.html'),
                          
                           name='registration_complete'),
                       url(r'^register/closed/$',
                           DirectTemplateView.as_view(template_name='registration/registration_closed.html'),
                           name='registration_disallowed'),
                       (r'', include('registration.auth_urls')),
                       )

#urlpatterns = patterns('',
#                       url(r'^activate/complete/$',
#                           direct_to_template,
#                           {'template': 'registration/activation_complete.html'},
#                           name='registration_activation_complete'),
#                       # Activation keys get matched by \w+ instead of the more specific
#                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
#                       # that way it can return a sensible "invalid key" message instead of a
#                       # confusing 404.
#                       url(r'^activate/(?P<activation_key>\w+)/$',
#                           activate,
#                           {'backend': 'registration.backends.default.DefaultBackend'},
#                           name='registration_activate'),
#                       url(r'^register/$',
#                           register,
#                           {'backend': 'registration.backends.default.DefaultBackend'},
#                           name='registration_register'),
#                       url(r'^register/complete/$',
#                           direct_to_template,
#                           {'template': 'registration/registration_complete.html'},
#                           name='registration_complete'),
#                       url(r'^register/closed/$',
#                           direct_to_template,
#                           {'template': 'registration/registration_closed.html'},
#                           name='registration_disallowed'),
#                       (r'', include('registration.auth_urls')),
#                       )

