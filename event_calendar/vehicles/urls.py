__author__ = 'Marek Mackiewicz'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^(?P<vehicle_id>\d+)/$', views.get_vehicle_view),
    url(r'^create/$', views.create_vehicle_view),
    url(r'^update/(?P<vehicle_id>\d+)$', views.update_vehicle_view),
    url(r'^all/$', views.get_all_vehicles_view),
)