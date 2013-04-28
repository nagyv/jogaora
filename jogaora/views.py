# TODO: write a view to list session data (ShowSession)
# TODO: write the missing templates

from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, FormView
from rest_framework.generics import ListAPIView

from .models import Participant, Session, SeasonTicket
from .forms import ParticipantListForm, SessionForm


class CreateParticipant(CreateView):
    model = Participant

    def get_success_url(self):
        return reverse('participants')


class CreateSession(CreateView):
    model = Session
    form_class = SessionForm


class ListSession(ListView):
    model = Session


class APIListSession(ListAPIView):
    model = Session

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = super(APIListSession, self).get_queryset()
        name = self.request.QUERY_PARAMS.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__istartswith=name)
        return queryset


class AddParticipantToSession(FormView):
    # TODO extra: Try to write this
    template_name = 'participant_to_session.html'
    form_class = ParticipantListForm


class CreateSeasonTicket(CreateView):
    model = SeasonTicket
