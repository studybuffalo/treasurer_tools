"""Test cases for the bank_reconciliation app views"""

import json

from django.core.urlresolvers import reverse
from django.test import TestCase

from bank_transactions.models import Statement, BankTransaction
from payee_payer.models import Demographics
from transactions.models import Transaction

from ..models import ReconciliationMatch
from ..utils import ReconciliationMatch

from .utils import create_user, create_bank_transactions, create_financial_transactions

class ReconciliationDashboardTest(TestCase):
    """Tests for the banking reconciliation view"""
    # pylint: disable=no-member,protected-access
    
    def setUp(self):
        create_user()
        
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
        create_user()
        create_bank_transactions()
        create_financial_transactions()

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

class ReconciliationMatchTest(TestCase):
    """Tests the match transaction view"""
    # pylint: disable=no-member,protected-access
    
    def test_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.post("/banking/reconciliation/match-transactions/")

        self.assertRedirects(
            response,
            "/accounts/login/?next=/banking/reconciliation/match-transactions/"
        )
        
class ReconciliationUnmatchTest(TestCase):
    """Tests the unmatch transaction view"""
    # pylint: disable=no-member,protected-access
    
    def test_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.post("/banking/reconciliation/unmatch-transactions/")

        self.assertRedirects(
            response,
            "/accounts/login/?next=/banking/reconciliation/unmatch-transactions/"
        )
        
# TODO: Add test to views to ensure proper responses are returned (note: majority of testing is done in test_utils