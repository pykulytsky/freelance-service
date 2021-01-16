from django.db import models
from behaviors.behaviors import Timestamped
import authentication.validators as custom_validators
from authentication.models import User


class Job(Timestamped):
    title = models.CharField(
        max_length=1024,
        verbose_name="Job name")
    description = models.CharField(max_length=8192)

    deadline = models.DateField()


class AttachedFile(models.Model):
    file = models.FileField(upload_to="/files/")
    job = models.ForeignKey(
        Job,
        related_name="files",
        on_delete=models.CASCADE)


class Respond(Timestamped):
    body = models.CharField(max_length=8192)
    rating = models.PositiveSmallIntegerField(
        validators=[custom_validators.rating_validator, ]
    )

    author = models.ForeignKey(
        User,
        related_name="responds",
        on_delete=models.PROTECT)

    performer = models.ForeignKey(
        User,
        related_name="responds",
        on_delete=models.CASCADE)

    job = models.ForeignKey()

    
    class Meta:
        unique_together = ('author', 'performer')