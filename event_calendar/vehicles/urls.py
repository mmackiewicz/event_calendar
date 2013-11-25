__author__ = 'Marek Mackiewicz'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^(?P<vehicle_id>\d+)/$', views.get_vehicle_view),
    url(r'^create/$', views.create_vehicle_view),
    url(r'^update/(?P<vehicle_id>\d+)/$', views.update_vehicle_view),
    url(r'^all/$', views.get_all_vehicles_view),
    url(r'^all_extended/$', views.get_vehicles_list_json),
    url(r'^create/validate/$', views.validate_vehicle_create),
    url(r'^update/validate/(?P<vehicle_id>\d+)/$', views.validate_vehicle_update),
)