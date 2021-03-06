"""Test cases for the bank_reconciliation app views"""

import json

from django.urls import reverse
from django.test import TestCase

from bank_reconciliation.models import ReconciliationGroup

from .utils import create_user, create_bank_transactions, create_financial_transactions


class ReconciliationDashboardTest(TestCase):
    """Tests for the banking reconciliation view"""

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
        response = self.client.get(reverse("bank_reconciliation:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_reconciliation:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "bank_reconciliation/index.html")

class ReconciliationRetrieveTest(TestCase):
    """Tests the retrieve transaction view"""

    def setUp(self):
        create_user()

        self.correct_url = "/banking/reconciliation/retrieve-transactions/"

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(self.correct_url)

        self.assertRedirects(
            response,
            "/accounts/login/?next=/banking/reconciliation/retrieve-transactions/"
        )

    def test_no_redirect_on_logged_in(self):
        """Checks that there is no redirect on logged in user"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url)

        self.assertEqual(
            response.status_code,
            200
        )

    def test_for_response_on_valid_data(self):
        """Checks that a JSON response is received on valid data"""
        # Setup valid data
        valid_data = {
            "transaction_type": "bank",
            "date_start": "2000-01-01",
            "date_end": "2018-12-31",
        }

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            self.correct_url,
            valid_data,
        )
        json_response = str(response.content, encoding="UTF-8")

        self.assertJSONEqual(
            json_response,
            {"type": "bank", "data": [], "errors": None}
        )

    def test_for_response_on_invalid_data(self):
        """Checks that a JSON response is received on invalid data"""
        # Setup invalid data
        invalid_data = {
            "transaction_type": "a",
            "date_start": "2000-01-01",
            "date_end": "2018-12-31",
        }

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            self.correct_url,
            invalid_data,
        )
        json_response = str(response.content, encoding="UTF-8")

        self.assertJSONEqual(
            json_response,
            {
                "type": None,
                "data": None,
                "errors": {"transaction_type": "Invalid transaction type provided."}
            }
        )

class ReconciliationMatchTest(TestCase):
    """Tests the match transaction view"""

    def setUp(self):
        create_user()

        self.correct_url = "/banking/reconciliation/match-transactions/"
        self.bank_transactions = create_bank_transactions()
        self.financial_transactions = create_financial_transactions()
        self.valid_data = {
            "bank_ids": [self.bank_transactions[0].id],
            "financial_ids": [self.financial_transactions[0].id],
        }

    def test_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.post(self.correct_url)

        self.assertRedirects(
            response,
            "/accounts/login/?next=/banking/reconciliation/match-transactions/"
        )

    def test_no_redirect_on_logged_in(self):
        """Checks that there is no redirect on logged in user"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(self.correct_url)

        self.assertEqual(
            response.status_code,
            200
        )

    def test_for_response_on_valid_data(self):
        """Checks that a JSON response is received on valid data"""

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

        json_response = str(response.content, encoding="UTF-8")

        self.assertTrue("success" in json_response)
        self.assertTrue("errors" in json_response)

    def test_for_response_on_invalid_data(self):
        """Checks that a JSON response is received on invalid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["bank_ids"] = [""]

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            data=json.dumps(invalid_data),
            content_type="application/json",
        )

        json_response = str(response.content, encoding="UTF-8")

        self.assertTrue("success" in json_response)
        self.assertTrue("errors" in json_response)

class ReconciliationUnmatchTest(TestCase):
    """Tests the unmatch transaction view"""

    def setUp(self):
        create_user()

        # Create a reconcilation match for testing
        group = ReconciliationGroup.objects.create()

        bank_transactions = create_bank_transactions()
        bank_transaction = bank_transactions[0]
        bank_transaction.reconciled = group
        bank_transaction.save()

        financial_transactions = create_financial_transactions()
        financial_transaction = financial_transactions[0]
        financial_transaction.reconciled = group
        financial_transaction.save()

        self.correct_url = "/banking/reconciliation/unmatch-transactions/"
        self.group = group
        self.valid_data = {
            "reconciliation_group_ids": [group.id],
        }

    def test_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.post("/banking/reconciliation/unmatch-transactions/")

        self.assertRedirects(
            response,
            "/accounts/login/?next=/banking/reconciliation/unmatch-transactions/"
        )

    def test_no_redirect_on_logged_in(self):
        """Checks that there is no redirect on logged in user"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(self.correct_url)

        self.assertEqual(
            response.status_code,
            200
        )

    def test_for_response_on_valid_data(self):
        """Checks that a JSON response is received on valid data"""
        # Match transactions for test

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            data=json.dumps(self.valid_data),
            content_type="application/json",
        )

        json_response = str(response.content, encoding="UTF-8")

        self.assertTrue("errors" in json_response)

    def test_for_response_on_invalid_data(self):
        """Checks that a JSON response is received on invalid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["reconciliation_group_ids"] = ["x"]

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            self.correct_url,
            data=json.dumps(invalid_data),
            content_type="application/json",
        )

        json_response = str(response.content, encoding="UTF-8")

        self.assertTrue("errors" in json_response)
