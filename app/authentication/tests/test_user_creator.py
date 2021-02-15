from authentication.exceptions import EmailNotValid, UserRoleError
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


def test_creator_verify_email_is_called(mocker, creator, performer_role):
    user_creator = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )
    mocker.patch('authentication.creator.UserCreator.verify_email')

    user = user_creator()

    user_creator.verify_email.assert_called_once()
    assert isinstance(user, User)


def test_creator_verify_email_is_called_with_parametres(mocker, creator, performer_role):
    user_creator = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )
    mocker.patch('authentication.creator.UserCreator.verify_email')

    user = user_creator()

    user_creator.verify_email.assert_called_once_with(
        user.email_verification_code,
        'http://localhost:8080/verify/'
    )
    assert isinstance(user, User)


@pytest.mark.xfail(strict=True)
def test_creator_emit_common_create_method(mocker, creator, performer_role):
    user_creator = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )
    mocker.patch('authentication.creator.UserCreator.create')

    user_creator()

    user_creator.create.assert_called_once()


@pytest.mark.xfail(strict=True)
def test_creator_emit_correct_create_method(mocker, creator, performer_role):
    user_creator = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )
    mocker.patch('authentication.creator.UserCreator.create_performer')

    user_creator()

    user_creator.create_performer.assert_called_once()


def test_creator_not_emit_wrong_create_method(mocker, creator, performer_role):
    user_creator = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
    )
    mocker.patch('authentication.creator.UserCreator.create_employer')

    user = user_creator()

    user_creator.create_employer.assert_not_called()
    assert isinstance(user, User)


def test_creator_emit_subscribe_method(mocker, creator, performer_role):
    user_creator = creator(
        username='test',
        email='test@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id
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


def test_user_creator(creator, performer_role):
    user_creator = creator(
        username='test2',
        email='test2@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id,
        rating=10
    )
    user = user_creator()

    assert user.rating == 10


def test_superuser_always_active(superuser):
    assert superuser.is_active


def test_user_creator_create_user(creator, performer_role):
    creator(
        username='test2',
        email='test2@py.com',
        password='1234',
        first_name='oleh',
        last_name="pykulytsky",
        role=performer_role.id,
        rating=10
    )()

    assert User.objects.get_or_none(email='test2@py.com') is not None


@pytest.mark.skip
def test_user_creator_validate_email_address(creator, performer_role, settings):
    settings.DEBUG = False
    with pytest.raises(EmailNotValid):
        creator(
            username='test2',
            email='test2@py.com',
            password='1234',
            first_name='oleh',
            last_name="pykulytsky",
            role=performer_role.id,
            rating=10
        )()
