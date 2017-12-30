"""Test cases for the bank_transactions app views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from bank_transactions.models import Statement, BankTransaction

class BankDashboardTest(TestCase):
    """Tests for the bank dashboard view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
    ]

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get("/banking/")

        self.assertRedirects(response, "/accounts/login/?next=/banking/")

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/index.html")

class StatementAddTest(TestCase):
    """Tests for the add statement view"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
    ]
    
    def setUp(self):
        self.CORRECT_STATEMENT_DATA = {
            "account": 1,
            "date_start": "2017-01-01",
            "date_end": "2017-01-31",
            "banktransaction_set-TOTAL_FORMS": 0,
            "banktransaction_set-INITIAL_FORMS": 0,
            "banktransaction_set-MIN_NUM_FORMS": 0,
            "banktransaction_set-MAX_NUM_FORMS": 1000,
        }
        self.CORRECT_TRANSACTION_DATA = {
            "account": 1,
            "date_start": "2017-01-01",
            "date_end": "2017-01-31",
            "banktransaction_set-0-date_transaction": "2017-01-01",
            "banktransaction_set-0-description_bank": "CHQ#0001",
            "banktransaction_set-0-description_user": "Cheque #0001",
            "banktransaction_set-0-amount_debit": 100.00,
            "banktransaction_set-0-amount_credit": 0.00,
            "banktransaction_set-TOTAL_FORMS": 1,
            "banktransaction_set-INITIAL_FORMS": 0,
            "banktransaction_set-MIN_NUM_FORMS": 0,
            "banktransaction_set-MAX_NUM_FORMS": 1000,
        }
            

    def test_statement_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("statement_add"))

        self.assertEqual(response.status_code, 302)

    def test_statement_add_url_exists_at_desired_location(self):
        """Checks that the add statement page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/statement/add/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_statement_add_accessible_by_name(self):
        """Checks that add statement page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("statement_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_statement_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("statement_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/add.html")

    def test_statement_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("statement_add"), self.CORRECT_STATEMENT_DATA, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_dashboard"))

    def test_statement_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("statement_add"), self.CORRECT_STATEMENT_DATA, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one statement was added
        self.assertEqual(1, Statement.objects.count())

class StatementEditTest(TestCase):
    """Tests for the edit statement view"""

class StatementDeleteTest(TestCase):
    """Tests for the delete statement view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
    ]

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get("/banking/")

        self.assertRedirects(response, "/accounts/login/?next=/banking/")

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/index.html")
