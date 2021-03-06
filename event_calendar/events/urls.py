from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    #url(r'^(?P<event_id>\d+)/$', views.get_event_view),
    url(r'^create/$', views.create_event_view),
    url(r'^edit/(?P<event_id>\d+)/$', views.edit_event_view),
    url(r'^edit_return/(?P<event_id>\d+)/$', views.edit_return_event_view),
    url(r'^create_return/$', views.create_return_event_view),
    url(r'^set_vehicle/$', views.set_vehicle_view),
    url(r'^set_date/$', views.set_event_date),
    url(r'^return/set_date/$', views.set_return_event_date),
    url(r'^(?P<year>\d+)/(?P<month>\d+)/$', views.monthly_events_view),
    url(r'^return/(?P<year>\d+)/(?P<month>\d+)/$', views.monthly_return_events_view),
    #url(r'^(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.daily_events_view),
    url(r'^json/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.daily_events_view_json),
    #url(r'^return/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.daily_return_events_view),
    url(r'^return/json/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/$', views.daily_return_events_view_json),
    url(r'^cancel/$', views.cancel_event),
    url(r'^return/cancel/$', views.cancel_return_event),
)
