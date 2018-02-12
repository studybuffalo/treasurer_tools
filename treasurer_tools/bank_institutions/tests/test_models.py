"""Test cases for the bank_institutions app"""

from django.test import TestCase

from bank_institutions.models import Institution, Account

from .utils import create_bank_institution, create_bank_account

class InstitutionModelTest(TestCase):
    """Test functions for the Institution model"""

    def setUp(self):
        create_bank_institution()

    def test_labels(self):
        """Tests a series of fields for proper label generation"""
        # Get an institution reference
        institution = Institution.objects.first()

        # Test name label
        self.assertEqual(
            institution._meta.get_field("name").verbose_name,
            "name",
        )

        # Test address label
        self.assertEqual(
            institution._meta.get_field("address").verbose_name,
            "address"
        )

        # Test phone label
        self.assertEqual(
            institution._meta.get_field("phone").verbose_name,
            "phone number"
        )

        # Test fax label
        self.assertEqual(
            institution._meta.get_field("fax").verbose_name,
            "fax number"
        )

    def test_max_length(self):
        """Tests a series of fields for proper max length"""
        # Get an institution reference
        institution = Institution.objects.first()

        # Test name field
        self.assertEqual(
            institution._meta.get_field("name").max_length,
            250
        )

        # Test address field
        self.assertEqual(
            institution._meta.get_field("address").max_length,
            1000
        )

        # Test phone field
        self.assertEqual(
            institution._meta.get_field("phone").max_length,
            30
        )

        # Test fax field
        self.assertEqual(
            institution._meta.get_field("fax").max_length,
            30
        )

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        # Get an institution reference
        institution = Institution.objects.first()

        self.assertEqual(
            str(institution),
            "Test Institution"
        )

class AccountModelTest(TestCase):
    """Test functions for the Account model"""

    def setUp(self):
        create_bank_account()

    def test_labels(self):
        """Tests a series of fields for proper label generation"""
        # Get an institution reference
        account = Account.objects.first()

        # Test institution label
        self.assertEqual(
            account._meta.get_field("institution").verbose_name,
            "institution",
        )

        # Test account_number label
        self.assertEqual(
            account._meta.get_field("account_number").verbose_name,
            "account number"
        )

        # Test name label
        self.assertEqual(
            account._meta.get_field("name").verbose_name,
            "name"
        )

        # Test status label
        self.assertEqual(
            account._meta.get_field("status").verbose_name,
            "status"
        )

    def test_max_length(self):
        """Tests a series of fields for proper max length"""
        # Get an institution reference
        account = Account.objects.first()

        # Test account_number field
        self.assertEqual(
            account._meta.get_field("account_number").max_length,
            100
        )

        # Test name field
        self.assertEqual(
            account._meta.get_field("name").max_length,
            100
        )

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        # Get an institution reference
        account = Account.objects.first()

        self.assertEqual(
            str(account),
            "Test Institution Chequing Account (123456789)"
        )
