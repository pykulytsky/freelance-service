import pytest
from sendgrid.client import SendgridAPIClient

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def client():
    return SendgridAPIClient()


def test_client(client):
    response = client.send_verification_mail(
        receiver_email='oleh.pykulytskyi.ki.2018@lpnu.ua',
        dynamic_template_data={
        "personalizations": [{
            "to": [{'email': 'oleh.pykulytskyi.ki.2018@lpnu.ua', 'name': 'Oleh'}],
            "dynamic_template_data": {
                'first_name': 'Oleh',
                'verification_link': 'http://loalhost:8080/verify/123121wefdsfdgd'
            },
            "subject": "Test message",
        }],
        "template_id": 'd-c0dc70b630b54c1d8214de6dc02d8d38',
        "from": {
            "email": 'pragmatic.once.lviv@gmail.com',
            "name": "Oleh Pykulytsky"
        }
    }
    )

    assert response['status'] == 202
