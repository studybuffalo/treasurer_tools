"""Models for the documents app"""
import os

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

    def __str__(self):
        file_name = os.path.basename(self.location.name)

        if len(file_name) > 70:
            return_string = "{}...".format(file_name[:67])
        else:
            return_string = file_name

        return file_name