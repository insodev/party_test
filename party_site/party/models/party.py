from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone


class Party(models.Model):
    """Мероприятие"""

    title = models.CharField(help_text='Название', max_length=255)
    party_time_at = models.DateTimeField(help_text='Начало мероприятия')
    party_time_till = models.DateTimeField(help_text='Окончание мероприятия')
    description = models.TextField(help_text='Описание')

    members = models.ManyToManyField('party.User', through='party.PartyRegistration')

    class Meta:
        ordering = ('party_time_at', 'party_time_till', 'pk')
        verbose_name_plural = 'Parties'

    def __str__(self):
        return '{title} с {party_time_at} по {party_time_till}'.format(
            title=self.title,
            party_time_at=timezone.localtime(self.party_time_at),
            party_time_till=timezone.localtime(self.party_time_till),
        )

    def clean(self):
        if self.party_time_till < self.party_time_at:
            raise ValidationError(_('Начало мероприятия не может быть позже его окончания'))

    @property
    def has_members(self):
        return bool(self.members.count())

    @property
    def date(self):
        return timezone.localtime(self.party_time_at).date()
