"""Models for the bank_reconcilation app"""
from django.db import models

from simple_history.models import HistoricalRecords

from bank_transactions.models import BankTransaction
from financial_transactions.models import FinancialTransaction

class ReconciliationMatch(models.Model):
    """Links bank transaction to one or more financial transactions"""
    bank_transaction = models.ForeignKey(
        BankTransaction,
        on_delete=models.CASCADE,
        related_name="rm_bank_transaction",
    )
    financial_transaction = models.ForeignKey(
        FinancialTransaction,
        on_delete=models.CASCADE,
        related_name="rm_financial_transaction",
    )
    # history = HistoricalRecords()

    def __str__(self):
        return "{} - {}".format(
            self.bank_transaction, self.financial_transaction
        )
