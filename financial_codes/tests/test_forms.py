"""Test cases for the bank_transaction app"""

from django.test import TestCase

from financial_codes.forms import FinancialCodeSystemForm

class FinancialCodeSystemFormTest(TestCase):
    """Test functions for the Financial Code System model"""
    # pylint: disable=no-member,protected-access
    
    def setUp(self):
        # Add standard test data
        self.correct_data = {
            "title": "CSHP National",
            "date_start": "2017-01-01",
            "date_end": "2016-01-01",
        }

    def test_date_end_validation(self):
        """Tests that the end date validation catches invalid end dates"""
        # Create a form instance with invalid data
        form = FinancialCodeSystemForm(data=self.correct_data)

        # Checks that it is not valid
        self.assertFalse(form.is_valid())

        # Check that it is the end date causing the invalid form
        self.assertEqual(
            form["date_end"].errors[0],
            "End date must occur after the start date."
        )