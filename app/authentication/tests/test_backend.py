from django.urls.base import reverse
import pytest
from django.urls import reverse

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


def test_backend_access_inactive_user(api, backend, inactive_user):
    url = reverse('login')
    response = api.post(
        url,
        {
            'username': inactive_user.username,
            'password': inactive_user.password,
            'email': inactive_user.email
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
