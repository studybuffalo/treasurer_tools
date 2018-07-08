"""Test cases for the investments app forms"""

from django.test import TestCase

from investments.forms import InvestmentForm
from investments.models import Investment

from .utils import create_investment


class InvestmentFormTest(TestCase):
    """Tests for the Institution Form"""

    def setUp(self):
        self.valid_data = {
            "name": "Mutual Funds",
            "date_invested": "2017-03-01",
            "amount_invested": 1000.00,
            "date_matured": "2017-06-01",
            "amount_matured": 1005.00,
            "rate": "0.05% per month"
        }

    def test_is_valid_with_valid_data(self):
        """Tests that a is_valid is true when provided valid data"""
        form = InvestmentForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_is_valid_with_invalid_data(self):
        """Tests that a is_valid is true when provided valid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["name"] = None

        form = InvestmentForm(data=invalid_data)

        self.assertFalse(form.is_valid())

    def test_can_add_entry(self):
        """Tests that form properly add new entry"""
        # Count number of investments
        investment_total = Investment.objects.count()

        # Create and save form
        form = InvestmentForm(self.valid_data)
        self.assertTrue(form.is_valid())
        form.save()

        # Check that number of entries increased
        self.assertEqual(Investment.objects.count(), investment_total + 1)

        # Check that name has saved properly
        self.assertEqual(Investment.objects.last().name, self.valid_data["name"])

    def test_can_update_original_entry(self):
        """Tests that form properly updates an old entry"""
        # Create investment
        investment_instance = create_investment()

        # Count number of investments
        investment_total = Investment.objects.count()

        # Create and save form
        form = InvestmentForm(self.valid_data, instance=investment_instance)
        self.assertTrue(form.is_valid())
        form.save()

        # Check that number of entries remains the same
        self.assertEqual(Investment.objects.count(), investment_total)

        # Check that name has updated
        self.assertEqual(Investment.objects.last().name, self.valid_data["name"])
