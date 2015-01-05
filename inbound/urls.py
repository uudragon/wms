from django.conf.urls import patterns, url

__author__ = 'pluto'


urlpatterns = patterns(
    'inbound.views',
    url(r'^receipt/create/$', 'create_receipt'),
    url(r'^receipt/(.+)/cancel/$', 'cancel_receipt'),
    url(r'^putin/$', 'put_in'),
)