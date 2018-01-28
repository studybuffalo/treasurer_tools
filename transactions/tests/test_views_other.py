"""Test cases for other transactions app views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from ..forms import FinancialCodeAssignmentForm

class TransactionsDashboard(TestCase):
    """Tests for the transactions dashboard view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "transactions/tests/fixtures/authentication.json",
    ]

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get("/transactions/")

        self.assertRedirects(response, "/accounts/login/?next=/transactions/")

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("transactions_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("transactions_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "transactions/index.html")

class RetrieveFinancialCodeSystemTest(TestCase):
    """Checks that financial code systems are properly retrieved"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "transactions/tests/fixtures/authentication.json",
        "transactions/tests/fixtures/country.json",
        "transactions/tests/fixtures/demographics.json",
        "transactions/tests/fixtures/financial_code_system.json",
        "transactions/tests/fixtures/budget_year.json",
        "transactions/tests/fixtures/financial_code_group.json",
        "transactions/tests/fixtures/financial_code.json",
        "transactions/tests/fixtures/transaction.json",
        "transactions/tests/fixtures/item.json",
    ]
    
    def setUp(self):
        self.correct_url = "/transactions/expense/add/retrieve-financial-code-systems/"
        self.correct_parameters = {
            "item_date": "2017-01-01",
            "item_form_id": 1,
        }

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(self.correct_url, self.correct_parameters)

        self.assertRedirects(
            response,
            "/accounts/login/?next={}%3Fitem_date%3D2017-01-01%26item_form_id%3D1".format(
                self.correct_url
            )
        )

    def test_404_on_invalid_date(self):
        """Checks that a 404 returns on invalid date"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["item_date"] = ""

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)

        self.assertEqual(response.status_code, 404)
        
    def test_404_on_invalid_item_form_id(self):
        """Checks that a 404 returns on invalid date"""
        # Generate incorrect parameters
        incorrect_parameters = self.correct_parameters
        incorrect_parameters["item_form_id"] = "a"

        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, incorrect_parameters)

        self.assertEqual(response.status_code, 404)

    def test_financial_code_forms_are_returned_on_valid_data(self):
        """Checks that financial_code_forms are returned"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.correct_url, self.correct_parameters)

        forms = response.context["financial_code_forms"]

        # Check that the proper systems are retrieved
        self.assertEqual(
            forms[0].system,
            "CSHP National (2014-04-01 to Present)"
        )

        self.assertEqual(
            forms[1].system,
            "CSHP Alberta Branch (2000-01-01 to 2018-03-31)"
        )

        # Check that a financial code form is provided
        self.assertEqual(
            type(forms[0].form),
            type(FinancialCodeAssignmentForm(system=1, transaction_type="e"))
        )

        self.assertEqual(
            type(forms[1].form),
            type(FinancialCodeAssignmentForm(system=2, transaction_type="e"))
        )
