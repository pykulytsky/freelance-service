from PIL import Image
import pytest
import requests_mock # noqa

from authentication.mailchimp import AppMailchimp, MailchimpMember

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def image():
    img = Image.open('static/assets/assets/avatars/image.gif')

    return img.filename


@pytest.fixture(autouse=True)
def set_chimp_credentials(settings):
    settings.MAILCHIMP_API_KEY = 'key-us05'
    settings.MAILCHIMP_AUDIENCE_ID = '123cba'


@pytest.fixture
def mailchimp():
    client = AppMailchimp()

    with requests_mock.Mocker() as http_mock:
        client.http_mock = http_mock
        yield client


@pytest.fixture
def mailchimp_member(user):
    return MailchimpMember.from_django_user(user)


@pytest.fixture
def post(mocker):
    return mocker.patch('authentication.mailchimp.http.MailchimpHTTP.post')


@pytest.fixture
def user(mixer, performer_role, image):
    return mixer.blend('authentication.User', email='test@e.mail', first_name='Rulon', last_name='Oboev', role=performer_role, avatar=image)
