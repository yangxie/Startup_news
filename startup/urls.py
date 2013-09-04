from django.conf.urls import patterns, include, url
from core.models import Event
from tastypie.api import Api
from core.resources import EventResource

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
admin.site.register(Event)

# Add tastypie resources.
v1_api = Api(api_name='v1')
v1_api.register(EventResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'startup.views.home', name='home'),
    # url(r'^startup/', include('startup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^index/', 'core.views.index_view'),
)


