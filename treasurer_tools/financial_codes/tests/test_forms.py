"""Test cases for the financial codes app forms"""

from django.test import TestCase

from financial_codes.forms import (
    FinancialCodeSystemForm, BudgetYearForm, FinancialCodeGroupForm, FinancialCodeForm
)
from financial_codes.models import (
    FinancialCodeSystem, BudgetYear, FinancialCodeGroup, FinancialCode
)

from .utils import (
    create_financial_code_systems, create_budget_year, create_financial_code_groups
)

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

class BudgetYearFormTest(TestCase):
    """Test functions for the Budget Year form"""

    def setUp(self):
        systems = create_financial_code_systems()

        self.valid_data = {
            "financial_code_system": systems[0].id,
            "date_start": "2017-01-01",
            "date_end": "2017-12-31",
        }
        self.systems = systems

    def test_missing_start_date_validation(self):
        """Tests that custom validation handles missing start date"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["date_start"] = "2017"

         # Create a form instance with invalid data
        form = BudgetYearForm(data=invalid_data)

        # Checks that it is not valid
        self.assertFalse(form.is_valid())

        # Check that it is the end date causing the invalid form
        self.assertEqual(
            form["date_start"].errors[0],
            "Enter a valid date."
        )

    def test_missing_end_date_validation(self):
        """Tests that custom validation handles missing end date"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["date_end"] = "2017"

         # Create a form instance with invalid data
        form = BudgetYearForm(data=invalid_data)

        # Checks that it is not valid
        self.assertFalse(form.is_valid())

        # Check that it is the end date causing the invalid form
        self.assertEqual(
            form["date_end"].errors[0],
            "Enter a valid date."
        )
        
    def test_missing_system_validation(self):
        """Tests that custom validation handles missing end date"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["financial_code_system"] = "999999999"

        # Create a form instance with invalid data
        form = BudgetYearForm(data=invalid_data)

        # Checks that it is not valid
        self.assertFalse(form.is_valid())

    def test_date_end_before_start_validation(self):
        """Tests that validation catches end date before start"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["date_end"] = "2016-12-31"

        # Create a form instance with invalid data
        form = BudgetYearForm(data=invalid_data)

        # Checks that it is not valid
        self.assertFalse(form.is_valid())

        # Check that it is the end date causing the invalid form
        self.assertEqual(
            form["date_end"].errors[0],
            "The end date must occur after the start date."
        )

    def test_start_date_within_system_date(self):
        """Tests that start date must occur within financial code system dates"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["date_start"] = "2000-01-01"

        # Create a form instance with invalid data
        form = BudgetYearForm(data=invalid_data)

        # Checks that it is not valid
        self.assertFalse(form.is_valid())

        # Check that it is the end date causing the invalid form
        self.assertEqual(
            form["date_start"].errors[0],
            "The start date must occur after the start of the Financial Code System."
        )

    def test_end_date_within_system_date(self):
        """
            Tests that end date must occur within financial code
            system dates (if end date specified)
        """
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["financial_code_system"] = self.systems[1].id
        invalid_data["date_end"] = "2020-12-31"

        # Create a form instance with invalid data
        form = BudgetYearForm(data=invalid_data)

        # Checks that it is not valid
        self.assertFalse(form.is_valid())

        # Check that it is the end date causing the invalid form
        self.assertEqual(
            form["date_end"].errors[0],
            "The end date must occur before the end of the Financial Code System."
        )
        
    def test_end_date_with_no_system_end_date(self):
        """
            Tests that any end date is okay if financial code
            system end date not specified
        """
        # Setup correct data
        valid_data = self.valid_data
        valid_data["date_end"] = "2020-12-31"

        # Create a form instance with invalid data
        form = BudgetYearForm(data=valid_data)

        # Checks that it is not valid
        self.assertTrue(form.is_valid())

    def test_form_populates_model(self):
        """Tests that the form properly populates a model"""
        # Create form
        form = BudgetYearForm(data=self.valid_data)

        # Save data
        form.save()

        # Check that values are saved properly
        year = BudgetYear.objects.last()

        self.assertEqual(self.valid_data["financial_code_system"], year.financial_code_system.id)
        self.assertEqual(self.valid_data["date_start"], str(year.date_start))
        self.assertEqual(self.valid_data["date_end"], str(year.date_end))

class FinancialCodeGroupFromTest(TestCase):
    """Tests for the FinancialCodeGroup form"""

    def setUp(self):
        year = create_budget_year()

        self.valid_data = {
            "budget_year": year.id,
            "title": "Awards & Grants",
            "description": "Expenses for awards & grants",
            "type": "e",
            "status": "a"
        }

    def test_form_populates_model(self):
        """Tests that the form properly populates a model"""
        # Create form
        form = FinancialCodeGroupForm(data=self.valid_data)

        # Save data
        form.save()

        # Check that values are saved properly
        group = FinancialCodeGroup.objects.last()

        self.assertEqual(self.valid_data["budget_year"], group.budget_year.id)
        self.assertEqual(self.valid_data["title"], str(group.title))
        self.assertEqual(self.valid_data["description"], str(group.description))
        self.assertEqual(self.valid_data["type"], str(group.type))
        self.assertEqual(self.valid_data["status"], str(group.status))

class FinancialCodeFormTest(TestCase):
    """Test functions for the Financial Code form"""

    def setUp(self):
        groups = create_financial_code_groups()

        self.valid_data = {
            "financial_code_group": groups[0].id,
            "code": "1000",
            "description": "FK Travel Grant",
        }
        self.groups = groups

    def test_custom_budget_year_choices(self):
        """Tests that custom budget year select is formatted correctly"""
        # Create a form instance with valid data
        form = FinancialCodeForm(data=self.valid_data)
        choices = form.fields["budget_year"].choices

        # Check length of the opt choices and opt groups
        self.assertEqual(len(choices), 2)
        self.assertEqual(len(choices[0]), 2)
        self.assertEqual(len(choices[1]), 2)

        # Check the opt groups
        self.assertEqual(
            str(choices[0][0]),
            "National (2010-01-01 to Present)"
        )

        self.assertEqual(
            str(choices[1][0]),
            "Regional (2000-01-01 to 2015-12-31)"
        )

        # Check the budget year ID
        self.assertEqual(
            choices[0][1][0][0],
            self.groups[0].budget_year.id
        )

        # Check the budget year string
        self.assertEqual(
            str(choices[0][1][0][1]),
            "2017-01-01 to 2017-12-31"
        )

    def test_form_populates_model(self):
        """Tests that the form properly populates a model"""
        # Create form
        form = FinancialCodeForm(data=self.valid_data)

        # Save data
        form.save()

        # Check that values are saved properly
        code = FinancialCode.objects.last()

        self.assertEqual(self.valid_data["financial_code_group"], code.financial_code_group.id)
        self.assertEqual(self.valid_data["code"], code.code)
        self.assertEqual(self.valid_data["description"], code.description)
