from typing import Dict, Tuple
from django.db import models
from django.conf import settings
from django.core import validators
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
import authentication.validators as custom_validators

from django.core.exceptions import ObjectDoesNotExist

from jwt.exceptions import *
import jwt
import uuid

from datetime import datetime
from datetime import timedelta

from django_countries.fields import CountryField
from creditcards.models import CardNumberField, CardExpiryField, SecurityCodeField

from django.utils.translation import gettext as _


class BaseAuthManager(BaseUserManager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class UserManager(BaseAuthManager):
    """Class calls when calls User.objects"""

    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError(_("The user does not have a name."))
        if not email:
            raise ValueError(_("No email specified."))

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('The superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('The superuser must have is_superuser=True.'))

        return self._create_user(username, email, password, **extra_fields)

    def delete(self) -> Tuple[int, Dict[str, int]]:
        from .mailchimp.client import AppMailchimp

        client = AppMailchimp()
        client.delete_list_member(settings.MAILCHIMP_AUDIENCE_ID, self.model)

        return super().delete()


class Role(models.Model):
    objects = BaseAuthManager()

    PERFORMER = 1
    EMPLOYER = 2
    AGENCY_PERFORMER = 3

    ROLE_CHOISES = (
        (PERFORMER, 'performer'),
        (EMPLOYER, 'employer'),
        (AGENCY_PERFORMER, 'agency_performer'),
    )

    id = models.PositiveSmallIntegerField(
        choices=ROLE_CHOISES,
        primary_key=True)

    def __str__(self):
        return self.get_id_display()


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True,
                                max_length=255,
                                unique=True)
    email = models.EmailField(validators=[validators.validate_email],
                              unique=True,
                              blank=False)

    age = models.IntegerField(
        validators=[custom_validators.validate_age, ],
        verbose_name='Age',
        blank=True, null=True)

    first_name = models.CharField(max_length=255, blank=True, verbose_name="First Name")

    last_name = models.CharField(max_length=255,
                                 blank=True,
                                 verbose_name="Last Name")

    avatar = models.ImageField(upload_to="assets/avatars/",
                               blank=True)
    avatar_url = models.URLField(blank=True, null=True)

    total_jobs_completed = models.PositiveIntegerField(default=0)

    rating = models.PositiveSmallIntegerField(
        validators=[custom_validators.rating_validator, ], verbose_name="Rating",
        default=0)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # User is not active until he verify his email
    is_active = models.BooleanField(default=False)

    email_verified = models.BooleanField(default=False)
    email_verification_code = models.UUIDField(max_length=32,
                                               default=uuid.uuid4,
                                               editable=False)
    subscribe_to_mailing = models.BooleanField(default=False)

    role = models.ForeignKey(
        Role,
        related_name="users",
        on_delete=models.PROTECT)
    user_verified = models.BooleanField(
        blank=True,
        null=True
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    country = CountryField(blank=True)

    card_number = CardNumberField('Card Number', blank=True, null=True)
    card_expiry = CardExpiryField('Expiration Date', blank=True, null=True)
    card_code = SecurityCodeField('CVV/CVC', blank=True, null=True)

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()

        if self.is_superuser and self.is_staff:
            self.is_active = True

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_full_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.username

    def get_short_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return self.username

    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        try:
            token = jwt.encode({
                'id': self.pk,
                'exp': dt.timestamp(),
                'role': self.role.id,
                'is_superuser': int(self.is_superuser)
            }, settings.SECRET_KEY, algorithm='HS256')
        except (InvalidTokenError, InvalidAlgorithmError,
                InvalidAudienceError, ExpiredSignatureError, ImmatureSignatureError, PyJWTError):
            raise ValueError("Error occured while generating jwt token")

        return token.decode('utf-8')


class Company(models.Model):
    name = models.CharField(
        max_length=512,
        verbose_name="Company name")

    country = CountryField()
    address = models.CharField(
        max_length=1024,
        verbose_name="Adress")


class Agency(models.Model):
    pass
