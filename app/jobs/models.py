from django.db import models
from behaviors.behaviors import Timestamped
import authentication.validators as custom_validators

from authentication.models import User

from chat.models import Room

from djmoney.models.fields import MoneyField


class Job(Timestamped):
    title = models.CharField(
        max_length=1024,
        verbose_name="Job name")
    description = models.CharField(max_length=8192)

    deadline = models.DateField()

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



    class Meta:
        unique_together = ('author', 'performer')


class FavoritesJobs(Timestamped):
    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name="favorites_list")

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorites_jobs"
    )

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
