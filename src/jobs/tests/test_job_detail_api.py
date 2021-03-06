import pytest
from django.urls import reverse
from jobs.models import Job

pytestmark = [pytest.mark.django_db]


def test_job_detail_api_success(api, job):
    url = reverse('job-detail', kwargs={'pk': job.id})

    response = api.patch(url, {
        'title': 'changed title'
    })

    assert response.status_code == 200


def test_job_detail_api_emit_save_method(api, job, mocker):
    url = reverse('job-detail', kwargs={'pk': job.id})
    mocker.patch('jobs.models.Job.save')

    response = api.patch(url, {
        'title': 'changed title'
    })

    assert response.status_code == 200
    job.save.assert_called_once()


def test_job_detail_api_access_not_author(api, another_job, mocker):
    url = reverse('job-detail', kwargs={'pk': another_job.id})
    mocker.patch('jobs.models.Job.save')

    with pytest.raises(PermissionError):
        api.patch(url, {
            'title': 'changed title'
        })

    another_job.save.assert_not_called()


def test_job_detail_api_change_field(api, job):
    url = reverse('job-detail', kwargs={'pk': job.id})

    response = api.patch(url, {
        'title': 'changed title'
    })

    assert response.status_code == 200
    assert Job.objects.get(id=job.id).title == 'changed title'


def test_job_detail_api_delete_record(api, job):
    url = reverse('job-detail', kwargs={'pk': job.id})

    response = api.delete(url)

    assert response.status_code == 204
    assert Job.objects.get_or_none(id=job.id) is None


def test_job_detail_api_get_record(api, job):
    url = reverse('job-detail', kwargs={'pk': job.id})

    response = api.get(url)

    assert response.status_code == 200
    assert response.data['description'] == job.description
    assert response.data['title'] == job.title
    assert response.data['deadline'] == job.deadline.strftime('%Y-%m-%d')


@pytest.mark.parametrize(
    'field,data',
    [
        ['title', 'changed title'],
        ['description', 'changed description'],
        ['deadline', '2020-09-09'],
        ['price', '100'],
        ['is_price_fixed', True],
        ['views', 255]
    ]
)
def test_job_detail_api_patch_each_field(api, job, field, data):
    url = reverse('job-detail', kwargs={'pk': job.id})

    response = api.patch(url, {field: data})

    if response.status_code == 400:
        assert False, response.data # noqa
    assert response.status_code == 200
    assert str(data) in eval(f'str(Job.objects.get(id=job.id).{field})')
