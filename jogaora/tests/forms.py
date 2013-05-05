from django.test import TestCase

from ..forms import ParticipantListForm
from ..models import Participant, Session

class ParticipantListFormTest(TestCase):

    def test_clean_w_participant_season_ticket(self):
        "participant has season ticket"
        session = Session.objects.create(name='Ma, itt')
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')
        st = participant.seasonticket_set.create(paid=8000)

        form = ParticipantListForm(data={
            'session': session.pk,
            'participant': participant.pk
            })
        self.assertTrue(form.is_valid())

    def test_clean_w_participant_paid(self):
        "participant buys season ticket"
        session = Session.objects.create(name='Ma, itt')
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')
        form = ParticipantListForm(data={
            'session': session.pk,
            'participant': participant.pk,
            })
        self.assertFalse(form.is_valid())
        self.assertTrue('paid' in form.errors)

        form = ParticipantListForm(data={
            'session': session.pk,
            'participant': participant.pk,
            'paid': 1000,
            })
        self.assertTrue(form.is_valid())

    def test_clean_w_namepaid(self):
        "new participant"
        session = Session.objects.create(name='Ma, itt')
        form = ParticipantListForm(data={
            'session': session.pk,
            'paid': 1000
            })
        self.assertFalse(form.is_valid())
        self.assertTrue('name' in form.errors)

        form = ParticipantListForm(data={
            'session': session.pk,
            'name': 'Parti',
            'paid': 1000
            })
        self.assertTrue(form.is_valid())

    def test_save_w_participant(self):
        session = Session.objects.create(name='Ma, itt')
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')
        st = participant.seasonticket_set.create(paid=8000)

        form = ParticipantListForm(data={
            'session': session.pk,
            'participant': participant.pk
            })
        form.is_valid()
        sp = form.save()
        self.assertEqual(sp.participant, session.participants.all()[0])

    def test_save_w_participant_paid(self):
        session = Session.objects.create(name='Ma, itt')
        participant = Participant.objects.create(
            name='New Participant',
            email='me@example.com')

        form = ParticipantListForm(data={
            'session': session.pk,
            'participant': participant.pk,
            'paid': 1000
            })
        form.is_valid()
        sp = form.save()
        self.assertEqual(sp.participant, session.participants.all()[0])
        self.assertEqual(sp.paid, 1000)

    def test_save_w_namepaid(self):
        session = Session.objects.create(name='Ma, itt')

        form = ParticipantListForm(data={
            'session': session.pk,
            'name': 'Parti',
            'paid': 1000
            })
        form.is_valid()
        sp = form.save()
        self.assertEqual(sp.participant.name, 'Parti')
        self.assertEqual(sp.paid, 1000)
