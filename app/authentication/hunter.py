import requests
from django.conf import settings


def validate_email(email: str) -> bool:
    request = requests.get(f'https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.HUNTER_API_KEY}')
    data = request.json()

    if data['data']['status'] == 'valid':
        return True
    else:
        return False
