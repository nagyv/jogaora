import datetime
from django.test import TestCase
from ..models import Participant, Session, SeasonTicket, \
    SessionParticipant


class ParticipantTest(TestCase):

    def test_participant_minimal_data(self):
        participant = Participant.objects.create(name='New Participant')
        self.assertEqual(participant.pk, 1)

    def test_participant_full_data(self):
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')
        self.assertEqual(participant.pk, 1)

    def test_active_season(self):
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')
        self.assertEqual(participant.active_season_ticket, None)

        st = participant.seasonticket_set.create(paid=8000)
        self.assertEqual(participant.active_season_ticket, st)


class SessionTest(TestCase):

    def test_session_minimal(self):
        session = Session.objects.create(name='Ma, itt')
        self.assertEqual(session.pk, 1)

    def test_session_participant_add_daily(self):
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')
        session = Session.objects.create(name='Ma, itt')
        session.participant_add(participant=participant, paid=900)
        self.assertEqual(SessionParticipant.objects.count(), 1)

    def test_session_participant_add_w_st(self):
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')
        participant.seasonticket_set.create(paid=8000)
        session = Session.objects.create(name='Ma, itt')
        session.participant_add(participant=participant)
        self.assertEqual(SessionParticipant.objects.count(), 1)


class SeasonTicketTest(TestCase):

    def setUp(self):
        self.participant = Participant.objects.create(name='New Participant')

    def test_season_ticket_minimal(self):
        ticket = SeasonTicket.objects.create(
            participant=self.participant,
            paid=8000)
        self.assertEqual(ticket.pk, 1)
        self.assertEqual(ticket.start_date, datetime.date.today())
        self.assertEqual((ticket.end_date - ticket.start_date).days, 30)


class PrepaidParticipantManagerTest(TestCase):

    def setUp(self):
        self.active = Participant.objects.create(name='Prepaid')
        self.inactive = Participant.objects.create(name='Inactive')

    def test_get_query_set(self):
        SeasonTicket.objects.create(
            participant=self.active,
            paid=8000)
        qs = Participant.with_seasonticket.all()
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].pk, self.active.pk)


class ActiveParticipantManagerTest(TestCase):

    def test_inactive(self):
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')
        self.assertEqual(Participant.active.count(), 0)

    def test_for_prepaid(self):
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')
        st = participant.seasonticket_set.create(paid=8000)
        self.assertEqual(Participant.active.count(), 1)
        

    def test_for_active(self):
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')
        session = Session.objects.create(name='Ma, itt')
        session.participant_add(participant=participant, paid=900)
        self.assertEqual(Participant.active.count(), 1)
