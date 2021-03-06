import pytest
from authentication.creator import UserCreateSerializer

pytestmark = [pytest.mark.django_db]


def test_creator(creator, performer_role):
    user_creator = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )

    assert user_creator.data['username'] == 'test'
    assert user_creator.data['role'] == 1


def test_creator_user_serializer_is_work(performer_role):
    user_data = {
        'username': 'test',
        'email': 'test@py.com',
        'password': '1234',
        'first_name': 'oleh',
        'last_name': "pykulytsky",
        'role': performer_role.id
    }

    serializer = UserCreateSerializer(data=user_data)

    assert serializer.is_valid()
    serializer.save()
    assert serializer.errors == {}


def test_creator_user_serializer_role_data(performer_role):
    user_data = {
        'username': 'test',
        'email': 'test@py.com',
        'password': '1234',
        'first_name': 'oleh',
        'last_name': "pykulytsky",
        'role': performer_role.id
    }

    serializer = UserCreateSerializer(data=user_data)

    assert serializer.is_valid()
    serializer.save()
    assert serializer.data['role'] == 1


def test_creator_user_serializer_user_data(performer_role):
    user_data = {
        'username': 'test',
        'email': 'test@py.com',
        'password': '1234',
        'first_name': 'oleh',
        'last_name': "pykulytsky",
        'role': performer_role.id
    }

    serializer = UserCreateSerializer(data=user_data)

    assert serializer.is_valid()
    serializer.save()
    assert serializer.data['username'] == 'test'
    assert serializer.data['email'] == 'test@py.com'


def test_creator_user_serializer_name_capitalizee(performer_role):
    user_data = {
        'username': 'test',
        'email': 'test@py.com',
        'password': '1234',
        'first_name': 'oleh',
        'last_name': "pykulytsky",
        'role': performer_role.id
    }

    serializer = UserCreateSerializer(data=user_data)

    assert serializer.is_valid()
    serializer.save()

    assert serializer.data['first_name'] != 'oleh'
    assert serializer.data['first_name'] == 'Oleh'
    assert serializer.data['last_name'] != 'pykulytsky'
    assert serializer.data['last_name'] == 'Pykulytsky'
