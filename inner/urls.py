from django.conf.urls import patterns, url

__author__ = 'pluto'


urlpatterns = patterns(
    'inner.views',
    url(r'^storage_records/$', 'query_storage_records'),
)