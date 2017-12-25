"""Models for the documents app"""

from django.db import models
from django.utils import timezone

class Attachment(models.Model):
    """Holds an attachment"""
    location = models.FileField(
        upload_to="attachments",
    )
    date_uploaded = models.DateTimeField(
        default=timezone.now,
    )
