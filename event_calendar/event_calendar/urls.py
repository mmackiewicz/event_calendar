from django.conf.urls import patterns, include, url
import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'event_calendar.views.home', name='home'),
    # url(r'^event_calendar/', include('event_calendar.foo.urls')),
    url(r'^home/', views.home_view),
    url(r'^login/', views.login_view),
    url(r'^logout/', views.logout_view),
    url(r'^events/', include('events.urls')),
    url(r'^vehicles/', include('vehicles.urls')),
    url(r'^products/', include('products.urls')),
    url(r'^loads/', include('loads.urls')),
    url(r'^transports/', include('transports.urls')),
    url(r'^workers/', include('workers.urls')),
    url(r'^invoices/', include('invoices.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
