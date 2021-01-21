import uuid
from typing import Optional, Union

from django.conf import settings

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Role, User


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
    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: int,
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

        self.verification_url = 'http://localhost:8080/verify/'
        self.extra_fields = True if len(kwargs) > 0 else False

    def __call__(self) -> User:
        user = self.create()

        if user is None:
            raise ValidationError("Cant create user")

        self.verify_email(
            user.email_verification_code,
            self.verification_url
        )
        self.subscribe()

        return user

    def create(self):
        try:
            if int(self.data['role']) == 1:
                self.user = self.get_user() or self.create_performer()

            elif int(self.data['role']) == 2:
                self.user = self.get_user() or self.create_employer()

            else:
                raise TypeError(f"No role with such id({self.data['role']})")
            return self.user
        except ValueError:
            raise ValidationError('Role must be integer like')

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

    def get_user(self) -> User:
        return User.objects.get_or_none(email=self.data['email'])

    def verify_email(
        self,
        verification_code: uuid,
        verification_link: str
    ) -> Union[int, None]:

        html_message = render_to_string(
            template_name='authentication/mail.html',
            context={
                'verification_link': verification_link,
                'verification_code': verification_code
            }
        )
        plain_message = strip_tags(html_message)

        _mail = send_mail(
            'Please verify your account',
            plain_message,
            settings.EMAIL_HOST_USER,
            [self.data['email']],
            fail_silently=False
        )

        return _mail

    def subscribe(self):
        pass
