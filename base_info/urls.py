from django.conf.urls import patterns, url

__author__ = 'pluto'


urlpatterns = patterns(
    'base_info.views',
    url(r'^goods_define/$', 'define_goods'),
    url(r'^product_define/$', 'define_product'),
    url(r'^query_goods/(.+)/$', 'query_goods'),
    url(r'^query_product/(.+)/$', 'query_product'),
)