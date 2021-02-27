from django.conf import settings
from authentication.models import User
import pytest
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password


pytestmark = [pytest.mark.django_db]


def test_user_viewset(api, superuser):
    url = reverse('user-set-password', kwargs={'pk': superuser.id})

    response = api.post(url, {'password': '1234'})

    assert response.status_code == 200
    assert response.data['status'] == 'password changed'


def test_user_viewset_by_another_user(api, user, anon_api):
    url = reverse('user-set-password', kwargs={'pk': user.id})

    response = api.post(url, {'password': '1234'})

    assert response.status_code == 403


def test_change_password(api, anon_api, superuser):
    url = reverse('user-set-password', kwargs={'pk': superuser.id})
    response = api.post(url, {'password': '1234'})

    assert response.status_code == 200

    login_url = reverse('login')
    login_response = anon_api.post(login_url, {
        'email': superuser.email,
        'password': '1234'
    })

    assert login_response.status_code == 200
