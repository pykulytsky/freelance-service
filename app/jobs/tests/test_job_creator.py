from chat.models import Room
from authentication.models import User
from jobs.models import Job
import pytest
from djmoney.money import Money

pytestmark = [pytest.mark.django_db]


def test_job_creator_create_job(creator, superuser):
    job = creator(
        author=superuser,
        title='write binary tree generator with css',
        description='it`s ez',
        price=Money(100500, 'USD'),
        is_price_fixed=True
    )()

    assert isinstance(job, Job)
    assert Job.get_or_none(title='write binary tree generator with css') is not None


def test_job_correct_author(creator, superuser):
    job = creator(
        author=superuser,
        title='write binary tree generator with css',
        description='it`s ez',
        price=Money(100500, 'USD'),
        is_price_fixed=True
    )()

    assert isinstance(job.author, User)
    assert job.author == superuser


def test_job_auhtor_must_be_active(creator, superuser):
    job = creator(
        author=superuser,
        title='write binary tree generator with css',
        description='it`s ez',
        price=Money(100500, 'USD'),
        is_price_fixed=True
    )()

    assert job.author.is_active


def test_job_creator_send_mail_to_creator(creator, superuser, mocker):
    job_creator = creator(
        author=superuser,
        title='write binary tree generator with css',
        description='it`s ez',
        price=Money(100500, 'USD'),
        is_price_fixed=True
    )

    mocker.patch('jobs.creator.JobCreator.notify_creator')

    job_creator()

    assert job_creator.notify_creator.assert_called_once()


def test_job_creator_call_create_room_method(creator, superuser, mocker):
    job_creator = creator(
        author=superuser,
        title='write binary tree generator with css',
        description='it`s ez',
        price=Money(100500, 'USD'),
        is_price_fixed=True
    )

    mocker.patch('jobs.creator.JobCreator.create_room')

    job_creator()

    assert job_creator.create_room.assert_called_once()


def test_job_creator_create_room(creator, superuser):
    creator(
        author=superuser,
        title='write binary tree generator with css',
        description='it`s ez',
        price=Money(100500, 'USD'),
        is_price_fixed=True
    )()

    assert Room.objects.get_or_none(name=f'write binary tree generator with css:{superuser.username}')
