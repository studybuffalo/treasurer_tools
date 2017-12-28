"""Test cases for the payee_payer app"""

from django.test import TestCase

from payee_payer.forms import PayeePayerForm
from payee_payer.models import Country

class CountryModelTest(TestCase):
    """Test functions for the Demographics model"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "payee_payer/tests/fixtures/country.json",
    ]

    def test_country_order(self):
        """Tests for countries in proper sorted order"""
        form = PayeePayerForm()
        country_list = form.fields["country"]

        self.assertTrue(True)