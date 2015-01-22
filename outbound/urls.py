from django.conf.urls import patterns, url

__author__ = 'pluto'


urlpatterns = patterns(
    'outbound.views',
    url(r'^(.+)/split/$', 'split'),
    url(r'^(.+)/shipment/save/$', 'save_shipment'),
    url(r'^(.+)/shipments/$', 'query_shipments'),
    url(r'^(.+)/shipment/(.+)/$', 'query_shipment'),
)