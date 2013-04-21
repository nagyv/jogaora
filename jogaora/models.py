import datetime
from django.db import models


class Participant(models.Model):
    # TODO: add optional nickname
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def _get_active_season_ticket(self):
        # TODO: fix this to return the last active season ticket or None
        return None
    active_season_ticket = property(_get_active_season_ticket)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('participant', (), {'pk': self.pk})


class Session(models.Model):
    # TODO: write a method to return the number of participants during a session
    # TODO: write a method to return the #Participants with a season and with a daily ticket
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(Participant, through='SessionParticipant')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('session', (), {'pk': self.pk})

    def participant_add(self, participant, paid=None):
        return SessionParticipant.objects.create(
            participant=participant,
            session=self,
            season_ticket=participant.active_season_ticket,
            paid=paid)


class SeasonTicket(models.Model):
    participant = models.ForeignKey(Participant)
    start_date = models.DateField(default=lambda: datetime.date.today())
    end_date = models.DateField(default=lambda: datetime.date.today()+datetime.timedelta(days=30))
    paid = models.DecimalField(max_digits=7, decimal_places=2)

    def __unicode__(self):
        return '%s (%s-%s)' % (self.participant, self.start_date, self.end_date)

    @models.permalink
    def get_absolute_url(self):
        return ('season_ticket', (), {'pk': self.pk})


class SessionParticipant(models.Model):
    participant = models.ForeignKey(Participant)
    session = models.ForeignKey(Session)
    season_ticket = models.ForeignKey(SeasonTicket, null=True)
    paid = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.participant, self.session)
