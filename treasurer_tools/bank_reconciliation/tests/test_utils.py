"""Test cases for the bank_reconciliation app views"""
from django.test import RequestFactory, TestCase

from bank_reconciliation.models import ReconciliationGroup
from bank_reconciliation.utils import return_transactions_as_json, BankReconciliation
from financial_transactions.models import FinancialTransaction

from .utils import create_bank_transactions, create_financial_transactions


class ReturnTransactionsAsJSONTest(TestCase):
    """Tests the return_transaction_as_json function"""
    # pylint: disable=unsubscriptable-object
    def setUp(self):
        # Populate database with entries
        create_bank_transactions()
        create_financial_transactions()

        # Create a request factory for testing function
        self.request = RequestFactory()

        # Proper parameters for testing
        self.correct_url = "banking/reconciliation/retrieve-transactions/"
        self.correct_bank_parameters = {
            "transaction_type": "bank",
            "date_start": "2000-01-01",
            "date_end": "2018-12-31",
        }
        self.correct_financial_parameters = {
            "transaction_type": "financial",
            "date_start": "2000-01-01",
            "date_end": "2018-12-31",
        }

    def test_proper_json_response_on_valid_bank_data(self):
        """Checks for a proper json response with valid financial data"""
        # Get current count of the financial transactions
        total_bank_transactions = FinancialTransaction.objects.count()

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=self.correct_bank_parameters
        )

        response = return_transactions_as_json(valid_request)

        # Checks that data was returned
        self.assertTrue(response)

        # Check that values were returned
        self.assertEqual(len(response["data"]), total_bank_transactions)
        self.assertEqual(response["type"], "bank")

    def test_proper_json_response_on_valid_financial_data(self):
        """Checks for a proper json response with valid financial data"""
        # Get current count of the financial transactions
        total_financial_transactions = FinancialTransaction.objects.count()

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=self.correct_financial_parameters
        )

        response = return_transactions_as_json(valid_request)

        # Checks that data was returned
        self.assertTrue(response)

        # Check that values were returned
        self.assertEqual(len(response["data"]), total_financial_transactions)
        self.assertEqual(response["type"], "financial")

    def test_error_on_missing_transaction_type(self):
        """Checks error response when transaction_type is missing"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_bank_parameters
        incorrect_parameters["transaction_type"] = ""

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=incorrect_parameters
        )

        # Generate the response
        response = return_transactions_as_json(valid_request)

        # Check for proper error message
        self.assertEqual(
            response["errors"]["transaction_type"],
            "Invalid transaction type provided."
        )

    def test_error_response_on_invalid_transaction_type(self):
        """Confirms error response returned on invalid transaction_type"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_bank_parameters
        incorrect_parameters["transaction_type"] = "a"

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=incorrect_parameters
        )

        # Generate the response
        response = return_transactions_as_json(valid_request)

        # Check for proper error message
        self.assertEqual(
            response["errors"]["transaction_type"],
            "Invalid transaction type provided."
        )

    def test_error_on_missing_bank_date_start(self):
        """Tests error response on missing bank start date"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_bank_parameters
        incorrect_parameters["date_start"] = ""

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=incorrect_parameters
        )

        # Generate the response
        response = return_transactions_as_json(valid_request)

        # Check for proper error message
        self.assertEqual(
            response["errors"]["date_start"],
            "Must specify start date."
        )

    def test_error_on_missing_bank_date_end(self):
        """Tests error response on missing bank end date"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_bank_parameters
        incorrect_parameters["date_end"] = ""

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=incorrect_parameters
        )

        # Generate the response
        response = return_transactions_as_json(valid_request)

        # Check for proper error message
        self.assertEqual(
            response["errors"]["date_end"],
            "Must specify end date."
        )

    def test_error_on_invalid_bank_start_date(self):
        """Tests error response on improperly formatted bank start date"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_bank_parameters
        incorrect_parameters["date_start"] = "01-01-2017"

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=incorrect_parameters
        )

        # Generate the response
        response = return_transactions_as_json(valid_request)

        # Check for proper error message
        self.assertEqual(
            response["errors"]["date_start"],
            "Provided date(s) not in valid format ('yyyy-mm-dd')."
        )

    def test_error_on_invalid_bank_end_date(self):
        """Tests error response on improperly formatted bank end date"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_bank_parameters
        incorrect_parameters["date_end"] = "31-12-2017"

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=incorrect_parameters
        )

        # Generate the response
        response = return_transactions_as_json(valid_request)

        # Check for proper error message
        self.assertEqual(
            response["errors"]["date_end"],
            "Provided date(s) not in valid format ('yyyy-mm-dd')."
        )

    def test_error_on_missing_financial_date_start(self):
        """Tests error response on missing financial start date"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_start"] = ""

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=incorrect_parameters
        )

        # Generate the response
        response = return_transactions_as_json(valid_request)

        # Check for proper error message
        self.assertEqual(
            response["errors"]["date_start"],
            "Must specify start date."
        )

    def test_error_on_missing_financial_date_end(self):
        """Tests error response on missing financial end date"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_end"] = ""

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=incorrect_parameters
        )

        # Generate the response
        response = return_transactions_as_json(valid_request)

        # Check for proper error message
        self.assertEqual(
            response["errors"]["date_end"],
            "Must specify end date."
        )

    def test_error_on_invalid_financial_start_date(self):
        """Tests error response on improperly formatted financial start date"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_start"] = "01-01-2017"

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=incorrect_parameters
        )

        # Generate the response
        response = return_transactions_as_json(valid_request)

        # Check for proper error message
        self.assertEqual(
            response["errors"]["date_start"],
            "Provided date(s) not in valid format ('yyyy-mm-dd')."
        )

    def test_error_on_invalid_financial_end_date(self):
        """Tests error response on improperly formatted financial end date"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_end"] = "31-12-2017"

        # Create a test request object
        valid_request = self.request.get(
            self.correct_url,
            data=incorrect_parameters
        )

        # Generate the response
        response = return_transactions_as_json(valid_request)

        # Check for proper error message
        self.assertEqual(
            response["errors"]["date_end"],
            "Provided date(s) not in valid format ('yyyy-mm-dd')."
        )

class BankReconciliationObjectTest(TestCase):
    """Tests for the BankReconciliation object"""

    def setUp(self):
        self.bank_transactions = create_bank_transactions()
        self.financial_transactions = create_financial_transactions()
        self.valid_data = {
            "bank_ids": [self.bank_transactions[0].id],
            "investment_ids": [],
            "financial_ids": [self.financial_transactions[0].id],
        }

    def test_is_valid_with_valid_data(self):
        """Control test to ensure is_valid works as intended"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("")

        # Test that is_valid works as expected
        reconciliation.json_data = self.valid_data
        self.assertTrue(reconciliation.is_valid())

    def test_match_success_response_on_valid_data(self):
        """Checks for proper responses on successful match"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("")
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
        total_matches = ReconciliationGroup.objects.count()

        # Setup the reconciliation object and match the IDs
        reconciliation = BankReconciliation("")
        reconciliation.json_data = self.valid_data
        reconciliation.create_matches()

        # Check for proper number of matches
        self.assertEqual(
            ReconciliationGroup.objects.count(),
            total_matches + 1,
        )

        # Check that proper IDs were matched
        last_match = ReconciliationGroup.objects.last()
        self.assertEqual(
            last_match.banktransactions.first().id,
            self.valid_data["bank_ids"][0]
        )
        self.assertEqual(
            last_match.financialtransactions.first().id,
            self.valid_data["financial_ids"][0]
        )

    def test_error_on_invalid_raw_data(self):
        """Checks error response for invalid raw data"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("a")

        # Check for proper error message
        self.assertEqual(
            reconciliation.errors["post_data"][0],
            "Invalid data submitted to server."
        )

    def test_error_on_missing_bank_id_key(self):
        """Checks error handling on json_data missing bank_id key"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("")

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
        reconciliation = BankReconciliation("")

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
        reconciliation = BankReconciliation("")

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
        reconciliation = BankReconciliation("")

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
        reconciliation = BankReconciliation("")

        # Reconcile the test bank ID
        group = ReconciliationGroup.objects.create()
        self.bank_transactions[0].reconciled = group
        self.bank_transactions[0].save()
        self.financial_transactions[1].reconciled = group
        self.financial_transactions[1].save()

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

    def test_error_on_missing_financial_id_key(self):
        """Checks error handling on json_data missing financial_id key"""
        # Setup the reconciliation object
        reconciliation = BankReconciliation("")

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
        reconciliation = BankReconciliation("")

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
        reconciliation = BankReconciliation("")

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
        reconciliation = BankReconciliation("")

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
        reconciliation = BankReconciliation("")

        # Reconcile the test financial ID
        group = ReconciliationGroup.objects.create()
        self.bank_transactions[1].reconciled = group
        self.bank_transactions[1].save()
        self.financial_transactions[0].reconciled = group
        self.financial_transactions[0].save()

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
