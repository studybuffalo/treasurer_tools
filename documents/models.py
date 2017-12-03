from django.db import models
from django.utils import timezone

class PDF(models.Model):
    """Holds PDF attachments for various other apps"""
    location = models.FileField(
        upload_to="attachments",
    )
    date_uploaded = models.DateTimeField(
        default=timezone.now,
    )

class OriginalFile(models.Model):
    """Holds all the un-merged files"""
    location = models.FileField(
        upload_to="user_uploads",
    )
    date_uploaded = models.DateTimeField(
        default=timezone.now,
    )