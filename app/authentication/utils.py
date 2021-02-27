from .models import User
from django.utils import timezone


def set_login_time(user: User):
    if not user.first_login:
        user.first_login = user.last_login = timezone.now()
    else:
        user.last_login = timezone.now()
