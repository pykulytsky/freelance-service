from datetime import date

import pytest
from django.urls import reverse
from jobs.models import Job
from jobs.tasks import send_email_after_create_job

pytestmark = [pytest.mark.django_db]


def test_jobs_api_list(api):
    url = reverse('job-list')

    response = api.get(url)

    assert response.status_code == 200


def test_jobs_list_api_data(api, mixer):
    url = reverse('job-list')
    mixer.cycle(3).blend('jobs.Job')

    response = api.get(url)

    assert response.status_code == 200
    assert len(response.data) == 3


def test_jobs_list_api_create_job_count(api, mixer, superuser):
    url = reverse('job-list')
    mixer.blend('jobs.Job', author=superuser)

    response = api.get(url)

    assert response.status_code == 200
    assert len(Job.objects.all()) > 0


def test_create_job_api_success(api):
    url = reverse('job-list')

    response = api.post(url, {
        'title': 'test',
        'description': 'test description',
        'price': 100500,
        'deadline': date.today(),
        'is_price_fixed': True
    })

    assert response.status_code == 201


def test_create_job_api_create_job(api):
    url = reverse('job-list')

    response = api.post(url, {
        'title': 'test',
        'description': 'test description',
        'price': 100500,
        'deadline': date.today(),
        'is_price_fixed': True
    })

    assert response.status_code == 201
    assert Job.objects.get_or_none(title='test') is not None


def test_create_job_api_emit_creator_send_email_task(api, mocker):
    url = reverse('job-list')
    mocker.patch('jobs.tasks.send_email_after_create_job.delay')

    response = api.post(url, {
        'title': 'test',
        'description': 'test description',
        'price': 100500,
        'deadline': date.today(),
        'is_price_fixed': True
    })

    assert response.status_code == 201
    send_email_after_create_job.delay.assert_called_once()


def test_none_employer_create_job(active_api, mocker):
    url = reverse('job-list')
    mocker.patch('jobs.tasks.send_email_after_create_job.delay')

    response = active_api.post(url, {
        'title': 'test',
        'description': 'test description',
        'price': 100500,
        'deadline': date.today(),
        'is_price_fixed': True
    })

    assert response.status_code == 400
    send_email_after_create_job.delay.assert_not_called()
