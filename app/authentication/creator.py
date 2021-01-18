from attr import fields
from django.conf import settings
from .models import User, Role
from rest_framework import serializers

from django.core.mail import send_mail
from django.template.loader import render_to_string

from typing import Union, Optional, Any

import uuid

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            'id'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'first_name',
            'last_name'
            'role'
        ]

class UserCreator:
    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        first_name: str,
        last_name: str,
        role: int) -> None:
        
        self.data = {
            'username': username,
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'role': role
        }

    def __call__(self) -> User:
        if self.role == 1:
            self.user = self.get_user() or self.create_performer(self.data)
        
        if self.role == 2:
            self.user = self.get_user() or self.create_employer(self.data)

        
        return self.user
    
    def create_performer(self, user_data) -> Optional[User]:
        serializer = UserCreateSerializer(user_data)

        if serializer.is_valid():
            serializer.save()

            self.verify_email(
                serializer.instance.email_verification_code,
                'http://localhost:8080/verify/')
            
            return serializer.instance

    def create_employer(self, user_data) -> Optional[User]:
        serializer = UserCreateSerializer(user_data)

        if serializer.is_valid():
            serializer.save()

            self.verify_email(
                serializer.instance.email_verification_code,
                'http://localhost:8080/verify/')

            return serializer.instance

    def get_user(self) -> User:
        return User.objects.get_or_none(email=self.email)

    def verify_email(
        self,
        verification_code: uuid,
        verification_link: str) -> Union[int, None]:
        _mail = send_mail(
            'Please verify your account',
            render_to_string(
                template_name='authentication/mail.html',
                context={
                    'verification_link': verification_link,
                    'verification_code': verification_code
                }),
            settings.EMAIL_HOST_USER,
            [self.data['email'] ],
            fail_silently=False
        )
        
        return _mail
        
    def subscribe(self):
        pass
