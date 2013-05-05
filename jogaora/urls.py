from django.conf.urls import patterns, url
from .views import CreateParticipant, CreateSession, CreateSeasonTicket, \
    AddParticipantToSession, ListSession, ShowSession

urlpatterns = patterns(
    '',
    url(r'^$', ListSession.as_view(), name='sessions'),
    url(r'^new/$', CreateSession.as_view(), name='add_session'),
    url(r'^(?P<pk>\d+)/$', ShowSession.as_view(), name='sessions'),
    url(r'^(?P<pk>\d+)/add/$', AddParticipantToSession.as_view(), name='session_add_participant'),
    url(r'^participants/$', CreateParticipant.as_view(), name='participants'),
    url(r'^season_tickets/$', CreateSeasonTicket, name='season_tickets'),
)
