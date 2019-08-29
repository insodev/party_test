from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
import pytz


class User(AbstractUser):
    timezone = models.CharField(
        help_text=_('Time Zone'),
        max_length=40,
        choices=[(t, t) for t in pytz.common_timezones],
        default=settings.DEFAULT_USER_TIMEZONE
    )
