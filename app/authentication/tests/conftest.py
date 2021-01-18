from _pytest.fixtures import fixture
import pytest

from rest_framework.test import APIClient

from authentication.models import Role
from authentication.backend import JWTAuthentication


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
def user(django_user_model, employer_role):
    return django_user_model.objects.create_user(
        username="test2",
        password="123456",
        email="test2@py.com",
        role=employer_role,
        user_verified=True
    )

@pytest.fixture
def inactive_user(django_user_model, performer_role):
    return django_user_model.objects.create_user(
        username="test1",
        password="123456",
        email="test1@py.com",
        role=performer_role
    )


@pytest.fixture
def active_user(django_user_model, performer_role):
    return django_user_model.objects.create_user(
        username="test3",
        password="123456",
        email="test3@py.com",
        role=performer_role,
        is_active=True
    )


@pytest.fixture
def superuser(django_user_model, performer_role):
    user = django_user_model.objects.create(
        username="test",
        password="test123456",
        email="test@test.com",
        is_superuser=True,
        role=performer_role
    )
    return user


@pytest.fixture
def backend():
    return JWTAuthentication()
