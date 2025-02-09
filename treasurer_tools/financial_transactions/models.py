"""Models for the transaction app"""

from decimal import Decimal

from django.db import models
from django.utils import timezone

from simple_history.models import HistoricalRecords

from bank_reconciliation.models import ReconciliationGroup
from financial_codes.models import FinancialCodeSystem, FinancialCode
from payee_payers.models import PayeePayer


class FinancialTransaction(models.Model):
    # TODO: Add proper tracking of submission details
    """Holds data on the overall transaction"""
    payee_payer = models.ForeignKey(
        PayeePayer,
        help_text=(
            'The individual, organization, or company this transaction '
            'applies to'
        ),
        on_delete=models.PROTECT,
        verbose_name='payee or payer'
    )
    transaction_type = models.CharField(
        choices=(
            ('e', 'expense'),
            ('r', 'revenue'),
        ),
        default='e',
        help_text='The type of transaction',
        max_length=1,
    )
    memo = models.CharField(
        help_text='Overall summary of the transaction',
        max_length=1000,
    )
    submitter = models.CharField(
        blank=True,
        help_text='Individual who submitted or initiated this transaction',
        max_length=256,
        null=True
    )
    date_submitted = models.DateField(
        default=timezone.now,
        verbose_name='submission date'
    )
    submission_notes = models.CharField(
        blank=True,
        help_text='Additional notes and details about this submission.',
        max_length=1000,
        null=True,
    )
    reconciled = models.ForeignKey(
        ReconciliationGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='financialtransactions',
    )
    history = HistoricalRecords()

    def __str__(self):
        if self.transaction_type == 'e':
            return_string = '{} - Expense - {} - {}'.format(
                self.date_submitted, self.payee_payer, self.memo[:100]
            )
        elif self.transaction_type == 'r':
            return_string = '{} - Revenue - {} - {}'.format(
                self.date_submitted, self.payee_payer, self.memo[:100]
            )

        return return_string

    @property
    def total(self):
        """Calculates the total of all children items"""
        items = self.items.all()

        total = Decimal(0)

        for item in items:
            total = Decimal(total) + Decimal(item.amount) + Decimal(item.gst)

        return total

    @property
    def total_before_tax(self):
        """Calculates the pre-tax total of all children items."""
        items = self.items.all()

        total = Decimal(0)

        for item in items:
            total = Decimal(total) + Decimal(item.amount)

        return total

    @property
    def total_tax(self):
        """Calculates the tax total of all children items."""
        items = self.items.all()

        total = Decimal(0)

        for item in items:
            total = Decimal(total) + Decimal(item.gst)

        return total

class Item(models.Model):
    """Holds data on an individual transaction item"""
    transaction = models.ForeignKey(
        FinancialTransaction,
        on_delete=models.CASCADE,
        related_name='items',
    )
    date_item = models.DateField(
        default=timezone.now,
        help_text='The date the item was purchased, cheque written, etc.',
        verbose_name='date'
    )
    description = models.CharField(
        help_text='A description of the item',
        max_length=500,
    )
    amount = models.DecimalField(
        decimal_places=2,
        default=0,
        help_text='The pre-tax dollar value',
        max_digits=12,
    )
    gst = models.DecimalField(
        decimal_places=2,
        default=0,
        help_text='The tax (GST/HST) dollar value',
        max_digits=12,
        verbose_name='GST/HST',
    )
    financial_codes = models.ManyToManyField(
        FinancialCode,
        through='FinancialCodeMatch',
    )
    history = HistoricalRecords()

    def __str__(self):
        return '{} - {} - ${}'.format(
            self.date_item, self.description, self.total
        )

    @property
    def total(self):
        """Calculates an item's total"""
        total = self.amount + self.gst

        # Return total as a proper dollar currency
        return Decimal(total)

    @property
    def get_submission_code(self):
        """Returns the proper submission code for this item."""
        system = FinancialCodeSystem.objects.filter(submission_code=True).order_by('title').first()
        return self.financial_codes.filter(financial_code_group__budget_year__financial_code_system=system).first()

class FinancialCodeMatch(models.Model):
    """Links a transaction to a financial code"""
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
    )
    financial_code = models.ForeignKey(
        FinancialCode,
        on_delete=models.CASCADE,
    )
    history = HistoricalRecords()

    def __str__(self):
        return '{} - {}'.format(str(self.item), str(self.financial_code))
