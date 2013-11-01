from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    #url(r'^(?P<event_id>\d+)/$', views.get_event_view),
    url(r'^create/$', views.create_event_view),
    url(r'^create_return/$', views.create_return_event_view),
    url(r'^set_vehicle/$', views.set_vehicle_view),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', views.monthly_events_view),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.daily_events_view),
    url(r'^json/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.daily_events_view_json),
    #url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.get_week_events_view),
    #url(r'^(?P<year>\d+)/(?P<week>\d+)/$', views.get_week_events_view),
)
