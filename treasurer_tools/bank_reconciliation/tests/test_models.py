"""Test cases for the bank_reconcilation app models"""

from django.test import TestCase

from bank_reconciliation.models import ReconciliationMatch

from .utils import create_bank_transactions, create_financial_transactions

class ReconciliationMatchModelTest(TestCase):
    """Tests for the ReconciliationMatch model"""

    def setUp(self):
        self.bank_transactions = create_bank_transactions()
        self.financial_transactions = create_financial_transactions()

    def test_string_representation(self):
        """Tests ReconciliationMatch string representation"""

        reconciliation_match = ReconciliationMatch.objects.create(
            bank_transaction=self.bank_transactions[0],
            financial_transaction=self.financial_transactions[0]
        )

        self.assertEqual(
            str(reconciliation_match),
            "2017-01-01 - Cheque #0001 - 2017-06-01 - Expense - Test User - Test Expense Transaction 1"
        )
