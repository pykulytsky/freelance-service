import pytest

pytestmark = [pytest.mark.django_db]


def test_request(api):
    