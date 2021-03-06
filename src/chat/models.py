from django.db import models
from behaviors.behaviors import Timestamped
from django.conf import settings

from django.db.models.manager import Manager
from django.core.exceptions import ObjectDoesNotExist


class BaseRoomManager(Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class Room(Timestamped):
    name = models.CharField(max_length=256, verbose_name="Room name")

    objects = BaseRoomManager()


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
