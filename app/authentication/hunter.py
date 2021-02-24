import requests
from django.conf import settings


def validate_email(email: str) -> bool:
    """Check if user email exists using third party service."""
    request = requests.get(f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.HUNTER_API_KEY}')
    data = request.json()

    return True if data['data']['status'] == 'valid' else False
