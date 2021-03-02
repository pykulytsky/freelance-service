import pytest
from django.urls import reverse

from authentication.tasks import send_new_password


pytestmark = [pytest.mark.django_db]


def test_user_viewset(api, superuser):
    url = reverse('user-set-password', kwargs={'pk': superuser.id})

    response = api.post(url, {'password': '1234'})

    assert response.status_code == 200
    assert response.data['status'] == 'password changed'


def test_user_viewset_by_another_user(api, user):
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


def test_reset_password(api, superuser):

    url = reverse('user-reset-password', kwargs={'pk': superuser.id})
    response = api.post(url, {
        'email': superuser.email
    })

    assert response.status_code == 200


def test_send_email_on_reset_password(mocker, api, superuser):
    mocker.patch('authentication.tasks.send_new_password.delay')

    url = reverse('user-reset-password', kwargs={'pk': superuser.id})
    response = api.post(url, {
        'email': superuser.email
    })

    assert response.status_code == 200
    assert False, response.data
    assert send_new_password.delay.assert_called_once()
