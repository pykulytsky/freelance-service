import pytest

from rest_framework.test import APIClient

from authentication.models import Role
from authentication.backend import JWTAuthentication

from mixer.backend.django import mixer as _mixer
from authentication.creator import UserCreator

from PIL import Image


@pytest.fixture
def image():
    img = Image.open('static/assets/assets/avatars/image.gif')

    return img.filename


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def anon_api():
    client = APIClient()

    return client


@pytest.fixture
def api(superuser):
    client = APIClient()

    token = superuser.token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return client


@pytest.fixture
def performer_role():
    return Role.objects.create(id=1)


@pytest.fixture
def employer_role():
    return Role.objects.create(id=2)


@pytest.fixture
def user(django_user_model, employer_role, mixer, image):
    return mixer.blend(
        django_user_model,
        role=employer_role,
        is_active=True,
        avatar=image)


@pytest.fixture
def inactive_user(django_user_model, performer_role, mixer, image):
    return mixer.blend(
        django_user_model,
        role=performer_role,
        avatar=image
    )


@pytest.fixture
def inactive_api(inactive_user):
    client = APIClient()

    token = inactive_user.token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return client


@pytest.fixture
def active_user(django_user_model, performer_role, mixer, image):
    return mixer.blend(
        django_user_model,
        role=performer_role,
        is_active=True,
        avatar=image
    )


@pytest.fixture
def superuser(django_user_model, performer_role, mixer, image):
    return mixer.blend(
        django_user_model,
        role=performer_role,
        is_superuser=True,
        is_staff=True,
        avatar=image,
        password='123456')


@pytest.fixture
def backend():
    return JWTAuthentication()


@pytest.fixture
def creator():
    return UserCreator


@pytest.fixture
def creator_mail(mocker):
    return mocker.patch('UserCreator.send_email')


@pytest.fixture
def active_api(active_user):
    client = APIClient()

    token = active_user.token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return client


@pytest.fixture(autouse=True)
def use_debug_true(settings):
    settings.DEBUG = True


@pytest.fixture
def use_debug_false(settings):
    settings.DEBUG = False
