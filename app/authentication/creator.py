from typing import Optional, Union

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Role, User
from .tasks import send_verification_email_by_sendgrid
from .exceptions import *

from .mailboxlayer import validate_email
from django.conf import settings

from jobs.models import FavoritesJobs

from authentication.mailchimp.client import AppMailchimp


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id'
        ]


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'role'
        ]


class UserCreateDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserCreator:
    """Service object for create user."""
    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: int,
        confirm_subscribe: bool = False,
        **kwargs
    ) -> None:

        self.data = {
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'role': role,
            **kwargs
        }
        self.confirm_subscribe = confirm_subscribe

        self.verification_url = 'http://localhost:8080/verify/'
        self.extra_fields = True if len(kwargs) > 0 else False

    def __call__(self) -> User:
        user = self.create()

        if user is None:
            raise ValidationError("Can`t create user")

        if settings.DEBUG is False:
            if validate_email(self.data['email']):
                self.verify_email()
            else:
                raise EmailNotValid("Your email is not valid.")
        else:
            self.verify_email()
        if self.confirm_subscribe:
            self.subscribe()
        self.create_favorite_jobs_list()

        return user

    def create(self) -> Union[User, None]:
        try:
            if int(self.data['role']) == 1:
                self.user = self._user or self.create_performer()

            elif int(self.data['role']) == 2:
                self.user = self._user or self.create_employer()

            else:
                raise UserRoleError(f"No role with such id({self.data['role']})")
            return self.user
        except ValueError:
            raise UserRoleError('Role must be integer like')

    def create_performer(self) -> Optional[User]:
        serializer = UserCreateDetailSerializer(data=self.data)

        if serializer.is_valid():
            serializer.save()

            return serializer.instance
        else:
            raise ValidationError(serializer.errors)

    def create_employer(self) -> Optional[User]:
        serializer = UserCreateDetailSerializer(data=self.data)

        if serializer.is_valid():
            serializer.save()

            return serializer.instance
        else:
            raise ValidationError(serializer.errors)

    @property
    def _user(self) -> User:
        return User.objects.get_or_none(email=self.data['email'])

    def verify_email(self) -> Union[int, None]:
        send_verification_email_by_sendgrid.delay(self._user.id)

    def subscribe(self):
        if not settings.DEBUG and self.subscribe:
            client = AppMailchimp()
            audience_id = settings.MAILCHIMP_AUDIENCE_ID

            client.subscribe_django_user(audience_id, self._user)

    def create_favorite_jobs_list(self) -> FavoritesJobs:
        return FavoritesJobs.objects.update_or_create(user=self._user)
