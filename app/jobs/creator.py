from datetime import date, datetime
from typing import Optional, Union

from rest_framework.exceptions import ValidationError
from authentication.models import User
from rest_framework import serializers

from djmoney.money import Money

from .models import Job
from chat.models import Room
from .tasks import send_email_after_create_job

from authentication.exceptions import UserNotActive


class JobCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ('performer', )


class JobCreator:
    def __init__(
        self,
        author: User,
        title: str,
        description: str,
        price: Money,
        is_price_fixed: bool,
        deadline: Union[date, str],
        plan: Optional[int] = None
    ) -> None:
        self.data = {
            'title': title,
            'description': description,
            'author': author.id,
            'price': price,
            'is_price_fixed': is_price_fixed,
            'deadline': deadline,
            'plan': plan
        }
        if isinstance(deadline, str):
            self.data.update({
                'deadline': datetime.strptime(deadline, '%Y-%m-%d').date(),
            })

        self.author = author

        if not author.is_active:
            raise UserNotActive("User must be active to create job")

    def __call__(self):
        self.room = self.create_room()
        self.job = self.create()
        self.notify_creator()

        return self.job

    def create_room(self):
        room = Room.objects.update_or_create(
            name=f'{self.data["title"]}:{self.author.username}'
        )
        self.data.update({
            'chat_room': room[0].id
        })

        return room

    def create(self) -> Optional[Job]:
        serializer = JobCreateSerializer(data=self.data)
        if serializer.is_valid():
            serializer.save()

            return serializer.instance
        else:
            raise ValidationError(serializer.errors)

    def notify_creator(self):
        _mail = send_email_after_create_job.delay(
            self.author.email,
            datetime.now().strftime("%m/%d/%Y %H:%M"),
            self.data['title'],
            self.data['deadline'].strftime("%d/%m/%Y")
        )

        return _mail.collect()
