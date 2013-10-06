__author__ = 'Marek Mackiewicz'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^create/$', views.create_transport_view),
    url(r'^(?P<transport_id>\d+)/$', views.get_transport_view),
    url(r'^return/create/$', views.create_return_transport_view),
    url(r'^return/(?P<transport_id>\d+)/$', views.get_return_transport_view),

)