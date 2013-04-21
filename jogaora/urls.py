from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^participants/$', lambda: '', name='participants'),
    url(r'^participants/(?P<pk>\d+)/$', lambda: '', name='participants'),
    url(r'^sessions/$', lambda: '', name='sessions'),
    url(r'^sessions/(?P<pk>\d+)/$', lambda: '', name='sessions'),
    url(r'^season_tickets/$', lambda: '', name='season_tickets'),
    url(r'^season_tickets/(?P<pk>\d+)/$', lambda: '', name='season_tickets'),
)
