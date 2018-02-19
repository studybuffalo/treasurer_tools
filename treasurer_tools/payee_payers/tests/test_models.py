"""Test cases for the payee_payer app"""

from django.test import TestCase

from .utils import create_country, create_demographics


class CountryModelTest(TestCase):
    """Test functions for the Country model"""

    def setUp(self):
        self.country = create_country()

    def test_country_verbose_name_plural(self):
        """Tests for expected model verbose name"""

        self.assertEqual(
            self.country._meta.verbose_name_plural,
            "countries"
        )

    def test_country_code_label(self):
        """Tests for expected country code label"""

        self.assertEqual(
            self.country._meta.get_field("country_code").verbose_name,
            "country code"
        )

    def test_country_name_label(self):
        """Tests for expected country name label"""

        self.assertEqual(
            self.country._meta.get_field("country_name").verbose_name,
            "country name"
        )

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        self.assertEqual(
            str(self.country),
            "Canada"
        )

class PayeePayersModelTest(TestCase):
    """Test functions for the Payee/Payers model"""

    def setUp(self):
        self.payee_payer = create_demographics()

    def test_labels(self):
        """Tests a series of fields for proper label generation"""

        # Test name label
        self.assertEqual(
            self.payee_payer._meta.get_field("name").verbose_name,
            "name"
        )

        # Test address label
        self.assertEqual(
            self.payee_payer._meta.get_field("address").verbose_name,
            "address"
        )

        # Test city label
        self.assertEqual(
            self.payee_payer._meta.get_field("city").verbose_name,
            "city"
        )

        # Test province label
        self.assertEqual(
            self.payee_payer._meta.get_field("province").verbose_name,
            "province"
        )

        # Test country label
        self.assertEqual(
            self.payee_payer._meta.get_field("country").verbose_name,
            "country"
        )

        # Test postal_code label
        self.assertEqual(
            self.payee_payer._meta.get_field("postal_code").verbose_name,
            "postal code"
        )

        # Test phone label
        self.assertEqual(
            self.payee_payer._meta.get_field("phone").verbose_name,
            "phone number"
        )

        # Test fax label
        self.assertEqual(
            self.payee_payer._meta.get_field("fax").verbose_name,
            "fax number"
        )

        # Test email label
        self.assertEqual(
            self.payee_payer._meta.get_field("email").verbose_name,
            "email"
        )

        # Test status label
        self.assertEqual(
            self.payee_payer._meta.get_field("status").verbose_name,
            "status"
        )

    def test_max_length(self):
        """Tests a series of fields for proper max length"""

        # Test name max length
        self.assertEqual(
            self.payee_payer._meta.get_field("name").max_length,
            250
        )

        # Test address max length
        self.assertEqual(
            self.payee_payer._meta.get_field("address").max_length,
            1000
        )

        # Test city max length
        self.assertEqual(
            self.payee_payer._meta.get_field("city").max_length,
            250
        )

        # Test province max length
        self.assertEqual(
            self.payee_payer._meta.get_field("province").max_length,
            100
        )

        # Test postal_code max length
        self.assertEqual(
            self.payee_payer._meta.get_field("postal_code").max_length,
            10
        )

        # Test phone max length
        self.assertEqual(
            self.payee_payer._meta.get_field("phone").max_length,
            30
        )

        # Test fax max length
        self.assertEqual(
            self.payee_payer._meta.get_field("fax").max_length,
            30
        )

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        self.assertEqual(str(self.payee_payer), "Test User")
