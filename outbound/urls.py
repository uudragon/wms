from django.conf.urls import patterns, url

__author__ = 'pluto'


urlpatterns = patterns(
    'outbound.views',
    url(r'^split/$', 'split'),
    url(r'^shipment/save/$', 'save_shipment'),
    url(r'^shipment/check/$', 'check'),
    url(r'^shipments/check/$', 'batch_check'),
    url(r'^shipments/print/$', 'query_print_shipments'),
    url(r'^shipments/sync/$', 'sync_shipments'),
    url(r'^shipment/amount_setting/$', 'set_orders_amount'),
    url(r'^shipment/modify_by_orders/(.+)/$', 'modify_shipment_by_orderno'),
    url(r'^shipments/$', 'query_shipments'),
    url(r'^picking_orders/create/$', 'assemble_picking_orders'),
    url(r'^picking_orders/picking_completed/(.+)/$', 'picking_completed'),
    url(r'^picking_orders/picking/(.+)/$', 'picking'),
    url(r'^picking_orders/$', 'query_picking_orders_list'),
    url(r'^picking_orders/query_shipments/(.+)/$', 'query_shipments_by_picking_no'),
    url(r'^shipment/sent/$', 'sent'),
    url(r'^shipment/merge/$', 'merge_shipments'),
    url(r'^shipments/orders(.+)/$', 'query_by_ordersno'),
    url(r'^picking_orders/(.+)/$', 'query_single_picking_orders'),
    url(r'^request_express_info/$', 'request_express_info'),
    url(r'^shipment/(.+)/$', 'query_shipment'),
)