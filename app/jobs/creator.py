from datetime import datetime
from authentication.models import User
from rest_framework import serializers

from djmoney.money import Money

from .models import Job
from chat.models import Room


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class JobCreator:
    def __init__(
        self,
        author: User,
        title: str,
        description: str,
        price: Money,
        is_price_fixed: bool,
        deadline: datetime,
        plan: int
    ) -> None:
        self.data = {
            'title': title,
            'description': description,
            'author': author,
            'price': price,
            'is_fixed_price': is_price_fixed,
            'dedline': deadline,
            'plan': plan
        }

        if not self.data['author'].is_active:
            raise ValueError("User must be active to create job")

    def __call__(self):

        self.room = self.create_room()

    def create_room(self):
        return Room.objects.update_or_create(
            name=f'{self.data["title"]}:{self.data["author"].username}'
        )

    def create(self):
        raise NotImplementedError

    def notify_creator(self):
        raise NotImplementedError
