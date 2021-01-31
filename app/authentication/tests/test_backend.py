from datetime import datetime
import pytest
from django.urls import reverse
import jwt
from django.conf import settings

from rest_framework import exceptions

pytestmark = [pytest.mark.django_db]


def test_backend_access_inactive_user_exception(api, backend, inactive_user):
    url = reverse('login')
    response = api.post(
        url,
        {
            'username': inactive_user.username,
            'password': inactive_user.password,
            'email': inactive_user.email
        })

    request = response.wsgi_request

    with pytest.raises(exceptions.AuthenticationFailed):
        backend.authenticate(request)


def test_backend_access_inactive_user(api, inactive_user):
    url = reverse('login')
    response = api.post(
        url,
        {
            'username': inactive_user.username,
            'password': inactive_user.password,
            'email': inactive_user.email
        })

    assert response.status_code == 403


def test_backend_access_active_user(api, active_user):
    url = reverse('login')
    response = api.post(
        url,
        {
            'username': active_user.username,
            'password': active_user.password,
            'email': active_user.email
        })

    assert response.status_code == 403


def test_backend_access_inactive_user_with_employer_role(api, backend, user):
    url = reverse('login')
    response = api.post(
        url,
        {
            'username': user.username,
            'password': user.password,
            'email': user.email
        })

    request = response.wsgi_request

    with pytest.raises(exceptions.AuthenticationFailed):
        backend.authenticate(request)


def test_backend_with_wrong_auth_credentials(api, backend):
    url = reverse('login')
    response = api.post(
        url,
        {
            'username': 'WRONG USER',
            'password': 'WRONG PASS',
            'email': 'WRONG EMAIL'
        })

    request = response.wsgi_request

    with pytest.raises(exceptions.AuthenticationFailed):
        backend.authenticate(request)


def test_backend_access_active_user_exception_on_protected_endpoint(api, backend):
    url = reverse('test')
    response = api.get(url)

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
