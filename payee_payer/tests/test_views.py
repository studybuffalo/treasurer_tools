"""Test cases for the payee_payer app"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from payee_payer.models import Country

class CountryModelTest(TestCase):
    """Test functions for the Demographics model"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "payee_payer/tests/fixtures/authentication.json",
        "payee_payer/tests/fixtures/country.json",
        "payee_payer/tests/fixtures/demographics.json",
    ]

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        login = self.client.login(username="user", password="abcd123456")
        response = self.client.get("/payee-payer/")

        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        login = self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("payee_payer_dashboard"))

        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        login = self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("payee_payer_dashboard"))

        self.assertTemplateUsed(response, "payee_payer/index.html")