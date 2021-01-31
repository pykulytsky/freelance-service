import pytest
from django.urls import reverse

from authentication.models import User

pytestmark = [pytest.mark.django_db]


def test_activate_user(superuser, inactive_api):
    url = reverse('activate', kwargs={
        'code': superuser.email_verification_code
    })

    response = inactive_api.post(url)

    assert response.status_code == 200
    assert response.data['info'] == 'activated'
    assert User.objects.get(id=superuser.id).is_active
