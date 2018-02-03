"""Test cases for the bank_reconciliation app views"""

from django.test import TestCase

from ..helpers import BankReconciliation
from utils.utils_tests import create_bank_transactions, create_financial_transactions_and_items

class ReconciliationDashboardTest(TestCase):
    """Tests for the BankReconciliation object"""
    # pylint: disable=no-member,protected-access
    
    def setUp(self):
        bank_transactions = create_bank_transactions()
        financial_transactions = create_financial_transactions_and_items()
        self.valid_json_data = {
            "financial_ids": [
                financial_transactions[0].id,
            ],
            "bank_ids": [
                bank_transactions[0].id
            ]
        }

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
