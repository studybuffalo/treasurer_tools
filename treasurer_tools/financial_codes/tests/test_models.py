"""Test cases for the financial codes app models"""

from django.test import TestCase

from financial_codes.models import (
    FinancialCodeSystem, BudgetYear, FinancialCodeGroup, FinancialCode
)

from .utils import (
    create_financial_code_systems, create_budget_year, create_financial_code_groups,
    create_financial_codes
)

class FinancialCodeSystemModelTest(TestCase):
    """Test functions for the Financial Code System model"""

    def setUp(self):
        self.systems = create_financial_code_systems()

    def test_financial_code_system_labels(self):
        """tests a series of fields for proper label generation"""

        # Test the title label
        self.assertEqual(
            self.systems[0]._meta.get_field("title").verbose_name,
            "title"
        )

        # Test the date_start label
        self.assertEqual(
            self.systems[0]._meta.get_field("date_start").verbose_name,
            "start date"
        )

        # Test the date_end label
        self.assertEqual(
            self.systems[0]._meta.get_field("date_end").verbose_name,
            "end date"
        )

    def test_title_max_length(self):
        """Tests a series of fields for proper max length"""

        self.assertEqual(self.systems[0]._meta.get_field("title").max_length, 100)

    def test_string_representation_without_end_date(self):
        """Tests that the model string representaton returns as expected"""
        # Test entry without end date
        self.assertEqual(
            str(self.systems[0]),
            "National (2010-01-01 to Present)"
        )

    def test_string_representation_with_end_date(self):
        # Test entry with end date
        self.assertEqual(
            str(self.systems[1]),
            "Regional (2000-01-01 to 2015-12-31)"
        )

class BudgetYearModelTest(TestCase):
    """Test functions for the BudgetYear model"""

    def setUp(self):
        self.budget_year = create_budget_year()

    def test_financial_code_system_label(self):
        """Tests for a proper date_start label"""

        self.assertEqual(
            self.budget_year._meta.get_field("financial_code_system").verbose_name,
            "financial code system"
        )

    def test_date_start_label(self):
        """Tests for a proper date_start label"""

        self.assertEqual(
            self.budget_year._meta.get_field("date_start").verbose_name,
            "start date"
        )

    def test_date_end_label(self):
        """Tests for a proper date_end label"""
        
        self.assertEqual(
            self.budget_year._meta.get_field("date_end").verbose_name,
            "end date"
        )

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""

        self.assertEqual(str(self.budget_year), "2017-01-01 to 2017-12-31")

class FinancialCodeGroupModelTest(TestCase):
    """Test functions for the FinancialCodeGroup"""

    def setUp(self):
        self.groups = create_financial_code_groups()

    def test_labels(self):
        """tests a series of fields for proper label generation"""

        # Test the budget_year label
        self.assertEqual(
            self.groups[0]._meta.get_field("budget_year").verbose_name,
            "budget year"
        )

        # Test the title label
        self.assertEqual(
            self.groups[0]._meta.get_field("title").verbose_name,
            "title"
        )

        # Test the description label
        self.assertEqual(
            self.groups[0]._meta.get_field("description").verbose_name,
            "description"
        )

        # Test the budget_year label
        self.assertEqual(
            self.groups[0]._meta.get_field("type").verbose_name,
            "type"
        )

        # Test the budget_year label
        self.assertEqual(
            self.groups[0]._meta.get_field("status").verbose_name,
            "status"
        )

    def test_title_max_length(self):
        """Tests the title field for proper max length"""

        self.assertEqual(
            self.groups[0]._meta.get_field("title").max_length,
            100
        )

    def test_description_max_length(self):
        """Tests a the description field for proper max length"""

        self.assertEqual(
            self.groups[0]._meta.get_field("description").max_length,
            500
        )

    def test_string_representation_expense(self):
        """Tests that the model string representaton returns as expected"""

        self.assertEqual(str(self.groups[0]), "Expense - Awards & Grants")

    def test_string_representation_revenue(self):
        """Tests that the model string representaton returns as expected"""

        self.assertEqual(str(self.groups[1]), "Revenue - Awards & Grants")


class FinancialCodeModelTest(TestCase):
    """Test functions for the FinancialCode model"""

    def setUp(self):
        self.codes = create_financial_codes()

    def test_labels(self):
        """tests a series of fields for proper label generation"""

        # Test the financial_code_group label
        self.assertEqual(
            self.codes[0]._meta.get_field("financial_code_group").verbose_name,
            "financial code group"
        )

        # Test the code label
        self.assertEqual(
            self.codes[0]._meta.get_field("code").verbose_name,
            "code"
        )

        # Test the description label
        self.assertEqual(
            self.codes[0]._meta.get_field("description").verbose_name,
            "description"
        )

    def test_code_max_length(self):
        """Tests the code field for a proper max length"""

        self.assertEqual(self.codes[0]._meta.get_field("code").max_length, 6)

    def test_description_max_length(self):
        """Tests the description field for a proper max length"""

        self.assertEqual(self.codes[0]._meta.get_field("description").max_length, 100)

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""

        self.assertEqual(str(self.codes[0]), "1000 - Travel Grant")
