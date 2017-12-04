from django.db import models
from django.utils import timezone

class FinalAttachment(models.Model):
    """Holds the final assembled PDF attachments for other apps"""
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