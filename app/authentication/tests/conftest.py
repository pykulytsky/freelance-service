from _pytest.fixtures import fixture
import pytest

from rest_framework.test import APIClient

from authentication.models import Role
from authentication.backend import JWTAuthentication

from mixer.backend.django import mixer as _mixer
from authentication.creator import UserCreator

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
def user(django_user_model, employer_role, mixer):
    return mixer.blend(
        django_user_model,
        role=employer_role,
        is_active=True)

@pytest.fixture
def inactive_user(django_user_model, performer_role, mixer):
    return mixer.blend(
        django_user_model,
        role = performer_role,
    )


@pytest.fixture
def active_user(django_user_model, performer_role, mixer):
    return mixer.blend(
        django_user_model,
        role=performer_role,
        is_active=True)


@pytest.fixture
def superuser(django_user_model, performer_role, mixer):
    return mixer.blend(
        django_user_model,
        role=performer_role,
        is_superuser=True,
        si_staff=True)


@pytest.fixture
def backend():
    return JWTAuthentication()


@pytest.fixture
def creator():
    return UserCreator


@pytest.fixture
def creator_mail(mocker):
    return mocker.patch('UserCreator.send_email')