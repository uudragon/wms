from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uudragon_wms.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^wms/baseinfo/', include('base_info.urls')),
    url(r'^wms/inbound', include('inbound.urls')),
    url(r'^wms/outbound', include('outbound.urls')),
    url(r'^wms/inner', include('inner.urls')),
)
