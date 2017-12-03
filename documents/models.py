from django.db import models
from django.utils import timezone

class PDF(models.Model):
    """Holds PDF attachments for various other apps"""
    location = models.FileField(
        upload_to="attachments",
    )
    date_uploads = models.DateTimeField(
        default=timezone.now,
    )