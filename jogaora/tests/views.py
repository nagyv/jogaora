import json
from django.core.urlresolvers import reverse
from django.test import TestCase

from .models import Session


class APITest(TestCase):

    def setUp(self):
        self.session1 = Session.objects.create(name='Ma, itt')
        self.session2 = Session.objects.create(name='Ma nem, itt')

    def test_list_sessions(self):
        resp = self.client.get(reverse("api_sessions"))
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(len(data), 2)

        resp = self.client.get(reverse("api_sessions") + "?name=Ma,")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.content)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["id"], self.session1.pk)

class AddParticipantToSessionTest(TestCase):

    def setUp(self):
        self.session1 = Session.objects.create(name='Ma, itt')

    def test_context(self):
        resp = self.client.get(reverse('session_add_participant', args=(), kwargs={'pk': self.session1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('form' in resp.context_data)
        self.assertTrue('session' in resp.context_data)
        self.assertEqual(resp.context_data['session'], self.session1)