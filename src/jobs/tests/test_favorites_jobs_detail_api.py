import pytest
from django.urls import reverse

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def list_api_response(api, favorite_list):
    url = reverse('favorites-jobs-list')

    return api.get(url)


@pytest.fixture
def detail_api_response(api, job, favorite_list):
    url = reverse('favorites-jobs-detail', kwargs={'id': job.id})

    return api.post(url)


def test_favorite_access_list_success(list_api_response):
    assert list_api_response.status_code == 200


def test_favorite_list_empty(list_api_response):
    assert list_api_response.data == []


def test_add_job_to_favorite(detail_api_response):
    assert detail_api_response.status_code == 200


def test_fill_favorites_list(list_api_response, detail_api_response):
    assert detail_api_response.data != []


def test_fill_favorites_list_data(list_api_response, detail_api_response, job):
    assert detail_api_response.data['title'] == job.title
    assert detail_api_response.data['description'] == job.description
    assert detail_api_response.data['author']['username'] == job.author.username
