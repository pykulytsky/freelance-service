from django.db import models
from behaviors.behaviors import Timestamped
from django.conf import settings


class Room(Timestamped):
    name = models.CharField(max_length=256, verbose_name="Room name")


class Message(Timestamped):
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="sended_messages",
        on_delete=models.PROTECT)

    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="received_messages",
        on_delete=models.PROTECT)

    body = models.CharField(
        max_length=4096,
        verbose_name="Message body")

    class Meta:
        unique_together = ('sender', 'receiver')
