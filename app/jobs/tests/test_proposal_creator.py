import pytest
from moneyed.classes import Money
from datetime import date

from rest_framework.exceptions import ValidationError

from jobs.models import Proposal

pytestmark = [pytest.mark.django_db]


def test_proposal_creator_create_proposal(proposal_creator, job, superuser):
    proposal = proposal_creator(
        job=job,
        performer=superuser,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )()

    assert isinstance(proposal, Proposal)


def test_proposal_from_two_users(proposal_creator, job, superuser, active_user):
    proposal = proposal_creator(
        job=job,
        performer=superuser,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )()

    another_proposal = proposal_creator(
        job=job,
        performer=active_user,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )()

    assert isinstance(proposal, Proposal)
    assert isinstance(another_proposal, Proposal)


def test_one_user_can_create_only_one_propose_to_each_job(proposal_creator, job, superuser):
    proposal_creator(
        job=job,
        performer=superuser,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )()

    with pytest.raises(ValueError):
        proposal_creator(
            job=job,
            performer=superuser,
            description="ya wohl",
            price=Money(100500, 'USD'),
            deadline=date.today()
        )()


def test_cretor_send_mail_when_success(proposal_creator, job, superuser, mocker):
    creator = proposal_creator(
        job=job,
        performer=superuser,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )

    mocker.patch('jobs.creator.ProposalCreator.notify_creator')
    mocker.patch('jobs.creator.ProposalCreator.notify_performer')
    creator()

    creator.notify_creator.assert_called_once()
    creator.notify_performer.assert_called_once()


def test_creator_not_send_mail_when_proposal_not_created(proposal_creator, job, superuser, mocker):

    creator = proposal_creator(
        job=job,
        performer=superuser,
        description=1234,
        price='dengi',
        deadline=date.today()
    )

    mocker.patch('jobs.creator.ProposalCreator.notify_creator')
    mocker.patch('jobs.creator.ProposalCreator.notify_performer')
    with pytest.raises(ValidationError):
        creator()

        creator.notify_creator.assert_not_called()
        creator.notify_performer.assert_not_called()


def test_creator_job_is_required(proposal_creator, job, superuser,):
    with pytest.raises(ValueError):
        proposal_creator(
            job=None,
            performer=superuser,
            description="ya wohl",
            price=Money(100500, 'USD'),
            deadline=date.today()
        )
