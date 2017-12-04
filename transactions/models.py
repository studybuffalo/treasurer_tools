from django.db import models
from documents.models import Attachment

from simple_history.models import HistoricalRecords


class Transaction(models.Model):
    """Holds data on the overall transaction"""

class Item(models.Model):
    """Holds data on an individual transaction item"""

class FinancialCodeSystem(models.Model):
    """Name and description of a financial code system"""

class FinancialCode(models.Model):
    """Holds data on an individual financial code"""

class AttachmentMatch(models.Model):
    """Links a transaction to one or more attachments"""
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
    )
    final_attachment = models.OneToOneField(
        Attachment,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()