"""Models for the bank_reconcilation app"""
from django.db import models

from simple_history.models import HistoricalRecords


class ReconciliationGroup(models.Model):
    history = HistoricalRecords()

class ReconciliationMatch(models.Model):
    """Links bank transaction to one or more financial transactions"""
    group = models.ForeignKey(
        ReconciliationGroup,
        on_delete=models.CASCADE,
    )
    bank_transaction = models.ForeignKey(
        'bank_transactions.BankTransaction',
        on_delete=models.CASCADE,
        related_name="rm_bank_transaction",
    )
    financial_transaction = models.ForeignKey(
        'financial_transactions.FinancialTransaction',
        on_delete=models.CASCADE,
        related_name="rm_financial_transaction",
    )
    history = HistoricalRecords()

    def __str__(self):
        return "{} - {}".format(
            self.bank_transaction, self.financial_transaction
        )
