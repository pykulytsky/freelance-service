from authentication.models import User
import pytest
from authentication import utils
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


def test_detect_user_login_time(mocker, anon_api, performer_role):
    mocker.patch('authentication.utils.set_login_time')
    user = User.objects.create(email='test@g.ot', password='1234', username='oleh', is_active=True, role=performer_role, first_name='oleh', last_name='pykul')

    url = reverse('login')
    anon_api.post(url, {
        'email': user.email,
        'password': user.password,
    })

    assert user.is_active
    utils.set_login_time.assert_not_called()
