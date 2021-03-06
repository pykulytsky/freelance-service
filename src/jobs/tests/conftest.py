import pytest
from authentication.models import Role
from jobs.creator import JobCreator, ProposalCreator
from jobs.models import FavoritesJobs
from mixer.backend.django import mixer as _mixer
from PIL import Image
from rest_framework.test import APIClient


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
def superuser(django_user_model, employer_role, mixer, image):
    return mixer.blend(
        django_user_model,
        role=employer_role,
        is_superuser=True,
        si_staff=True,
        is_active=True,
        avatar=image)


@pytest.fixture
def active_user(django_user_model, performer_role, mixer, image):
    return mixer.blend(
        django_user_model,
        role=performer_role,
        is_active=True,
        avatar=image
    )


@pytest.fixture
def user(django_user_model, performer_role, mixer, image):
    return mixer.blend(
        django_user_model,
        role=performer_role,
        is_active=True,
        avatar=image
    )


@pytest.fixture
def active_api(active_user):
    client = APIClient()

    token = active_user.token
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    return client


@pytest.fixture
def creator():
    return JobCreator


@pytest.fixture
def performer_role():
    return Role.objects.create(id=1)


@pytest.fixture
def employer_role():
    return Role.objects.create(id=2)


@pytest.fixture
def job(mixer, superuser):
    return mixer.blend('jobs.Job', author=superuser)


@pytest.fixture
def another_job(mixer, active_user):
    return mixer.blend('jobs.Job', author=active_user)


@pytest.fixture
def favorite_list(superuser):
    return FavoritesJobs.objects.create(user=superuser)


@pytest.fixture
def proposal_creator():
    return ProposalCreator


@pytest.fixture
def proposal(superuser, mixer, job):
    return mixer.blend('jobs.Proposal', performer=superuser, job=job)
