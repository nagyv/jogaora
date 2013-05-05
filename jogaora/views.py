from django.core.urlresolvers import reverse
from django.views.generic import ListView, CreateView, FormView, DetailView
from rest_framework.generics import ListAPIView, RetrieveAPIView

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


class ShowSession(DetailView):
    model = Session


class AddParticipantToSession(FormView):
    template_name = 'jogaora/participant_to_session.html'
    form_class = ParticipantListForm

    def get_initial(self):
        return {'session': Session.objects.get(**self.kwargs)}

    def get_context_data(self, form):
        ctx = super(AddParticipantToSession, self).get_context_data(form=form)
        ctx['session'] = Session.objects.get(**self.kwargs)
        return ctx


class CreateSeasonTicket(CreateView):
    model = SeasonTicket


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


class APIShowSession(RetrieveAPIView):
    model = Session


class APIListParticipant(ListAPIView):
    model = Participant

    def get_queryset(self):
        """
        Return only the active participants
        """
        return Participant.active.all()


class APIShowParticipant(RetrieveAPIView):
    model = Participant
