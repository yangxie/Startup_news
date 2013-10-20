from django.conf.urls import patterns, include, url
from core.models import Event
from tastypie.api import Api
# from core.resources import EventResource
from core import views
from django.views.generic import TemplateView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
# admin.site.register(Event)

# Add tastypie resources.
# v1_api = Api(api_name='v1')
# v1_api.register(EventResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'startup.views.home', name='home'),
    # url(r'^startup/', include('startup.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', TemplateView.as_view(template_name="common/base.html")),
    url(r'^admin/', include(admin.site.urls)),
#    url(r'^api/', include(v1_api.urls)),
#    url(r'^index/', 'core.views.index_view'),
    url(r'^all_filter_options/', 'core.views.all_filter_options_view'),
    url(r'^signup/$', 'auth.views.signup'),
    url(r'^signup/confirm/$', 'auth.views.signup_confirm'),
    url(r'^login/$', 'auth.views.login_view'),
    url(r'^logout/$', 'auth.views.logout_view'),
#    url(r'^event-url/$', 'eventadmin.views.event_url_process_view'),
#    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
#    url(r'^$', views.HomeView.as_view()),
#    url(r'^$', 'core.views.home_view'),
#    url(r'^events/$', views.EventsView.as_view()),
#    url(r'^events/(?P<pk>\d+)/$', views.EventView.as_view()),
    url(r'^events/', include('events.urls')),
    url(r'^eventadmin/', include('eventadmin.urls')),
)
