import pytest

from django.urls import reverse

pytestmark = [pytest.mark.django_db]


def test_login_inactive_user(inactive_api, superuser):
    url = reverse('login')

    response = inactive_api.post(
        url,
        {
            'username': superuser.username,
            'password': superuser.password,
            'email': superuser.email
        })

    assert response.status_code == 403


@pytest.mark.xfail(strict=True)
def test_login_active_user(api, active_user):
    url = reverse('login')

    response = api.post(
        url,
        {
            'username': active_user.username,
            'password': active_user.password,
            'email': active_user.email
        })

    assert response.status_code == 200
    assert response.data['token'] == active_user.token
