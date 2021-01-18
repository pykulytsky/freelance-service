from authentication.models import Role, User
import pytest
import jwt
from django.conf import settings
from datetime import datetime

pytestmark = [pytest.mark.django_db]


def test_token_enought_fields(superuser):
    token = superuser.token

    payload = jwt.decode(token, settings.SECRET_KEY)

    assert payload.get('id', None) != None
    assert payload.get('exp', None) != None
    assert payload.get('role', None) != None
    assert payload.get('is_superuser', None) != None


def test_token_match_fields(superuser):
    token = superuser.token

    payload = jwt.decode(token, settings.SECRET_KEY)

    assert payload.get('id', None) == superuser.id
    assert payload.get('role', None) == superuser.role.id
    assert payload.get('is_superuser', None) == superuser.is_superuser


def test_user_by_token_payload(superuser):
    token = superuser.token

    payload = jwt.decode(token, settings.SECRET_KEY)

    assert payload.get('id', None) != None
    assert superuser.id == payload['id']
    assert User.objects.get_or_none(id=payload['id']) != None 


def test_base_token_expired(superuser):
   token = superuser.token

   payload = jwt.decode(token, settings.SECRET_KEY)

   assert payload['exp'] > datetime.now().timestamp()


def test_user_role_by_token_payload(superuser):
    token = superuser.token

    payload = jwt.decode(token, settings.SECRET_KEY)

    assert payload['role'] == superuser.role.id
    assert Role.objects.get_or_none(id=payload['role']) != None

