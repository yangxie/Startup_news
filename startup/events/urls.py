from django.conf.urls import patterns, include, url
from events import views

urlpatterns = patterns('',
                       url(r'^$', views.view_events),
                       url(r'^filter/$', views.view_events_filter),
                       url(r'^delete/(?P<event_id>\d+)/$',
                           views.view_delete_event),
                       )
