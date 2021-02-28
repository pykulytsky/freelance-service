from authentication.models import User
from rest_framework.authentication import authenticate
from rest_framework import serializers

from authentication.utils import set_login_time

from django.shortcuts import get_object_or_404


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('id',
                  'email',
                  'username',
                  'password',
                  'first_name',
                  'last_name',
                  'token',)

    def create(self, validated_data) -> User:
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    pk = serializers.IntegerField(read_only=True)

    def validate(self, validation_data) -> dict:
        email = validation_data.get('email', None)
        password = validation_data.get('password', None)

        if email is None:
            raise serializers.ValidationError("No email provided")

        if password is None:
            serializers.ValidationError("No email provided")

        user = authenticate(username=email, password=password)
        if user:
            set_login_time(user)

        if user is None:
            raise serializers.ValidationError("No such user found.")

        if not user.is_active:
            raise serializers.ValidationError("User is not active")

        return {
            'token': user.token,
            'pk': user.pk
        }


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'age',
            'first_name',
            'last_name',
            'avatar',
            'total_jobs_completed',
            'rating',
            'role',
            'user_verified'
        )


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class PasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']


class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']

    def validate(self, validation_data):
        email = validation_data.get('email', None)
        get_object_or_404(User, email=email)

        return {
            'status': 'password reset'
        }
