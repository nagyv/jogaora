# TODO: write a view to list session data (ShowSession)
# TODO: write the missing templates

from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, FormView

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


class AddParticipantToSession(FormView):
    # TODO extra: Try to write this
    template_name = 'participant_to_session.html'
    form_class = ParticipantListForm


class CreateSeasonTicket(CreateView):
    model = SeasonTicket
