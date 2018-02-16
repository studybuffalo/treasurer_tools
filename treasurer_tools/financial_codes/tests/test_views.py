"""Test cases for the financial_codes app non-form views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from .utils import create_user


class FinancialCodeDashboard(TestCase):
    """Tests for the financial code dashboard view"""

    def setUp(self):
        create_user()

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get("/settings/codes/")

        self.assertRedirects(response, "/accounts/login/?next=/settings/codes/")

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/")

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/index.html")
