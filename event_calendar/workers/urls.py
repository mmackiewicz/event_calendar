__author__ = 'Marek Mackiewicz'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^(?P<worker_id>\d+)/$', views.get_worker_view),
    url(r'^create/$', views.create_worker_view),
    url(r'^update/(?P<worker_id>\d+)/$', views.update_worker_view),
    url(r'^delete/(?P<worker_id>\d+)/$', views.delete_worker_view),
    url(r'^create/validate/$', views.validate_worker_create),
    url(r'^update/validate/(?P<worker_id>\d+)/$', views.validate_worker_update),
    url(r'^all/$', views.get_all_workers_view),
)