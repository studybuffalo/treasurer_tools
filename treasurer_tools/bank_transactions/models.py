"""Models for bank_transaction app"""

from decimal import Decimal

from django.db import models
from django.db.models import Sum

from simple_history.models import HistoricalRecords

from bank_institutions.models import Account


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
    history = HistoricalRecords()

    def __str__(self):
        return "{} to {} statement".format(self.date_start, self.date_end)

    @property
    def total_debit(self):
        """Calculates a statements debit total"""
        debit_total = self.banktransaction_set.all().aggregate(total=Sum("amount_debit"))

        return Decimal(debit_total["total"])

    @property
    def total_credit(self):
        """Calculates a statements credit total"""
        credit_total = self.banktransaction_set.all().aggregate(total=Sum("amount_credit"))

        return Decimal(credit_total["total"])

    @property
    def total(self):
        """Calculates a statements total"""
        total = self.banktransaction_set.all().aggregate(
            debit_total=Sum("amount_debit"),
            credit_total=Sum("amount_credit")
        )

        return Decimal(total["credit_total"] - total["debit_total"])

class BankTransaction(models.Model):
    """Details on a single bank transactions"""
    statement = models.ForeignKey(
        Statement,
        on_delete=models.CASCADE,
        help_text="The statement this this transaction applies to",
        verbose_name="bank statement",
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
        verbose_name="custom description",
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
    history = HistoricalRecords()

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
