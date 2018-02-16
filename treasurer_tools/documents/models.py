"""Models for the documents app"""
import os

from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from bank_transactions.models import Statement


class Attachment(models.Model):
    """Holds an attachment"""
    location = models.FileField(
        upload_to="attachments",
        max_length=255,
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

        return return_string

class BankStatementMatch(models.Model):
    """Links bank statement to one or more attachments"""
    statement = models.ForeignKey(
        Statement,
        on_delete=models.CASCADE,
    )
    attachment = models.ForeignKey(
        Attachment,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return "{} - {}".format(self.statement, self.attachment)
