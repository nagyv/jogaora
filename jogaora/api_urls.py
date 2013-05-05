from django.conf.urls import patterns, url
from .views import APIListSession, APIListParticipant, APIShowSession, APIShowParticipant

urlpatterns = patterns('',
    url(r'^sessions/$', APIListSession.as_view(), name='api_sessions'),
    url(r'^sessions/(?P<pk>\d+)/$', APIShowSession.as_view(), name='api_sessions'),
    url(r'^participants/$', APIListParticipant.as_view(), name='api_participants'),
    url(r'^participants/(?P<pk>\d+)/$', APIShowParticipant.as_view(), name='api_participants'),
)
