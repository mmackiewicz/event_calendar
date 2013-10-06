__author__ = 'Marek Mackiewicz'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^create/$', views.create_invoice_view),
    url(r'^(?P<invoice_id>\d+)/$', views.get_invoice_view),
#    url(r'^all/$', views.get__view),
)