import pytest
from moneyed.classes import Money
from datetime import date

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


def test_proposal_from_two_users(proposal_creator, job, superuser, user):
    proposal = proposal_creator(
        job=job,
        performer=superuser,
        description="ya wohl",
        price=Money(100500, 'USD'),
        deadline=date.today()
    )()

    another_proposal = proposal_creator(
        job=job,
        performer=user,
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
