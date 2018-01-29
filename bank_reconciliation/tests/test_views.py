"""Test cases for the bank_reconciliation app views"""

import json

from django.core.urlresolvers import reverse
from django.test import TestCase

FIXTURES = [
    "bank_reconciliation/tests/fixtures/account.json",
    "bank_reconciliation/tests/fixtures/authentication.json",
    "bank_reconciliation/tests/fixtures/bank_transaction.json",
    "bank_reconciliation/tests/fixtures/country.json",
    "bank_reconciliation/tests/fixtures/demographics.json",
    "bank_reconciliation/tests/fixtures/institution.json",
    "bank_reconciliation/tests/fixtures/item.json",
    "bank_reconciliation/tests/fixtures/reconciliation_match.json",
    "bank_reconciliation/tests/fixtures/statement.json",
    "bank_reconciliation/tests/fixtures/transaction.json",
]

class ReconciliationDashboardTest(TestCase):
    """Tests for the banking reconciliation view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_reconciliation/tests/fixtures/authentication.json",
    ]

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

    fixtures = FIXTURES
    
    def setUp(self):
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
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["transaction_type"] = ""

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_invalid_transaction_type(self):
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["transaction_type"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_missing_date_start(self):
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_start"] = ""

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_invalid_date_start(self):
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_start"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_missing_date_end(self):
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_end"] = ""

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))
        
    def test_empty_response_on_invalid_date_end(self):
        # Generate incorrect parameters
        incorrect_parameters = self.correct_financial_parameters
        incorrect_parameters["date_end"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)
        
        # Check for blank json response
        self.assertFalse(json.loads(response.content))

    def test_proper_json_response_on_valid_financial_data(self):
        """Checks for a proper json response with valid financial data"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, self.correct_financial_parameters)
        
        json_data = json.loads(response.content)

        # Checks that data was returned
        self.assertTrue(json_data)
        
        # Checks for the proper keys
        self.assertTrue("data" in json_data)
        self.assertTrue("type" in json_data)

        # Check that values were retruned
        self.assertEqual(len(json_data["data"]), 2)
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

class ReconciliationUnmatchTest(TestCase):
    """Tests the unmatch transaction view"""
     # pylint: disable=no-member,protected-access