from jobs.models import Job
from authentication.api.serializers import UserPublicSerializer
from djmoney.contrib.django_rest_framework import MoneyField

from rest_framework import serializers


class JobListSerializer(serializers.ModelSerializer):
    price = MoneyField(
        max_digits=14,
        decimal_places=2,
    )
    author = UserPublicSerializer(read_only=True)

    class Meta:
        model = Job
        fields = (
            'id',
            'title',
            'description',
            'author',
            'price',
            'price_currency',
            'is_price_fixed',
            'views',
            'deadline'
        )


class JobDetailSerializer(serializers.ModelSerializer):
    price = MoneyField(
        max_digits=14,
        decimal_places=2,
    )
    author = UserPublicSerializer(read_only=True)

    class Meta:
        model = Job
        fields = '__all__'
