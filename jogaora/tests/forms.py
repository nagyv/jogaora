from django.test import TestCase


class ParticipantListFormTest(TestCase):

    def test_clean_w_participant_season_ticket(self):
        "participant has season ticket"
        raise NotImplementedError

    def test_clean_w_participant_paid(self):
        "participant buys season ticket"
        raise NotImplementedError

    def test_clean_w_namepaid(self):
        "new participant"
        raise NotImplementedError

    def test_clean_w_no_name(self):
        "missing name"
        raise NotImplementedError

    def test_clean_w_no_paid(self):
        "missing paid"
        raise NotImplementedError

    def test_save_w_participant(self):
        raise NotImplementedError

    def test_save_w_participant_paid(self):
        raise NotImplementedError

    def test_save_w_namepaid(self):
        raise NotImplementedError
