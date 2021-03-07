from jobs.models import Job, Proposal
import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def proposal(mixer, job, active_user):
    return mixer.blend('jobs.Proposal', performer=active_user, job=job)


@pytest.fixture
def another_proposal(mixer, job, user):
    return mixer.blend('jobs.Proposal', performer=user, job=job)


def test_approve_proposal(api, job, proposal):
    url = reverse('job-approve', kwargs={'pk': job.id})

    response = api.post(url, {'proposal_id': proposal.id})

    assert response.status_code == 200
    assert Job.objects.get(id=job.id).has_performer is True


def test_attempt_approve_proposal_on_job_with_already_approved_proposal(api, job, proposal, another_proposal):
    url = reverse('job-approve', kwargs={'pk': job.id})
    response = api.post(url, {'proposal_id': proposal.id})
    assert response.status_code == 200

    url = reverse('job-approve', kwargs={'pk': job.id})
    response = api.post(url, {'proposal_id': another_proposal.id})
    assert response.status_code == 400


def test_done_job(api, job, proposal):
    url = reverse('job-approve', kwargs={'pk': job.id})
    api.post(url, {'proposal_id': proposal.id})

    url = reverse('job-done', kwargs={'pk': job.id})
    response = api.post(url)

    assert response.status_code == 200
    assert Job.objects.get(id=job.id).done is True
    assert Job.objects.get(id=job.id).published is False
