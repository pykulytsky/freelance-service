from datetime import date

import pytest
from jobs.models import Proposal
from moneyed.classes import Money
from rest_framework.exceptions import ValidationError

pytestmark = [pytest.mark.django_db]


def test_proposal_creator_create_proposal(proposal_creator, job, active_user):
    proposal = proposal_creator(
        job=job,
        performer=active_user,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )()

    assert isinstance(proposal, Proposal)


def test_proposal_from_two_users(proposal_creator, job, active_user, mixer, performer_role):
    proposal = proposal_creator(
        job=job,
        performer=active_user,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )()

    user = mixer.blend('authentication.User', is_active=True, role=performer_role)

    another_proposal = proposal_creator(
        job=job,
        performer=user,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )()

    assert isinstance(proposal, Proposal)
    assert isinstance(another_proposal, Proposal)


def test_one_user_can_create_only_one_propose_to_each_job(proposal_creator, job, active_user,):
    proposal_creator(
        job=job,
        performer=active_user,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )()

    with pytest.raises(ValueError):
        proposal_creator(
            job=job,
            performer=active_user,
            description="ya wohl",
            price=Money(100500, 'USD'),
            deadline=date.today()
        )()


def test_cretor_send_mail_when_success(proposal_creator, job, active_user, mocker):
    creator = proposal_creator(
        job=job,
        performer=active_user,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )

    mocker.patch('jobs.creator.ProposalCreator.notify_creator')
    mocker.patch('jobs.creator.ProposalCreator.notify_performer')
    creator()

    creator.notify_creator.assert_called_once()
    creator.notify_performer.assert_called_once()


def test_creator_not_send_mail_when_proposal_not_created(proposal_creator, job, active_user, mocker):

    creator = proposal_creator(
        job=job,
        performer=active_user,
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


def test_creator_job_is_required(proposal_creator, active_user,):
    with pytest.raises(ValueError):
        proposal_creator(
            job=None,
            performer=active_user,
            description="ya wohl",
            price=Money(100500, 'USD'),
            deadline=date.today()
        )
