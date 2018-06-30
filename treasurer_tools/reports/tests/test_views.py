"""Test cases for other transactions app views"""

from decimal import Decimal

from django.urls import reverse
from django.test import TestCase

from financial_codes.models import FinancialCodeSystem
from .utils import create_user, create_financial_transactions

class ReportsDashboard(TestCase):
    """Tests for the reports dashboard view"""

    def setUp(self):
        create_user()

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(reverse("reports:dashboard"))

        self.assertRedirects(response, "/accounts/login/?next=/reports/")

    def test_dashboard_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("reports:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible and there was no dedirection
        self.assertEqual(response.status_code, 200)

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/reports/")

        # Check that page is accessible and there was no dedirection
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("reports:dashboard"))

        # Check for proper template
        self.assertTemplateUsed(response, "reports/index.html")

class IncomeStatementDashboard(TestCase):
    """Tests for income statement dashboard view"""

    def setUp(self):
        create_user()

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(reverse("reports:income_statement"))

        self.assertRedirects(response, "/accounts/login/?next=/reports/income-statement/")

    def test_dashboard_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("reports:income_statement"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible and there was no dedirection
        self.assertEqual(response.status_code, 200)

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/reports/income-statement/")

        # Check that page is accessible and there was no dedirection
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("reports:income_statement"))

        # Check for proper template
        self.assertTemplateUsed(response, "reports/income_statement.html")

class RetrieveTransactionsTest(TestCase):
    """Checks that transactions are retrieved properly"""

    def setUp(self):
        create_user()
        create_financial_transactions()

        financial_code_system = FinancialCodeSystem.objects.first().id

        self.url = "/reports/income-statement/retrieve-report/"
        self.valid_args = {
            "financial_code_system": financial_code_system,
            "date_start": "2016-04-01",
            "date_end": "2018-03-31"
        }

    def test_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(self.url, self.valid_args)

        self.assertRedirects(
            response,
            "/accounts/login/?next={}%3Ffinancial_code_system%3D{}%26date_start%3D{}%26date_end%3D{}".format(
                self.url, self.valid_args["financial_code_system"],
                self.valid_args["date_start"], self.valid_args["date_end"]
            )
        )

    def test_no_redirect_if_logged_in(self):
        """Checks no redirect if user is logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, self.valid_args)

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible and there was no dedirection
        self.assertEqual(response.status_code, 200)

    def test_retrieval_on_valid_data(self):
        """Checks that transactions are retrieved when provided with valid data"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, self.valid_args)

        # Check number of revenue codes received
        self.assertEqual(
            len(response.context["revenue_codes"]),
            1
        )

        # Check number of expense codes received
        self.assertEqual(
            len(response.context["expense_codes"]),
            1
        )

    def test_code_total(self):
        """Tests that amounts are totaled properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, self.valid_args)

        # Check the total for revenue codes
        self.assertEqual(
            response.context["revenue_codes"][0]["total"],
            Decimal("1500.00")
        )

        # Check the total for expense codes
        self.assertEqual(
            response.context["expense_codes"][0]["total"],
            Decimal("347.29")
        )

    def test_date_start_filter(self):
        """Checks that you can filter by start date"""
        # Setup modified date
        modified_args = self.valid_args
        modified_args["date_start"] = "2017-06-01"

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, modified_args)

        # Check number of revenue codes received
        self.assertEqual(
            len(response.context["revenue_codes"]),
            0
        )

        # Check number of expense codes received
        self.assertEqual(
            len(response.context["expense_codes"]),
            1
        )

    def test_date_end_filter(self):
        """Checks that you can filter by end date"""
        # Setup modified date
        modified_args = self.valid_args
        modified_args["date_end"] = "2017-05-31"

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, modified_args)

        # Check number of revenue codes received
        self.assertEqual(
            len(response.context["revenue_codes"]),
            1
        )

        # Check number of expense codes received
        self.assertEqual(
            len(response.context["expense_codes"]),
            0
        )

    def test_invalid_financial_code_system(self):
        """Tests that filtering handles invalid financial_code_system"""
        # Setup modified date
        invalid_args = self.valid_args
        invalid_args["financial_code_system"] = ""

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, invalid_args)

        # Check number of revenue codes received
        self.assertIsNone(response.context["revenue_codes"])

        # Check number of expense codes received
        self.assertIsNone(response.context["expense_codes"])

    def test_invalid_date_start(self):
        """Tests that filtering handles invalid start date"""
        # Setup modified date
        invalid_args = self.valid_args
        invalid_args["date_start"] = ""

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, invalid_args)

        # Check number of revenue codes received
        self.assertIsNone(response.context["revenue_codes"])

        # Check number of expense codes received
        self.assertIsNone(response.context["expense_codes"])

    def test_invalid_date_end(self):
        """Tests that filtering handles invalid end date"""
        # Setup modified date
        invalid_args = self.valid_args
        invalid_args["date_end"] = ""

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, invalid_args)

        # Check number of revenue codes received
        self.assertIsNone(response.context["revenue_codes"])

        # Check number of expense codes received
        self.assertIsNone(response.context["expense_codes"])
