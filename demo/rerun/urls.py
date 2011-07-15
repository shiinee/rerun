from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('rerun.views',
    (r'^$', 'index'),
    (r'^feeds/$', 'index'),
    (r'^feeds/(?P<feed_id>\d+)/$', 'feed'),
    (r'^entries/(?P<entry_id>\d+)/$', 'entry'),
    (r'^feeds/add/$', 'add'),
    (r'^subscribe/$', 'subscribe'),
    (r'^deliver/(?P<subscription_id>\d+)/$', 'deliver'),
    (r'^xml/(?P<subscription_id>\d+).xml$', 'xml'),
    # Example:
    # (r'^demo/', include('demo.foo.urls')),
)

urlpatterns += patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
