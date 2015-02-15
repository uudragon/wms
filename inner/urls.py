from django.conf.urls import patterns, url

__author__ = 'pluto'


urlpatterns = patterns(
    'inner.views',
    url(r'^(.+)/records/$', 'query_records'),
    url(r'^(.+)/goods/$', 'query_goods'),
    url(r'^(.+)/products/$', 'query_products'),
    url(r'^(.+)/picking/$', 'picking'),
    url(r'^(.+)/picking_statistic', 'picking_statistic'),
)