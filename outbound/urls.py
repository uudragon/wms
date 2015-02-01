from django.conf.urls import patterns, url

__author__ = 'pluto'


urlpatterns = patterns(
    'outbound.views',
    url(r'^split/$', 'split'),
    url(r'^shipment/save/$', 'save_shipment'),
    url(r'^shipment/amount_setting/$', 'set_orders_amount'),
    url(r'^shipments/$', 'query_shipments'),
    url(r'^shipment/(.+)/$', 'query_shipment'),
    url(r'^shipment/(.+)/check/$', 'check'),
    url(r'^shipment/(.+)/prepared/$', 'prepared'),
    url(r'^shipment/(.+)/picking/$', 'picking'),
    url(r'^shipment/(.+)/sent/$', 'sent'),
    url(r'^shipments/orders(.+)/$', 'query_by_ordersno'),
)