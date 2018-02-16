"""Test cases for the financial codes app forms"""

from django.test import TestCase

from financial_codes.forms import FinancialCodeSystemForm, BudgetYearForm, FinancialCodeForm
from financial_codes.models import FinancialCodeSystem

class FinancialCodeSystemFormTest(TestCase):
    """Test functions for the Financial Code System form"""

    def setUp(self):
        # Add standard test data
        self.valid_data = {
            "title": "CSHP National",
            "date_start": "2017-01-01",
            "date_end": "2017-12-31",
        }

    def test_date_end_validation(self):
        """Tests that the end date validation catches invalid end dates"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["date_end"] = "2016-12-31"

        # Create a form instance with invalid data
        form = FinancialCodeSystemForm(data=invalid_data)

        # Checks that it is not valid
        self.assertFalse(form.is_valid())

        # Check that it is the end date causing the invalid form
        self.assertEqual(
            form["date_end"].errors[0],
            "The end date must occur after the start date."
        )

    def test_missing_start_date_validation(self):
        """Tests that custom validation handles missing start date"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["date_start"] = "2017"

         # Create a form instance with invalid data
        form = FinancialCodeSystemForm(data=invalid_data)

        # Checks that it is not valid
        self.assertFalse(form.is_valid())

        # Check that it is the end date causing the invalid form
        self.assertEqual(
            form["date_start"].errors[0],
            "Enter a valid date."
        )

    def test_valid_data_with_end_date(self):
        """Tests that data validates properly"""
        # Create form
        form = FinancialCodeSystemForm(data=self.valid_data)

        # Check that form is valid
        self.assertTrue(form.is_valid())

    def test_valid_data_without_end_date(self):
        """Tests that data validates properly when no end date provided"""
        # Create data without end date
        modified_data = self.valid_data
        modified_data["date_end"] = None
        
        # Create form
        form = FinancialCodeSystemForm(data=modified_data)

        # Check that form is valid
        self.assertTrue(form.is_valid())

    def test_form_populates_model(self):
        """Tests that the form properly populates a model"""

        # Create form
        form = FinancialCodeSystemForm(data=self.valid_data)

        # Save data
        form.save()

        # Check that values are saved properly
        system = FinancialCodeSystem.objects.last()

        self.assertEqual(self.valid_data["title"], system.title)
        self.assertEqual(self.valid_data["date_start"], str(system.date_start))
        self.assertEqual(self.valid_data["date_end"], str(system.date_end))

#class BudgetYearFormTest(TestCase):
#    """Test functions for the Budget Year form"""

#    def setUp(self):
#        # Add standard test data
#        self.correct_data = {
#            "financial_code_system": 1,
#            "date_start": "2017-01-01",
#            "date_end": "2017-12-31",
#        }

#    def test_missing_start_date_validation(self):
#        """Tests that custom validation handles missing start date"""
#        # Setup invalid data
#        incorrect_data = self.correct_data
#        incorrect_data["date_start"] = "2017"

#         # Create a form instance with invalid data
#        form = BudgetYearForm(data=incorrect_data)

#        # Checks that it is not valid
#        self.assertFalse(form.is_valid())

#        # Check that it is the end date causing the invalid form
#        self.assertEqual(
#            form["date_start"].errors[0],
#            "Enter a valid date."
#        )
        
#    def test_missing_end_date_validation(self):
#        """Tests that custom validation handles missing end date"""
#        # Setup invalid data
#        incorrect_data = self.correct_data
#        incorrect_data["date_end"] = "2017"

#         # Create a form instance with invalid data
#        form = BudgetYearForm(data=incorrect_data)

#        # Checks that it is not valid
#        self.assertFalse(form.is_valid())

#        # Check that it is the end date causing the invalid form
#        self.assertEqual(
#            form["date_end"].errors[0],
#            "Enter a valid date."
#        )
        
#    def test_missing_system_validation(self):
#        """Tests that custom validation handles missing end date"""
#        # Setup invalid data
#        incorrect_data = self.correct_data
#        incorrect_data["financial_code_system"] = "999999999"

#        # Create a form instance with invalid data
#        form = BudgetYearForm(data=incorrect_data)

#        # Checks that it is not valid
#        self.assertFalse(form.is_valid())

#    def test_date_end_before_start_validation(self):
#        """Tests that validation catches end date before start"""
#        # Setup invalid data
#        incorrect_data = self.correct_data
#        incorrect_data["date_end"] = "2016-12-31"

#        # Create a form instance with invalid data
#        form = BudgetYearForm(data=incorrect_data)

#        # Checks that it is not valid
#        self.assertFalse(form.is_valid())

#        # Check that it is the end date causing the invalid form
#        self.assertEqual(
#            form["date_end"].errors[0],
#            "The end date must occur after the start date."
#        )

#    def test_start_date_within_system_date(self):
#        """Tests that start date must occur within financial code system dates"""
#        # Setup invalid data
#        incorrect_data = self.correct_data
#        incorrect_data["date_start"] = "2000-01-01"

#        # Create a form instance with invalid data
#        form = BudgetYearForm(data=incorrect_data)

#        # Checks that it is not valid
#        self.assertFalse(form.is_valid())

#        # Check that it is the end date causing the invalid form
#        self.assertEqual(
#            form["date_start"].errors[0],
#            "The start date must occur after the start of the Financial Code System."
#        )

#    def test_end_date_within_system_date(self):
#        """
#            Tests that end date must occur within financial code
#            system dates (if end date specified)
#        """
#        # Setup invalid data
#        incorrect_data = self.correct_data
#        incorrect_data["financial_code_system"] = 2
#        incorrect_data["date_end"] = "2020-12-31"

#        # Create a form instance with invalid data
#        form = BudgetYearForm(data=incorrect_data)

#        # Checks that it is not valid
#        self.assertFalse(form.is_valid())

#        # Check that it is the end date causing the invalid form
#        self.assertEqual(
#            form["date_end"].errors[0],
#            "The end date must occur before the end of the Financial Code System."
#        )
        
#    def test_end_date_with_no_system_end_date(self):
#        """
#            Tests that any end date is okay if financial code
#            system end date not specified
#        """
#        # Setup correct data
#        correct_data = self.correct_data
#        correct_data["date_end"] = "2020-12-31"

#        # Create a form instance with invalid data
#        form = BudgetYearForm(data=correct_data)

#        # Checks that it is not valid
#        self.assertTrue(form.is_valid())

#class FinancialCodeFormTest(TestCase):
#    """Test functions for the Financial Code form"""

#    def setUp(self):
#        # Add standard test data
#        self.correct_data = {
#            "financial_code_group": 1,
#            "code": "1000",
#            "description": "FK Travel Grant",
#        }

#    def test_custom_budget_year_choices(self):
#        """Tests that custom budget year select is formatted correctly"""
#        # Create a form instance with invalid data
#        form = FinancialCodeForm(data=self.correct_data)
#        choices = form.fields["budget_year"].choices

#        # Check length of the opt choices and opt groups
#        self.assertEqual(len(choices), 2)
#        self.assertEqual(len(choices[0]), 2)
#        self.assertEqual(len(choices[1]), 2)

#        # Check the opt groups
#        self.assertEqual(
#            str(choices[0][0]),
#            "CSHP National (2014-04-01 to Present)"
#        )

#        self.assertEqual(
#            str(choices[1][0]),
#            "CSHP Alberta Branch (2000-01-01 to 2018-03-31)"
#        )

#        # Check the budget year IDs
#        self.assertEqual(
#            choices[0][1][0][0],
#            1
#        )

#        self.assertEqual(
#            choices[1][1][0][0],
#            3
#        )

#        # Check the budget year strings
#        self.assertEqual(
#            str(choices[0][1][0][1]),
#            "2016-04-01 to 2017-03-31"
#        )

#        self.assertEqual(
#            str(choices[1][1][0][1]),
#            "2016-04-01 to 2017-03-31"
#        )
