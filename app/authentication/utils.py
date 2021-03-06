import random
import string

from django.utils import timezone

from .exceptions import InvalidTimeError
from .models import User


def set_login_time(user: User) -> None:
    try:
        if not user.first_login:
            user.first_login = user.last_login = timezone.now()
        else:
            user.last_login = timezone.now()

        user.save()
    except (TypeError, ValueError):
        raise InvalidTimeError("Invalid time")


def generate_random_password() -> str:
    """Generates truly random password"""
    letters = string.ascii_letters
    password = ''.join(random.choice(letters) for _ in range(random.randint(5, 14)))

    return password


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
