__author__ = 'Marek Mackiewicz'

from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^create/$', views.create_product_view),
    url(r'^update/(?P<product_id>\d+)/$', views.update_product_view),
    url(r'^(?P<product_id>\d+)/$', views.get_product_view),
    url(r'^all/$', views.get_all_products_view),
    url(r'^create/validate/$', views.validate_product_create),
    url(r'^update/validate/(?P<product_id>\d+)/$', views.validate_product_update),
)