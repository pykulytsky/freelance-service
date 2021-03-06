import pytest
from sendgrid.http import (SendgridAuthenticationFailed, SendgridHTTP,
                           SendgridWrongRequest)

pytestmark = [
    pytest.mark.django_db,
]


@pytest.fixture()
def http():
    return SendgridHTTP()


def test_http_wrong_request(http):
    with pytest.raises(SendgridWrongRequest):
        http.post('mail/send', {})


def test_http_auth_error():
    http = SendgridHTTP(api_key='wrong_api_key')

    with pytest.raises(SendgridAuthenticationFailed):
        http.post('mail/send', {})


def test_http_send_email(http):
    response = http.post('mail/send', {
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
