from django.conf import settings
from django.utils import timezone


class UserTimeZone:
    """
    middleware для установки пользовательской timezone
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            timezone.activate(request.user.timezone)
        else:
            timezone.activate(settings.DEFAULT_USER_TIMEZONE)

        response = self.get_response(request)
        timezone.deactivate()

        return response
