import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


def test_list_api_success(api):
    url = reverse('proposals-list')

    response = api.get(url)

    assert response.status_code == 200


def test_list_api_data(api, proposal, superuser, job):
    url = reverse('proposals-list')

    response = api.get(url)

    assert len(response.data) == 1
    assert response.data[0]['performer']['username'] == superuser.username
    assert response.data[0]['description'] == proposal.description
    assert response.data[0]['job']['description'] == job.description


def test_create_api_success(api, active_user, job):
    url = reverse('proposals-list')

    response = api.post(
        url,
        {
            'performer': active_user.id,
            'description': 'test',
            'price': 100500,
            'price_currency': 'USD',
            'deadline': '2020-01-01',
            'job': job.id
        }
    )

    assert response.status_code == 201
