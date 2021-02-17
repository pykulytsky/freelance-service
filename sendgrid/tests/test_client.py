import pytest
from sendgrid.client import SendgridAPIClient
from sendgrid.mail import Receiver
from mixer.backend.django import mixer

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def client():
    return SendgridAPIClient()


def test_client(client):
    user = mixer.blend('authentication.User')
    receiver = Receiver.from_user_model()(user)

    response = client.send_verification_mail(receiver)

    assert response['status'] == 202
