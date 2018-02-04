"""Test cases for the bank_reconciliation app views"""

import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from ..models import ReconciliationMatch
from ..utils import ReconciliationMatch
from bank_transactions.models import Statement, BankTransaction
from payee_payer.models import Demographics
from transactions.models import Transaction
from utils.utils_tests import (
    create_authentication_entries, create_reconciliation_matches, create_financial_transactions_and_items, 
    create_bank_transactions,
)

class ReconciliationDashboardTest(TestCase):
    """Tests for the banking reconciliation view"""
    # pylint: disable=no-member,protected-access
    
    def setUp(self):
        create_authentication_entries()
        create_reconciliation_matches()

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get("/banking/reconciliation/")

        self.assertRedirects(response, "/accounts/login/?next=/banking/reconciliation/")

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/reconciliation/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_reconciliation"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_reconciliation"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "bank_reconciliation/index.html")

class ReconciliationRetrieveTest(TestCase):
    """Tests the retrieve transaction view"""
    # pylint: disable=no-member,protected-access
    
    def setUp(self):
        create_authentication_entries()
        create_reconciliation_matches()

        self.correct_url = "/banking/reconciliation/retrieve-transactions/"
        self.correct_financial_parameters = {
            "transaction_type": "financial",
            "date_start": "2000-01-01",
            "date_end": "2018-12-31",
        }
        self.correct_bank_parameters = {
            "transaction_type": "bank",
            "date_start": "2000-01-01",
            "date_end": "2018-12-31",
        }

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(self.correct_url, self.correct_financial_parameters)

        self.assertRedirects(
            response,
            (
                "/accounts/login/?next="
                "/banking/reconciliation/retrieve-transactions/"
                "%3Ftransaction_type%3Dfinancial%26date_start%3D2000-01-01"
                "%26date_end%3D2018-12-31"
            )
        )

    def test_empty_response_on_missing_transaction_type(self):
        """Test confirms no data returned on missing transaction_type"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["transaction_type"] = ""

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_invalid_transaction_type(self):
        """Test confirms no data returned on invalid transaction_type"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["transaction_type"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_missing_date_start(self):
        """Test confirms no data returned on missing date_start"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_start"] = ""

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_missing_date_end(self):
        """Test confirms no data returned on missing date_end"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_end"] = ""

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_invalid_financial_date_start(self):
        """Test confirms no data returned on invalid financial date_start"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_start"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_invalid_bank_date_start(self):
        """Test confirms no data returned on invalid bank date_start"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_bank_parameters
        incorrect_parameters["date_start"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))

    def test_empty_response_on_invalid_financial_date_end(self):
        """Test confirms no data returned on invalid financial date_end"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_end"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_invalid_bank_date_end(self):
        """Test confirms no data returned on invalid bank date_end"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_bank_parameters
        incorrect_parameters["date_end"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))

    def test_proper_json_response_on_valid_financial_data(self):
        """Checks for a proper json response with valid financial data"""
        # Get current count of the financial transactions
        total_financial_transactions = Transaction.objects.count()

        # Retrieve the data
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, self.correct_financial_parameters)
        
        json_data = json.loads(response.content)

        # Checks that data was returned
        self.assertTrue(json_data)
        
        # Checks for the proper keys
        self.assertTrue("data" in json_data)
        self.assertTrue("type" in json_data)

        # Check that values were retruned
        self.assertEqual(len(json_data["data"]), total_financial_transactions)
        self.assertEqual(json_data["type"], "financial")
        
    def test_proper_json_response_on_valid_bank_data(self):
        """Checks for a proper json response with valid bank data"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, self.correct_bank_parameters)
        
        json_data = json.loads(response.content)

        # Checks that data was returned
        self.assertTrue(json_data)
        
        # Checks for the proper keys
        self.assertTrue("data" in json_data)
        self.assertTrue("type" in json_data)

        # Check that values were retruned
        self.assertEqual(len(json_data["data"]), 4)
        self.assertEqual(json_data["type"], "bank")

class ReconciliationMatchTest(TestCase):
    """Tests the match transaction view"""
    # pylint: disable=no-member,protected-access
    
    def setUp(self):
        create_authentication_entries()
        financial_transactions = create_financial_transactions_and_items()
        bank_transactions = create_bank_transactions()

        self.correct_url = "/banking/reconciliation/match-transactions/"
        self.correct_parameters = {
            "financial_ids": [financial_transactions[0].id],
            "bank_ids": [bank_transactions[0].id],
        }

    def test_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.post(self.correct_url, self.correct_parameters)

        self.assertRedirects(
            response,
            "/accounts/login/?next=/banking/reconciliation/match-transactions/"
        )
        
    def test_error_response_on_invalid_data_format(self):
        """Checks for proper error message on invalid data formatting"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(self.correct_url, "A1", content_type="text")

        json_data = json.loads(response.content)

        self.assertEqual(
            json_data["errors"]["post_data"][0],
            "Invalid data submitted to server."
        )

    def test_error_response_on_invalid_financial_ids(self):
        """Checks for proper error message on invalid financial ID format"""
        # Setup incorrect financial id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["financial_ids"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["financial_id"][0],
            "a is not a valid financial transaction ID. Please make a valid selection."
        )

    def test_error_response_on_nonexistent_financial_ids(self):
        """Checks for proper error message on nonexistent financial ID"""
        # Setup incorrect financial id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["financial_ids"] = [999999999]

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["financial_id"][0],
            "999999999 is not a valid financial transaction ID. Please make a valid selection."
        )
        
    def test_error_response_on_already_reconciled_financial_ids(self):
        """Checks for proper error message on reconciled financial ID"""
        # Reconcile the correct transactions
        ReconciliationMatch.objects.create(
            financial_transaction=Transaction.objects.get(id=self.correct_parameters["financial_ids"][0]),
            bank_transaction=BankTransaction.objects.get(id=self.correct_parameters["bank_ids"][0]),
        )

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(self.correct_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["financial_id"][0],
            (
                "2017-06-01 - Expense - Test User - Test Expense Transaction 1 is already "
                "reconciled. Unmatch the transaction before reassigning it."
            )
        )
        
    def test_error_response_on_missing_financial_ids(self):
        """Checks for proper error message on missing financial ID"""
        # Setup incorrect financial id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["financial_ids"] = []

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["financial_id"][0],
            "Please select at least one financial transaction."
        )

    def test_error_response_on_invalid_bank_ids(self):
        """Checks for proper error message on invalid bank ID format"""
        # Setup incorrect bank id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["bank_ids"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["bank_id"][0],
            "a is not a valid bank transaction ID. Please make a valid selection."
        )
        
    def test_error_response_on_nonexistent_bank_ids(self):
        """Checks for proper error message on nonexistent bank ID"""
        # Setup incorrect bank id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["bank_ids"] = [999999999]

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["bank_id"][0],
            "999999999 is not a valid bank transaction ID. Please make a valid selection."
        )
        
    def test_error_response_on_already_reconciled_bank_ids(self):
        """Checks for proper error message on reconciled bank ID"""
        # Reconcile the correct transactions
        ReconciliationMatch.objects.create(
            financial_transaction=Transaction.objects.get(id=self.correct_parameters["financial_ids"][0]),
            bank_transaction=BankTransaction.objects.get(id=self.correct_parameters["bank_ids"][0]),
        )

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(self.correct_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["bank_id"][0],
            (
                "2017-01-01 - Cheque #0001 is already reconciled. Unmatch "
                "the transaction before reassigning it."
            )
        )
        
    def test_error_response_on_missing_bank_ids(self):
        """Checks for proper error message on missing bank ID"""
        # Setup incorrect bank id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["bank_ids"] = []

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["bank_id"][0],
            "Please select at least one bank transaction."
        )

    def test_success_on_valid_data(self):
        """Checks for proper matching on valid data"""
        # Count number of matches there are currently
        total_matches = ReconciliationMatch.objects.count()
        
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(self.correct_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        # Check for valid success responses
        self.assertEqual(len(json_data["success"]["financial_id"]), 1)
        self.assertEqual(
            json_data["success"]["financial_id"][0],
            self.correct_parameters["financial_ids"][0]
        )
        self.assertEqual(len(json_data["success"]["bank_id"]), 1)
        self.assertEqual(
            json_data["success"]["bank_id"][0],
            self.correct_parameters["bank_ids"][0]
        )

        # Check for proper number of matches
        self.assertEqual(
            ReconciliationMatch.objects.count(),
            total_matches + 1,
        )

        # Check that proper IDs were matched
        last_match = ReconciliationMatch.objects.last()
        self.assertEqual(
            last_match.bank_transaction.id,
            self.correct_parameters["financial_ids"][0]
        )
        self.assertEqual(
            last_match.financial_transaction.id,
            self.correct_parameters["bank_ids"][0]
        )

class ReconciliationUnmatchTest(TestCase):
    """Tests the unmatch transaction view"""
    # pylint: disable=no-member,protected-access
    
    def setUp(self):
        create_authentication_entries()
        reconciliation_matches = create_reconciliation_matches()
        
        self.correct_url = "/banking/reconciliation/unmatch-transactions/"
        self.correct_parameters = {
            "financial_ids": [reconciliation_matches[0].financial_transaction.id],
            "bank_ids": [reconciliation_matches[0].bank_transaction.id],
        }

    def test_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.post(self.correct_url, self.correct_parameters)

        self.assertRedirects(
            response,
            "/accounts/login/?next=/banking/reconciliation/unmatch-transactions/"
        )
        
    def test_error_response_on_invalid_data_format(self):
        """Checks for proper error message on invalid data formatting"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(self.correct_url, "A1", content_type="text")

        json_data = json.loads(response.content)

        self.assertEqual(
            json_data["errors"]["post_data"][0],
            "Invalid data submitted to server."
        )

    def test_error_response_on_invalid_financial_ids(self):
        """Checks for proper error message on invalid financial ID format"""
        # Setup incorrect financial id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["financial_ids"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["financial_id"][0],
            "a is not a valid financial transaction ID. Please make a valid selection."
        )

    def test_error_response_on_nonexistent_financial_ids(self):
        """Checks for proper error message on nonexistent financial ID"""
        # Setup incorrect financial id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["financial_ids"] = [999999999]

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["financial_id"][0],
            "999999999 is not a valid financial transaction ID. Please make a valid selection."
        )
        
    def test_error_response_on_unreconciled_financial_ids(self):
        """Checks for proper error message on reconciled financial ID"""
        # Create an invalid financial transaction
        new_transaction = Transaction.objects.create(
            payee_payer=Demographics.objects.first(),
            transaction_type="e",
            memo="Unreconciled Transaction Test",
            date_submitted = "2017-01-01",
        )

        # Replace the financial transaction with the new one
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["financial_ids"] = [new_transaction.id]

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["financial_id"][0],
            (
                "2017-01-01 - Expense - Test User - Unreconciled Transaction "
                "Test is not a matched transaction."
            )
        )
        
    def test_error_response_on_missing_financial_ids(self):
        """Checks for proper error message on missing financial ID"""
        # Setup incorrect financial id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["financial_ids"] = []

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["financial_id"][0],
            "Please select at least one financial transaction."
        )

    def test_error_response_on_invalid_bank_ids(self):
        """Checks for proper error message on invalid bank ID format"""
        # Setup incorrect bank id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["bank_ids"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["bank_id"][0],
            "a is not a valid bank transaction ID. Please make a valid selection."
        )
        
    def test_error_response_on_nonexistent_bank_ids(self):
        """Checks for proper error message on nonexistent bank ID"""
        # Setup incorrect bank id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["bank_ids"] = [999999999]

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["bank_id"][0],
            "999999999 is not a valid bank transaction ID. Please make a valid selection."
        )
        
    def test_error_response_on_unreconciled_bank_ids(self):
        """Checks for proper error message on reconciled bank ID"""
        # Create an invalid bank transaction
        new_transaction = BankTransaction.objects.create(
            statement=Statement.objects.first(),
            date_transaction="2017-01-01",
            description_bank="Unreconciled Bank Transaction",
        )

        # Setup incorrect bank id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["bank_ids"] = [new_transaction.id]

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["bank_id"][0],
            "2017-01-01 - Unreconciled Bank Transaction is not a matched transaction."
        )
        
    def test_error_response_on_missing_bank_ids(self):
        """Checks for proper error message on missing bank ID"""
        # Setup incorrect bank id data
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["bank_ids"] = []

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(incorrect_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)
        
        self.assertEqual(
            json_data["errors"]["bank_id"][0],
            "Please select at least one bank transaction."
        )

    def test_success_on_valid_data(self):
        """Checks for proper unmatching on valid data"""
        # Count number of matches there are currently
        total_matches = ReconciliationMatch.objects.count()

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            json.dumps(self.correct_parameters),
            content_type="application/json"
        )

        json_data = json.loads(response.content)

        # Check for valid success responses
        self.assertEqual(len(json_data["success"]["financial_id"]), 1)
        self.assertEqual(
            json_data["success"]["financial_id"][0],
            self.correct_parameters["financial_ids"][0]
        )
        self.assertEqual(len(json_data["success"]["bank_id"]), 1)
        self.assertEqual(
            json_data["success"]["bank_id"][0],
            self.correct_parameters["bank_ids"][0]
        )

        # Check that number of matches has decreased
        self.assertEqual(
            ReconciliationMatch.objects.count(),
            total_matches - 1
        )

        # Check that this match no long exists
        self.assertFalse(ReconciliationMatch.objects.filter(id=1).exists())
