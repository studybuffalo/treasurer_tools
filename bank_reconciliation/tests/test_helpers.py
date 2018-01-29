"""Test cases for the bank_reconciliation app views"""

from django.test import TestCase

from ..helpers import BankReconciliation

class ReconciliationDashboardTest(TestCase):
    """Tests for the BankReconciliation object"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_reconciliation/tests/fixtures/transaction.json",
        "bank_reconciliation/tests/fixtures/item.json",
        "bank_reconciliation/tests/fixtures/account.json",
        "bank_reconciliation/tests/fixtures/bank_transaction.json",
        "bank_reconciliation/tests/fixtures/country.json",
        "bank_reconciliation/tests/fixtures/demographics.json",
        "bank_reconciliation/tests/fixtures/institution.json",
        "bank_reconciliation/tests/fixtures/reconciliation_match.json",
        "bank_reconciliation/tests/fixtures/statement.json",
    ]

    def setUp(self):
        self.valid_json_data = {"financial_ids": [2], "bank_ids": [2]}

    def test_invalid_financial_ids_key(self):
        """Checks for proper handling of a missing financial_ids key"""
        reconciliation = BankReconciliation("", "match")

        # Control test
        reconciliation.json_data = self.valid_json_data
        self.assertTrue(reconciliation.is_valid())

        # Invalid data test
        reconciliation.json_data = {"bank_ids": [2]}

        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["financial_id"][0],
            "Please select at least one financial transaction."
        )
        
    def test_invalid_bank_ids_key(self):
        """Checks for proper handling of a missing bank_ids key"""
        reconciliation = BankReconciliation("", "match")

        # Control test
        reconciliation.json_data = self.valid_json_data
        self.assertTrue(reconciliation.is_valid())

        # Invalid data test
        reconciliation.json_data = {"financial_ids": [2]}

        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["bank_id"][0],
            "Please select at least one bank transaction."
        )
