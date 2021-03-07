from typing import Optional
import authentication.validators as custom_validators
from app.mixins import ModelChangeDetectMixin
from authentication.models import User
from behaviors.behaviors import Timestamped
from chat.models import Room
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.manager import Manager
from djmoney.models.fields import MoneyField
from .exceptions import JobAlreadyApproveProposal, JobAlreadyDoneErorr


class BaseJobManager(Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class Job(Timestamped, ModelChangeDetectMixin):
    title = models.CharField(
        max_length=1024,
        verbose_name="Job name")
    description = models.CharField(max_length=8192)

    deadline = models.DateField(blank=True)

    author = models.ForeignKey(
        User,
        related_name="created_jobs",
        on_delete=models.CASCADE)
    performer = models.ForeignKey(
        User,
        related_name="performed_jobs",
        on_delete=models.CASCADE,
        blank=True,
        null=True)

    price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='USD'
    )
    is_price_fixed = models.BooleanField()

    chat_room = models.OneToOneField(
        Room,
        related_name="job",
        on_delete=models.PROTECT
    )

    views = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False)
    has_performer = models.BooleanField(default=False)
    done = models.BooleanField(default=False)

    objects = BaseJobManager()

    @property
    def approved_proposal(self) -> Optional['Proposal']:
        proposal = self.proposals.filter(approved=True)
        if proposal and len(proposal) < 2:
            return proposal.first()

    def approve_proposal(self, proposal_id):
        if not self.approved_proposal:
            _proposal = self.proposals.get(id=proposal_id)
            _proposal.approve()
            self.has_performer = True
            self.save()
            return _proposal
        else:
            raise JobAlreadyApproveProposal(f"Proposal {self.approved_proposal.id} already approved on this job.")

    def confirm_done(self):
        if not self.done and self.approved_proposal:
            self.done = True
            self.published = False

            self.save()
        else:
            raise JobAlreadyDoneErorr("This job is already done")

    class Meta:
        unique_together = ('author', 'performer')


class FavoritesJobs(Timestamped):
    jobs = models.ManyToManyField(
        Job,
        related_name="favorites_list")

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="favorites_jobs"
    )

    objects = BaseJobManager()


class AttachedFile(models.Model):
    file = models.FileField(upload_to="files/")
    job = models.ForeignKey(
        Job,
        related_name="files",
        on_delete=models.CASCADE)


class Feedback(Timestamped):
    body = models.CharField(max_length=8192)
    rating = models.PositiveSmallIntegerField(
        validators=[custom_validators.rating_validator, ]
    )

    author = models.ForeignKey(
        User,
        related_name="created_feedback",
        on_delete=models.PROTECT)

    performer = models.ForeignKey(
        User,
        related_name="received_feedback",
        on_delete=models.CASCADE)

    job = models.ForeignKey(
        Job,
        related_name="feedback",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('author', 'performer')


class Proposal(Timestamped):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="proposals"
    )
    performer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="proposals"
    )
    approved = models.BooleanField(default=False)
    description = models.CharField(max_length=2048)

    price = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency='USD'
    )
    deadline = models.DateField(blank=True)

    def approve(self):
        self.approved = True
        self.save()
