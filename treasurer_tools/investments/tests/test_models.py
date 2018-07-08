"""Test cases for the investments app"""

from django.test import TestCase

from .utils import create_investment


class InvestmentModelTest(TestCase):
    """Test functions for the Financial Code System model"""

    def setUp(self):
        self.investment = create_investment()

    def test_labels(self):
        """tests a series of fields for proper label generation"""

        # Test name label
        self.assertEqual(
            self.investment._meta.get_field("name").verbose_name,
            "name"
        )

        # Test date_invested label
        self.assertEqual(
            self.investment._meta.get_field("date_invested").verbose_name,
            "date invested"
        )

        # Test amount_invested label
        self.assertEqual(
            self.investment._meta.get_field("amount_invested").verbose_name,
            "amount invested"
        )

        # Test date_matured label
        self.assertEqual(
            self.investment._meta.get_field("date_matured").verbose_name,
            "date matured"
        )

        # Test amount_matured label
        self.assertEqual(
            self.investment._meta.get_field("amount_matured").verbose_name,
            "amount matured"
        )


        # Test rate label
        self.assertEqual(
            self.investment._meta.get_field("rate").verbose_name,
            "rate"
        )

    def test_name_max_length(self):
        """Tests the name field for proper max length"""
        self.assertEqual(
            self.investment._meta.get_field("name").max_length,
            256
        )

    def test_rate_max_length(self):
        """Tests the rate field for proper max length"""
        self.assertEqual(
            self.investment._meta.get_field("rate").max_length,
            256
        )

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        self.assertEqual(
            str(self.investment),
            "2017-02-01 - Term Deposit #1"
        )
