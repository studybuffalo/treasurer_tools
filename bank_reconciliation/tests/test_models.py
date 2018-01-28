"""Test cases for the bank_reconcilation app models"""

from django.test import TestCase

from ..models import ReconciliationMatch

class ReconciliationMatchModelTest(TestCase):
    """Tests for the ReconciliationMatch model"""
    fixtures = [
        "bank_transactions/tests/fixtures/account.json",
        "bank_transactions/tests/fixtures/bank_transaction.json",
        "bank_transactions/tests/fixtures/country.json",
        "bank_transactions/tests/fixtures/demographics.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/item.json",
        "bank_transactions/tests/fixtures/reconciliation_match.json",
        "bank_transactions/tests/fixtures/statement.json",
        "bank_transactions/tests/fixtures/transaction.json",
    ]
    
    def test_string_representation(self):
        """Tests ReconciliationMatch string representation"""
        # pylint: disable=no-member
        reconciliation_match = ReconciliationMatch.objects.get(id=1)

        self.assertEqual(
            str(reconciliation_match),
            "2017-01-01 - Cheque #0001 - 2017-06-01 - Expense - Joshua Torrance - Travel Grant award 2017"
        )
