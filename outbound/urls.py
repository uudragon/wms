from django.conf.urls import patterns, url

__author__ = 'pluto'


urlpatterns = patterns(
    'outbound.views',
    url(r'^(.+)/split/$', 'split'),
)