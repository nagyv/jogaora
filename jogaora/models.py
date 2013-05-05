import datetime
from django.db import models

from model_utils.models import TimeStampedModel


class PrepaidParticipantManager(models.Manager):

    def get_query_set(self):
        """ TODO: Return only the participants with an active season ticket """
        qs = super(PrepaidParticipantManager, self).get_query_set()
        return qs.filter(
            seasonticket__start_date__lte=datetime.date.today(), seasonticket__end_date__gte=datetime.date.today()
        )


class ActiveParticipantManager(models.Manager):
    """ Returns the participants either with an active season ticket
    or who were on a session in the past two weeks"""

    def get_query_set(self):
        qs = super(ActiveParticipantManager, self).get_query_set()
        active_participant = models.Q(sessionparticipant__created__gte=datetime.date.today()-datetime.timedelta(days=12))
        with_seasonticket = models.Q(seasonticket__end_date__gte=datetime.date.today(), seasonticket__start_date__lte=datetime.date.today())
        return qs.filter( active_participant | with_seasonticket )


class Participant(TimeStampedModel):
    name = models.CharField(max_length=255)
    nick = models.CharField(max_length=255, blank=True)
    email = models.EmailField()

    objects = models.Manager()
    with_seasonticket = PrepaidParticipantManager()
    active = ActiveParticipantManager()

    def _get_active_season_ticket(self):
        try:
            return self.seasonticket_set.filter(start_date__lte=datetime.date.today(), end_date__gte=datetime.date.today()).order_by('-end_date')[0]
        except IndexError:
            return None
    active_season_ticket = property(_get_active_season_ticket)

    def __unicode__(self):
        return self.nick if self.nick else self.name

    @models.permalink
    def get_absolute_url(self):
        return ('participants', (), {'pk': self.pk})


class Session(models.Model):
    # TODO: write a method to return the number of participants during a session
    # TODO: write a method to return the #Participants with a season and with a daily ticket
    name = models.CharField(max_length=255)
    participants = models.ManyToManyField(Participant, through='SessionParticipant')

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('sessions', (), {'pk': self.pk})

    def participant_add(self, participant, paid=None):
        return SessionParticipant.objects.create(
            participant=participant,
            session=self,
            season_ticket=participant.active_season_ticket,
            paid=paid)


class SeasonTicket(TimeStampedModel): # TODO: rewrite with model_utils: TimeFramedModel
    participant = models.ForeignKey(Participant)
    start_date = models.DateField(default=lambda: datetime.date.today())
    end_date = models.DateField(default=lambda: datetime.date.today()+datetime.timedelta(days=30))
    paid = models.DecimalField(max_digits=7, decimal_places=2)

    def __unicode__(self):
        return '%s (%s-%s)' % (self.participant, self.start_date, self.end_date)

    @models.permalink
    def get_absolute_url(self):
        return ('season_tickets', (), {'pk': self.pk})


class SessionParticipant(TimeStampedModel):
    participant = models.ForeignKey(Participant)
    session = models.ForeignKey(Session)
    season_ticket = models.ForeignKey(SeasonTicket, null=True)
    paid = models.DecimalField(max_digits=7, decimal_places=2, null=True)

    def __unicode__(self):
        return '%s - %s' % (self.participant, self.session)
