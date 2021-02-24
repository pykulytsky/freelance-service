import requests
from django.conf import settings

from .hunter import validate_email as hunter


def validate_email(email: str) -> bool:
    """Check if user email exists using third party service."""
    request = requests.get(f'http://apilayer.net/api/check?access_key={settings.MAILBOXLAYER_API_KEY}&email={email}')
    data = request.json()

    try:
        return True if data['smtp_check'] and data['mx_found'] else False
    except KeyError:
        return hunter(email)
