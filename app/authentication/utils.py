from .models import User
from django.utils import timezone

import string
import random


def set_login_time(user: User) -> None:
    if not user.first_login:
        user.first_login = user.last_login = timezone.now()
    else:
        user.last_login = timezone.now()

    user.save()


def generate_random_password() -> str:
    """Generates truly random password"""
    letters = string.ascii_letters
    password = ''.join(random.choice(letters) for _ in range(random.randint(5, 14)))

    return password


