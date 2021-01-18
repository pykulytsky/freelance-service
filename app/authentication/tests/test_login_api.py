import pytest

from django.urls import reverse

pytestmark = [pytest.mark.django_db]


def test_login(api, superuser):
    url = reverse('login')

    response = api.post(
        url,
        {
            'username': superuser.username,
            'password': superuser.password,
            'email': superuser.email
        })

    assert False, response.data
    assert response.status_code == 200