from django.conf.urls import patterns, include, url
from eventadmin import views

urlpatterns = patterns('',
                       url(r'^$', views.view_event_admin),
                       url(r'^add-event/$', views.view_add_event),
                       url(r'^edit-event/$', views.view_edit_event),
                       )
