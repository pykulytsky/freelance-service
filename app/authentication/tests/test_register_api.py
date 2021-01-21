import pytest
from django.urls import reverse
import jwt
from django.conf import settings

pytestmark = [pytest.mark.django_db]


def test_register_works(anon_api, performer_role):
    url = reverse('register')

    response = anon_api.post(
        url,
        {
            'username': 'test',
            'email': 'test@mail.com',
            'password': '123456',
            'first_name': 'oleh',
            'last_name': 'pykulytsky',
            'role': performer_role.id
        }
    )

    assert response.status_code == 200


def test_register_data(anon_api, performer_role):
    url = reverse('register')

    response = anon_api.post(
        url,
        {
            'username': 'test',
            'email': 'test@mail.com',
            'password': '123456',
            'first_name': 'oleh',
            'last_name': 'pykulytsky',
            'role': performer_role.id
        }
    )

    assert response.status_code == 200
    assert response.data['token'] is not None


def test_register_api_decode_token(anon_api, performer_role):
    url = reverse('register')

    response = anon_api.post(
        url,
        {
            'username': 'test',
            'email': 'test@mail.com',
            'password': '123456',
            'first_name': 'oleh',
            'last_name': 'pykulytsky',
            'role': performer_role.id
        }
    )

    payload = jwt.decode(response.data['token'], settings.SECRET_KEY)

    assert response.status_code == 200
    assert payload['role'] == performer_role.id
