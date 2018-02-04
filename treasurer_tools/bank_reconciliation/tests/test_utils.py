"""Test cases for the bank_reconciliation app views"""

from django.test import TestCase

from ..models import ReconciliationMatch
from ..utils import BankReconciliation

from .utils import create_bank_transactions, create_financial_transactions

class BankReconciliationObjectTest(TestCase):
    """Tests for the BankReconciliation object"""
    # pylint: disable=no-member,protected-access
    
    def setUp(self):
        self.bank_transactions = create_bank_transactions()
        self.financial_transactions = create_financial_transactions()
        self.valid_data = {
            "bank_ids": [self.bank_transactions[0].id],
            "financial_ids": [self.financial_transactions[0].id],
        }

    def test_is_valid_with_valid_data(self):
        """Control test to ensure is_valid works as intended"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")

        # Test that is_valid works as expected
        reconciliation.json_data = self.valid_data
        self.assertTrue(reconciliation.is_valid())

    def test_match_success_response_on_valid_data(self):
        """Checks for proper responses on successful match"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")
        reconciliation.json_data = self.valid_data
        
        # Match the transactions
        reconciliation.create_matches()

        # Check for proper number of responses
        self.assertEqual(len(reconciliation.success["bank_id"]), 1)
        self.assertEqual(len(reconciliation.success["financial_id"]), 1)

        # Check for proper response
        self.assertEqual(
            reconciliation.success["bank_id"][0],
            self.valid_data["bank_ids"][0]
        )
        self.assertEqual(
            reconciliation.success["financial_id"][0],
            self.valid_data["financial_ids"][0]
        )

    def test_match_success_database_changes(self):
        """Checks for correct changes to database on successful match"""
        # Count number of matches there are currently
        total_matches = ReconciliationMatch.objects.count()
        
        # Setup the reconciliation object and match the IDs
        reconciliation = BankReconciliation("", "match")
        reconciliation.json_data = self.valid_data
        reconciliation.create_matches()

        # Check for proper number of matches
        self.assertEqual(
            ReconciliationMatch.objects.count(),
            total_matches + 1,
        )

        # Check that proper IDs were matched
        last_match = ReconciliationMatch.objects.last()
        self.assertEqual(
            last_match.bank_transaction.id,
            self.valid_data["bank_ids"][0]
        )
        self.assertEqual(
            last_match.financial_transaction.id,
            self.valid_data["financial_ids"][0]
        )

    def test_unmatch_success_response_on_valid_data(self):
        """Checks for proper responses on successful unmatch"""
        # Create a test match
        ReconciliationMatch.objects.create(
            bank_transaction=self.bank_transactions[0],
            financial_transaction=self.financial_transactions[0],
        )

        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "unmatch")
        reconciliation.json_data = self.valid_data
        
        # Match the transactions
        reconciliation.delete_matches()

        # Check for proper number of responses
        self.assertEqual(len(reconciliation.success["bank_id"]), 1)
        self.assertEqual(len(reconciliation.success["financial_id"]), 1)

        # Check for proper response
        self.assertEqual(
            reconciliation.success["bank_id"][0],
            self.valid_data["bank_ids"][0]
        )
        self.assertEqual(
            reconciliation.success["financial_id"][0],
            self.valid_data["financial_ids"][0]
        )

    def test_unmatch_success_database_changes(self):
        """Checks for correct changes to database on successful match"""
        # Create a test match
        ReconciliationMatch.objects.create(
            bank_transaction=self.bank_transactions[0],
            financial_transaction=self.financial_transactions[0],
        )

        # Count number of matches there are currently
        total_matches = ReconciliationMatch.objects.count()        

        # Setup the reconciliation object and match the IDs
        reconciliation = BankReconciliation("", "unmatch")
        reconciliation.json_data = self.valid_data
        reconciliation.delete_matches()

        # Check for proper number of matches
        self.assertEqual(
            ReconciliationMatch.objects.count(),
            total_matches - 1,
        )

        # Check that proper IDs were unmatched
        last_match = ReconciliationMatch.objects.last()
        self.assertEqual(
            ReconciliationMatch.objects.filter(bank_transaction=self.bank_transactions[0]).count(),
            0
        )
        self.assertEqual(
            ReconciliationMatch.objects.filter(financial_transaction=self.financial_transactions[0]).count(),
            0
        )

    def test_error_on_invalid_raw_data(self):
        """Checks error response for invalid raw data"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("a", "match")

        # Check for proper error message
        self.assertEqual(
            reconciliation.errors["post_data"][0],
            "Invalid data submitted to server."
        )
        
    def test_error_on_missing_bank_id_key(self):
        """Checks error handling on json_data missing bank_id key"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")

        # Setup up invalid data (remove bank_ids key)
        invalid_data = self.valid_data
        invalid_data.pop("bank_ids", None)

        reconciliation.json_data = invalid_data

        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["bank_id"][0],
            "Please select at least one bank transaction."
        )
        
    def test_error_on_missing_bank_ids(self):
        """Checks for proper handling of a missing bank_ids"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")

        # Setup up invalid data (no bank IDs)
        invalid_data = self.valid_data
        invalid_data["bank_ids"] = []

        reconciliation.json_data = invalid_data

        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["bank_id"][0],
            "Please select at least one bank transaction."
        )

    def test_error_on_invalid_bank_id_format(self):
        """Checks error responses for a string bank ID"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")
        
        # Setup up invalid data (change financial_id to string)
        invalid_data = self.valid_data
        invalid_data["bank_ids"] = "a"

        reconciliation.json_data = invalid_data
        
        # Check for proper error responses
        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["bank_id"][0],
            "a is not a valid bank transaction ID. Please make a valid selection."
        )

    def test_error_on_nonexistent_bank_id(self):
        """Checks error responses for a non-existent bank ID"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")
        
        # Setup up invalid data (change financial_id to string)
        invalid_data = self.valid_data
        invalid_data["bank_ids"] = [999999999]

        reconciliation.json_data = invalid_data
        
        # Check for proper error responses
        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["bank_id"][0],
            "999999999 is not a valid bank transaction ID. Please make a valid selection."
        )

    def test_error_on_already_matched_bank_id(self):
        """Checks error responses for matching already matched financial"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")
        
        # Reconcile the test bank ID
        ReconciliationMatch.objects.create(
            bank_transaction=self.bank_transactions[0],
            financial_transaction=self.financial_transactions[1],
        )

        # Pass the now invalid data to the object
        reconciliation.json_data = self.valid_data
        
        # Check for proper error responses
        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["bank_id"][0],
            (
                "2017-01-01 - Cheque #0001 is already reconciled. Unmatch "
                "the transaction before reassigning it."
            )
        )

    def test_error_on_unmatched_bank_id(self):
        """Checks error response for unmatching an unmatched bank ID"""
        # Create a test match
        ReconciliationMatch.objects.create(
            bank_transaction=self.bank_transactions[1],
            financial_transaction=self.financial_transactions[0],
        )

        # Setup reconciliation object
        reconciliation = BankReconciliation("", "unmatch")
        reconciliation.json_data = self.valid_data
        
        # Check for proper error handling
        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["bank_id"][0],
            "2017-01-01 - Cheque #0001 is not a matched transaction."
        )

    def test_error_on_missing_financial_id_key(self):
        """Checks error handling on json_data missing financial_id key"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")

        # Setup up invalid data (remove financial_ids key)
        invalid_data = self.valid_data
        invalid_data.pop("financial_ids", None)

        reconciliation.json_data = invalid_data

        # Check for proper error responses
        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["financial_id"][0],
            "Please select at least one financial transaction."
        )

    def test_error_on_missing_financial_ids(self):
        """Checks for proper handling of a missing financial_ids"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")

        # Setup up invalid data
        invalid_data = self.valid_data
        invalid_data["financial_ids"] = []
        
        reconciliation.json_data = invalid_data

        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["financial_id"][0],
            "Please select at least one financial transaction."
        )
        
    def test_error_on_invalid_financial_id_format(self):
        """Checks error responses for a string financial ID"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")
        
        # Setup up invalid data (change financial_id to string)
        invalid_data = self.valid_data
        invalid_data["financial_ids"] = "a"

        reconciliation.json_data = invalid_data
        
        # Check for proper error responses
        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["financial_id"][0],
            "a is not a valid financial transaction ID. Please make a valid selection."
        )

    def test_error_on_nonexistent_financial_id(self):
        """Checks error responses for a non-existent financial ID"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")
        
        # Setup up invalid data (change financial_id to string)
        invalid_data = self.valid_data
        invalid_data["financial_ids"] = [999999999]

        reconciliation.json_data = invalid_data
        
        # Check for proper error responses
        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["financial_id"][0],
            "999999999 is not a valid financial transaction ID. Please make a valid selection."
        )

    def test_error_on_already_matched_financial_id(self):
        """Checks error responses for already matched financial"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("", "match")
        
        # Reconcile the test financial ID
        ReconciliationMatch.objects.create(
            bank_transaction=self.bank_transactions[1],
            financial_transaction=self.financial_transactions[0],
        )

        # Pass the now invalid data to the object
        reconciliation.json_data = self.valid_data
        
        # Check for proper error responses
        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["financial_id"][0],
            (
                "2017-06-01 - Expense - Test User - Test Expense Transaction 1 is already "
                "reconciled. Unmatch the transaction before reassigning it."
            )
        )

    
    def test_error_on_unmatched_financial_id(self):
        """Checks error response for unmatching an unmatched financial ID"""
        # Create a test match
        ReconciliationMatch.objects.create(
            bank_transaction=self.bank_transactions[0],
            financial_transaction=self.financial_transactions[1],
        )

        # Setup reconciliation object
        reconciliation = BankReconciliation("", "unmatch")
        reconciliation.json_data = self.valid_data
        
        # Check for proper error handling
        self.assertFalse(reconciliation.is_valid())
        self.assertEqual(
            reconciliation.errors["financial_id"][0],
            (
                "2017-06-01 - Expense - Test User - Test Expense Transaction "
                "1 is not a matched transaction."
            )
        )
