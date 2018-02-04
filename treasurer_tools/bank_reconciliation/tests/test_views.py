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
        
        self.correct_url = "/banking/reconciliation/retrieve-transactions/"
        
    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(self.correct_url)

        self.assertRedirects(
            response,
            "/accounts/login/?next=/banking/reconciliation/retrieve-transactions/"
        )
    
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