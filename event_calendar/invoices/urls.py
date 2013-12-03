__author__ = 'Marek Mackiewicz'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^create/(?P<transport_id>\d+)/$', views.create_invoice_view),
    url(r'^(?P<invoice_id>\d+)/$', views.get_invoice_view),
    url(r'^list/(?P<year>\d+)/(?P<month>\d+)/$', views.get_invoices_list),
    url(r'^mark_paid/(?P<invoice_id>\d+)/$', views.mark_as_paid),
    url(r'^outdated/$', views.outdated_invoices_view),
    url(r'^edit/(?P<invoice_id>\d+)/$', views.edit_invoice_view),
    url(r'^create/validate/$', views.validate_create_invoice),
    url(r'^update/validate/(?P<invoice_id>\d+)/$', views.validate_update_invoice),
)