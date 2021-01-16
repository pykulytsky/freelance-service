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



# Create your models here.
class UserManager(BaseUserManager):
    """Class calls when calls User.objects"""

    def _create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("В користувача не встановлено ім’я.")
        if not email:
            raise ValueError("Не вказано електронну пошту.")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперкористувач повинен мати is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперкористувач повинен мати is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class Role(models.Model):

    



class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True,
                                max_length=255,
                                unique=True)
    email = models.EmailField(validators=[validators.validate_email],
                              unique=True,
                              blank=False)

    age = models.IntegerField(validators=[custom_validators.validate_age, ], verbose_name='Age', blank=True, null=True)
    last_name = models.CharField(max_length=255,
                                 blank=True,
                                 verbose_name="Last Name")
    first_name = models.CharField(max_length=255, blank=True, verbose_name="First Name")

    avatar = models.ImageField(upload_to="assets/avatars/",
                               default="noimage.png")

    avatar_url = models.URLField(blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    email_verified = models.BooleanField(default=False)
    email_verification_code = models.UUIDField(max_length=32,
                                               default=uuid.uuid4,
                                               editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    country = models.CharField(max_length=128)

    objects = UserManager()

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.capitalize()
        self.last_name = self.last_name.capitalize()
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
                'exp': dt.timestamp()
            }, settings.SECRET_KEY, algorithm='HS256')
        except (InvalidTokenError, DecodeError, InvalidAlgorithmError,
                InvalidAudienceError, ExpiredSignatureError, ImmatureSignatureError,
                InvalidIssuedAtError, InvalidIssuerError, ExpiredSignature,
                InvalidAudience, InvalidIssuer, MissingRequiredClaimError,
                InvalidSignatureError,
                PyJWTError):
            raise ValueError("Error occured while generating jwt token")

        return token.decode('utf-8')
