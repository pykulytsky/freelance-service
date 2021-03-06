from datetime import datetime

import jwt
import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import exceptions

pytestmark = [pytest.mark.django_db]


def test_backend_access_inactive_user_exception(inactive_api, backend, inactive_user):
    url = reverse('login')
    response = inactive_api.post(
        url,
        {
            'username': inactive_user.username,
            'password': inactive_user.password,
            'email': inactive_user.email
        })

    request = response.wsgi_request

    with pytest.raises(exceptions.AuthenticationFailed):
        backend.authenticate(request)


def test_backend_access_inactive_user(inactive_api, inactive_user):
    url = reverse('login')
    response = inactive_api.post(
        url,
        {
            'username': inactive_user.username,
            'password': inactive_user.password,
            'email': inactive_user.email
        })

    assert response.status_code == 403


def test_backend_access_inactive_user_with_employer_role(inactive_api, backend, user):
    url = reverse('login')
    response = inactive_api.post(
        url,
        {
            'username': user.username,
            'password': user.password,
            'email': user.email
        })

    request = response.wsgi_request

    with pytest.raises(exceptions.AuthenticationFailed):
        backend.authenticate(request)


def test_backend_with_wrong_auth_credentials(inactive_api, backend):
    url = reverse('login')
    response = inactive_api.post(
        url,
        {
            'username': 'WRONG USER',
            'password': 'WRONG PASS',
            'email': 'WRONG EMAIL'
        })

    request = response.wsgi_request

    with pytest.raises(exceptions.AuthenticationFailed):
        backend.authenticate(request)


def test_backend_access_active_user_exception_on_protected_endpoint(inactive_api, backend):
    url = reverse('test')
    response = inactive_api.get(url)

    request = response.wsgi_request

    with pytest.raises(exceptions.AuthenticationFailed):
        backend.authenticate(request)


def test_backend_success(active_api, backend, active_user):
    url = reverse('test')
    response = active_api.get(url)
    request = response.wsgi_request

    user = backend.authenticate(request)

    assert active_user == user[0]


def test_backend_success_token(active_api, backend, active_user):
    url = reverse('test')
    response = active_api.get(url)
    request = response.wsgi_request

    user = backend.authenticate(request)
    token = jwt.decode(user[1], settings.SECRET_KEY, algorithms=['HS256'])

    assert token['id'] == active_user.id
    assert token['exp'] > datetime.now().timestamp()
