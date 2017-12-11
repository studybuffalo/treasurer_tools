from django.db import models
from django.utils import timezone

from payee_payer.models import Demographics
from financial_codes.models import FinancialCode
from documents.models import Attachment

from simple_history.models import HistoricalRecords


class Transaction(models.Model):
    """Holds data on the overall transaction"""
    payee_payer = models.ForeignKey(
        Demographics,
        help_text=(
            "The individual, organization, or company this transaction "
            "applies to"
        ),
        on_delete=models.PROTECT,
    )
    transaction_type = models.CharField(
        choices=(
            ("p", "Payable"),
            ("r", "Receivable"),
        ),
        help_text="The type of transaction",
        max_length=1,
    )
    memo = models.CharField(
        help_text="Details of the transaction",
        max_length=1000,
    )
    date_submitted = models.DateField(
        default=timezone.now,
    )
    history = HistoricalRecords

    def __str__(self):
        if self.transaction_type == "p":
            return "Accounts Payable - {} - {}".format(
                self.payee_payer, self.memo[:100]
            )
        else:
            return "Accounts Receivable - {} - {}".format(
                self.payee_payer, self.memo[:100]
            )

class Item(models.Model):
    """Holds data on an individual transaction item"""
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
    )
    date_item = models.DateField(
        help_text="The date the item was purchased, cheque written, etc.",
    )
    description = models.CharField(
        help_text="A description of the item",
        max_length=500,
    )
    amount = models.DecimalField(
        decimal_places=2,
        help_text="The pre-tax dollar value",
        max_digits=12,
    )
    gst = models.DecimalField(
        decimal_places=2,
        help_text="The tax (GST/HST) dollar value",
        max_digits=12,
    )
    history = HistoricalRecords

class FinancialCodeMatch(models.Model):
    """Links a transaction to a financial code"""
    item = models.OneToOneField(
        Item,
        on_delete=models.CASCADE,
    )
    financial_code = models.OneToOneField(
        FinancialCode,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()

class AttachmentMatch(models.Model):
    """Links a transaction to one or more attachments"""
    transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
    )
    attachment = models.OneToOneField(
        Attachment,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return "{} - {}".format(self.transaction, self.attachment)