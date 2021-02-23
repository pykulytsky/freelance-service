import pytest
from sendgrid.client import SendgridAPIClient
from sendgrid.mail import Receiver
from mixer.backend.django import mixer

from authentication.models import Role

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def client():
    return SendgridAPIClient()


def test_client(client):
    user = mixer.blend('authentication.User', role=Role.objects.create(id=1))
    receiver = Receiver.from_user_model(user)

    response = client.send_verification_mail(receiver)

    assert response['status'] == 202