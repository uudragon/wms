from django.conf.urls import patterns, url

__author__ = 'pluto'


urlpatterns = patterns(
    'base_info.views',
    url(r'^goods_define/$', 'define_goods'),
    url(r'^product_define/$', 'define_product'),
    url(r'^query_goods/(.+)/$', 'query_goods'),
    url(r'^query_product/(.+)/$', 'query_product'),
    url(r'^query_goods_list/$', 'query_goods_list'),
    url(r'^query_product_list/$', 'query_product_list'),
    url(r'^warehouse/save/$', 'save_warehouse'),
    url(r'^warehouses/$', 'query_warehouse_list'),
    url(r'^warehouse/(.+)/$', 'query_warehouse'),
    url(r'^package/save/$', 'save_package'),
    url(r'^packages/agency/$', 'query_agency_package'),
    url(r'^packages/agency_orders/$', 'query_agency_orders_package'),
    url(r'^packages/site/$', 'query_site_package'),
    url(r'^package/(.+)/$', 'query_package'),
    url(r'^packages/$', 'query_packages'),
    url(r'^packages_all/$', 'query_packages_all'),
)