from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^(?P<event_id>\d+)/$', views.get_event_view),
    url(r'^all/$', views.get_events_view),
    url(r'^create/', views.create_event_view),
    url(r'^create/json/', views.create_event_view),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', views.get_month_events_view),
    #url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.get_week_events_view),
    #url(r'^(?P<year>\d+)/(?P<week>\d+)/$', views.get_week_events_view),
)
