from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db import models


class PartyRegistration(models.Model):
    """
    Регистрация пользователя на мероприятие
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    party = models.ForeignKey('party.Party', on_delete=models.PROTECT)
    registered_at = models.DateTimeField(auto_now=True)
    # deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            ('user', 'party',),
        )

    def __str__(self):
        return 'Регистрация {user} на мероприятие {party}'.format(
            user=self.user,
            party=self.party,
        )
