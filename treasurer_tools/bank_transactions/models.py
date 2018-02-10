"""Models for bank_transaction app"""
from django.db import models

from simple_history.models import HistoricalRecords

from documents.models import Attachment


class Institution(models.Model):
    """Details on the bank/financial institution"""
    name = models.CharField(
        help_text="Name of the bank/financial institution",
        max_length=250,
    )
    address = models.CharField(
        max_length=1000,
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="phone number",
    )
    fax = models.CharField(
        max_length=30,
        verbose_name="fax number",
    )
    # history = HistoricalRecords()

    def __str__(self):
        return self.name


class Account(models.Model):
    """A single account associated with an institution"""
    institution = models.ForeignKey(
        Institution,
        help_text="The bank this account is associated with",
        on_delete=models.CASCADE,
    )
    account_number = models.CharField(
        help_text="The account number/reference for this account",
        max_length=100,
    )
    name = models.CharField(
        help_text="The name of the account",
        max_length=100,
    )
    status = models.CharField(
        choices=(
            ("a", "Active"),
            ("i", "Inactive"),
        ),
        default="a",
        help_text="The account status",
        max_length=1,
    )
    # history = HistoricalRecords()

    def __str__(self):
        return "{} {} ({})".format(
            self.institution, self.name, self.account_number
        )

class Statement(models.Model):
    """Details on a single bank account statement"""
    account = models.ForeignKey(
        Account,
        help_text="The account this statement belong to",
        on_delete=models.PROTECT,
    )
    date_start = models.DateField(
        help_text="The first date the statement applies to",
        verbose_name="start date",
    )
    date_end = models.DateField(
        help_text="The last date the statement applies to",
        verbose_name="end date",
    )
    # history = HistoricalRecords()

    def __str__(self):
        return "{} to {} statement".format(self.date_start, self.date_end)

class BankTransaction(models.Model):
    """Details on a single bank transactions"""
    statement = models.ForeignKey(
        Statement,
        on_delete=models.CASCADE,
        help_text="The statement this this transaction applies to",
    )
    date_transaction = models.DateField(
        help_text="The date of the transaction",
        verbose_name="transaction date",
    )
    description_bank = models.CharField(
        help_text="Description of the transaction as per the bank statement",
        max_length=100,
        verbose_name="bank description",
    )
    description_user = models.CharField(
        blank=True,
        help_text="A user-specified description of the transaction",
        max_length=100,
        null=True,
        verbose_name="user description",
    )
    amount_debit = models.DecimalField(
        decimal_places=2,
        default=0,
        help_text="The debit (withdrawal) amount of the transaction",
        max_digits=12,
        verbose_name="debit amount",
    )
    amount_credit = models.DecimalField(
        decimal_places=2,
        default=0,
        help_text="The credit (deposit) amount of the transaction",
        max_digits=12,
        verbose_name="credit amount",
    )
    # history = HistoricalRecords()

    def __str__(self):
        if self.description_user:
            return_str = "{} - {}".format(
                self.date_transaction, self.description_user
            )
        else:
            return_str = "{} - {}".format(
                self.date_transaction, self.description_bank
            )

        return return_str

class AttachmentMatch(models.Model):
    """Links bank statement to one or more attachments"""
    statement = models.ForeignKey(
        Statement,
        on_delete=models.CASCADE,
        related_name="am_bank_transaction",
    )
    attachment = models.ForeignKey(
        Attachment,
        on_delete=models.CASCADE,
        related_name="am_attachment",
    )
    # history = HistoricalRecords()

    def __str__(self):
        return "{} - {}".format(self.statement, self.attachment)
