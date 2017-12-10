from django.db import models

from documents.models import Attachment
from transactions.models import Transaction

from simple_history.models import HistoricalRecords


class Institution(models.Model):
    """Details on the bank/financial institution"""
    name = models.CharField(
        help_text="Name of the bank/financial institution",
        max_length=200,
    )
    address = models.CharField(
        max_length=500,
    )
    phone = models.CharField(
        max_length=30,
    )
    fax = models.CharField(
        max_length=30,
    )
    history = HistoricalRecords()

class Account(models.Model):
    """A single account associated with an institution"""
    institution = models.ForeignKey(
        Institution,
        help_text="The bank this account is associated with",
        on_delete=models.PROTECT,
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
        help_text="The account status",
        max_length=1,
    )
    history = HistoricalRecords()

class Statement(models.Model):
    """Details on a single bank account statement"""
    account = models.ForeignKey(
        Account,
        help_text="The account this statement belong to",
        on_delete=models.PROTECT,
    )
    date_start = models.DateField(
        help_text="The first date the statement applies to",
    )
    date_end = models.DateField(
        help_text="The last date the statement applies to",
    )
    history = HistoricalRecords()

class BankTransaction(models.Model):
    """Details on a single bank transactions"""
    date_transaction = models.DateField(
        help_text="The date of the transaction",
    )
    description_bank = models.CharField(
        help_text="Description of the transaction as per the bank statement",
        max_length=100,
    )
    description_user = models.CharField(
        help_text="A user-specified description of the transaction",
        max_length=100,
    )
    amount_debit = models.DecimalField(
        decimal_places=2,
        help_text="The debit (withdrawal) amount of the transaction",
        max_digits=12,
    )
    amount_credit = models.DecimalField(
        decimal_places=2,
        help_text="The credit (deposit) amount of the transaction",
        max_digits=12,
    )
    history = HistoricalRecords()
    
class AttachmentMatch(models.Model):
    """Links a transaction to one or more attachments"""
    transaction = models.OneToOneField(
        BankTransaction,
        on_delete=models.CASCADE,
    )
    attachment = models.OneToOneField(
        Attachment,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return "{} - {}".format(self.transaction, self.attachment)

class ReconciliationMatch(models.Model):
    """Links bank transaction to one or more financial transactions"""
    bank_transaction = models.OneToOneField(
        BankTransaction,
        on_delete=models.CASCADE,
    )
    financial_transaction = models.OneToOneField(
        Transaction,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return "{} - {}".format(
            self.bank_transaction, self.financial_attachment
        )