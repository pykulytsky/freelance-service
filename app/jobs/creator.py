from datetime import date, datetime
from typing import Optional, Union

from rest_framework.exceptions import ValidationError
from authentication.models import User
from rest_framework import serializers

from djmoney.money import Money

from .models import Job, Proposal
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
        plan: Optional[int] = None,
        **kwargs
    ) -> None:
        self.data = {
            'title': title,
            'description': description,
            'author': author.id,
            'price': price,
            'is_price_fixed': is_price_fixed,
            'deadline': deadline,
            'plan': plan,
            **kwargs
        }
        if isinstance(deadline, str):
            self.data.update({
                'deadline': datetime.strptime(deadline, '%Y-%m-%d').date(),
            })

        self.author = author

        if not author.is_active:
            raise UserNotActive("User must be active to create job")

    def __call__(self) -> Job:
        self.room = self.create_room()
        self.job = self.create()

        if self.job is not None:
            self.notify_creator()

        return self.job

    def create_room(self) -> Room:
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

    def notify_creator(self) -> Union[int, None]:
        _mail = send_email_after_create_job.delay(
            self.author.email,
            datetime.now().strftime("%m/%d/%Y %H:%M"),
            self.data['title'],
            self.data['deadline'].strftime("%d/%m/%Y")
        )

        return _mail.collect()


class ProposalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = '__all__'


class ProposalCreator:
    def __init__(
        self,
        job: Job,
        performer: User,
        description: str,
        price: Union[Money, str],
        deadline: date,
        **kwargs
    ) -> None:
        if isinstance(job, Job):
            for proposal in job.proposals.all():
                if proposal.performer == performer:
                    raise ValueError("1 performer can send only 1 proposal to 1 job")
        else:
            raise ValueError("Job is required.")

        self.data = {
            'job': job.id,
            'performer': performer.id,
            'description': description,
            'price': price,
            'deadline': deadline
        }

    def __call__(self) -> Proposal:
        self.propose = self.create()

        if self.propose is not None:
            self.notify_creator()
            self.notify_performer()

        return self.propose

    def create(self) -> Proposal:
        serializer = ProposalCreateSerializer(data=self.data)
        if serializer.is_valid():
            serializer.save()

            return serializer.instance
        else:
            raise ValidationError(f"Can`t create propose, data not valid - [{serializer.errors}]")

    def notify_creator(self) -> Union[int, None]:
        pass

    def notify_performer(self) -> Union[int, None]:
        pass
