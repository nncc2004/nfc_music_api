import uuid

from django.conf import settings
from django.db import models


class Song(models.Model):
    uuid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )

    title = models.CharField(
        max_length=200,
    )

    artist = models.CharField(
        max_length=200,
        blank=True,
    )

    firebase_url = models.URLField(
        blank=True,
        null=True,
    )

    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="uploaded_songs",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )