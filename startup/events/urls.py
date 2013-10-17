from django.conf.urls import patterns, include, url
from events import views

urlpatterns = patterns('',
                       url(r'^$', views.view_events),
                       url(r'^filter/$', views.view_events_filter),
                       )
