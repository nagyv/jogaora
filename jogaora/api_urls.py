from django.conf.urls import patterns, url
from .views import APIListSession

urlpatterns = patterns('',
    url(r'^sessions/$', APIListSession.as_view(), name='api_sessions'),
)
