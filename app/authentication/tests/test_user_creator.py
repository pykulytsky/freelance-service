from authentication.models import User
import pytest

pytestmark = [pytest.mark.django_db]


def test_creator_initialization(creator, performer_role):
    user_creator = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )

    assert user_creator.data['username'] == 'test'


def test_creator_create_user_with_role_with_create_method(creator, performer_role):
    user_creator = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )

    user = user_creator.create()

    assert isinstance(user, User)

    
def test_creator_create_user_with_role(creator, performer_role):
    user = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )()

    assert isinstance(user, User)


def test_creator_create_user_with_role_with_already_used_credentials(creator, performer_role):
    user = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )()

    another_user = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )()

    assert isinstance(user, User)
    assert isinstance(another_user, User)

    assert user == another_user

