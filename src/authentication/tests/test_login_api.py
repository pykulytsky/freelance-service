import pytest
from authentication.models import User
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


def test_login_api_works(anon_api, performer_role):
    user = User.objects.create_user(username='test', email='test@mail.com', password='1234', role=performer_role, first_name='test', last_name='test', is_active=True)
    url = reverse('login')

    response = anon_api.post(url, {
        'email': user.email,
        'password': '1234'
    })

    assert response.status_code == 200


def test_login_api_get_token(anon_api, performer_role):
    user = User.objects.create_user(username='test', email='test@mail.com', password='1234', role=performer_role, first_name='test', last_name='test', is_active=True)
    url = reverse('login')

    response = anon_api.post(url, {
        'email': user.email,
        'password': '1234'
    })

    assert response.data['token']
