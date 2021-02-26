from authentication.exceptions import EmailNotValid, UserRoleError
from authentication.models import User
import pytest

from authentication.tasks import send_verification_email_by_sendgrid

from django.conf import settings

pytestmark = [pytest.mark.django_db]


@pytest.fixture
def user_data(performer_role):
    return {
        'username': 'test',
        'email': 'test@py.com',
        'password': '1234',
        'first_name': 'oleh',
        'last_name': "pykulytsky",
        'role': performer_role.id
    }


def test_creator_initialization(creator, user_data):
    user_creator = creator(
        **user_data
    )

    assert user_creator.data['username'] == 'test'


def test_creator_create_user_with_role_with_create_method(creator, user_data):
    user_creator = creator(
        **user_data
    )

    user = user_creator.create()

    assert isinstance(user, User)


def test_creator_create_user_with_role(creator, user_data):
    user = creator(
        **user_data
    )()

    assert isinstance(user, User)


def test_creator_create_user_with_role_with_already_used_credentials(creator, user_data):
    user = creator(
        **user_data
    )()

    another_user = creator(
        **user_data
    )()

    assert isinstance(user, User)
    assert isinstance(another_user, User)

    assert user == another_user


def test_creator_verify_email_is_called(mocker, creator, user_data):
    user_creator = creator(
        **user_data
    )
    mocker.patch('authentication.creator.UserCreator.verify_email')

    user = user_creator()

    user_creator.verify_email.assert_called_once()
    assert isinstance(user, User)


def test_creator_verify_email_is_called_with_parametres(mocker, creator, user_data):
    user_creator = creator(
        **user_data
    )
    mocker.patch('authentication.tasks.send_verification_email_by_sendgrid.delay')

    user = user_creator()

    send_verification_email_by_sendgrid.delay.assert_called_once_with(user.id)
    assert isinstance(user, User)


@pytest.mark.xfail(strict=True)
def test_creator_emit_common_create_method(mocker, creator, user_data):
    user_creator = creator(
        **user_data
    )
    mocker.patch('authentication.creator.UserCreator.create')

    user_creator()

    user_creator.create.assert_called_once()


@pytest.mark.xfail(strict=True)
def test_creator_emit_correct_create_method(mocker, creator, user_data):
    user_creator = creator(
        **user_data
    )
    mocker.patch('authentication.creator.UserCreator.create_performer')

    user_creator()

    user_creator.create_performer.assert_called_once()


def test_creator_not_emit_wrong_create_method(mocker, creator, user_data):
    user_creator = creator(
        **user_data
    )
    mocker.patch('authentication.creator.UserCreator.create_employer')

    user = user_creator()

    user_creator.create_employer.assert_not_called()
    assert isinstance(user, User)


def test_creator_emit_subscribe_method(mocker, creator, user_data):
    user_creator = creator(
        **user_data
    )
    mocker.patch('authentication.creator.UserCreator.subscribe')

    user = user_creator()

    user_creator.subscribe.assert_called_once()
    assert isinstance(user, User)


def test_user_creator_not_enought_fields(creator, performer_role):
    with pytest.raises(TypeError):
        creator(
            username='test',
            email='test@py.com',
            password='1234',
            role=performer_role.id
        )()


def test_user_creator_wrong_role(creator):
    with pytest.raises(UserRoleError) as role_error:
        creator(
            username='test',
            email='test@py.com',
            password='1234',
            first_name='oleh',
            last_name="pykulytsky",
            role=100500
        )()

    assert "No role with such id" in str(role_error.value)


def test_user_creator(creator, user_data):
    user_creator = creator(
        **user_data,
        rating=10
    )
    user = user_creator()

    assert user.rating == 10


def test_superuser_always_active(superuser):
    assert superuser.is_active


def test_user_creator_create_user(creator, user_data):
    creator(
        **user_data,
        rating=10
    )()

    assert User.objects.get_or_none(email='test@py.com') is not None


@pytest.mark.skipif(settings.DEBUG is True, reason="Free account is limited for use API")
def test_user_creator_validate_email_address(creator, user_data, settings):
    settings.DEBUG = False
    with pytest.raises(EmailNotValid):
        creator(
            **user_data,
            rating=10
        )()
