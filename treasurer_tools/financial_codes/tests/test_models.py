"""Test cases for the financial codes app models"""

from django.test import TestCase

from financial_codes.models import (
    FinancialCodeSystem, FinancialCodeGroup, BudgetYear, FinancialCode
)

class FinancialCodeSystemModelTest(TestCase):
    """Test functions for the Financial Code System model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/financial_code_system.json",
    ]

    def test_labels(self):
        """tests a series of fields for proper label generation"""
        test_list = [
            {"field_name": "title", "label_name": "title"},
            {"field_name": "date_start", "label_name": "start date"},
            {"field_name": "date_end", "label_name": "end date"},
        ]

        for test_item in test_list:
            financial_code_system = FinancialCodeSystem.objects.get(id=1)
            field_label = financial_code_system._meta.get_field(test_item["field_name"]).verbose_name
            self.assertEqual(field_label, test_item["label_name"])

    def test_title_max_length(self):
        """Tests a series of fields for proper max length"""
        financial_code_system = FinancialCodeSystem.objects.get(id=1)
        max_length = financial_code_system._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        # Test entry without end date
        self.assertEqual(
            str(FinancialCodeSystem.objects.get(id=1)),
            "CSHP National (2014-04-01 to Present)"
        )

        # Test entry with end date
        self.assertEqual(
            str(FinancialCodeSystem.objects.get(id=2)),
            "CSHP Alberta Branch (2000-01-01 to 2018-03-31)"
        )

class BudgetYearModelTest(TestCase):
    """Test functions for the BudgetYear model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/financial_code_system.json",
        "financial_codes/tests/fixtures/budget_year.json",
    ]
    
    def test_financial_code_system_label(self):
        """Tests for a proper date_start label"""
        budget_year = BudgetYear.objects.get(id=1)
        field_label = budget_year._meta.get_field("financial_code_system").verbose_name

        self.assertEqual(field_label, "financial code system")
        
    def test_date_start_label(self):
        """Tests for a proper date_start label"""
        budget_year = BudgetYear.objects.get(id=1)
        field_label = budget_year._meta.get_field("date_start").verbose_name

        self.assertEqual(field_label, "start date")
        
    def test_date_end_label(self):
        """Tests for a proper date_end label"""
        budget_year = BudgetYear.objects.get(id=1)
        field_label = budget_year._meta.get_field("date_end").verbose_name

        self.assertEqual(field_label, "end date")

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        budget_year = BudgetYear.objects.get(id=1)
        
        self.assertEqual(
            str(budget_year),
            "{} to {}".format(budget_year.date_start, budget_year.date_end)
        )
        
class FinancialCodeGroupModelTest(TestCase):
    """Test functions for the FinancialCodeGroup"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/financial_code_system.json",
        "financial_codes/tests/fixtures/budget_year.json",
        "financial_codes/tests/fixtures/financial_code_group.json",
    ]

    def test_labels(self):
        """tests a series of fields for proper label generation"""
        test_list = [
            {"field_name": "budget_year", "label_name": "budget year"},
            {"field_name": "title", "label_name": "title"},
            {"field_name": "description", "label_name": "description"},
            {"field_name": "type", "label_name": "type"},
            {"field_name": "status", "label_name": "status"},
        ]

        for test_item in test_list:
            financial_code_group = FinancialCodeGroup.objects.get(id=1)
            field_label = financial_code_group._meta.get_field(test_item["field_name"]).verbose_name
            self.assertEqual(field_label, test_item["label_name"])

    def test_title_max_length(self):
        """Tests the title field for proper max length"""
        financial_code_group = FinancialCodeGroup.objects.get(id=1)
        max_length = financial_code_group._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)
        
    def test_description_max_length(self):
        """Tests a the description field for proper max length"""
        financial_code_group = FinancialCodeGroup.objects.get(id=1)
        max_length = financial_code_group._meta.get_field("description").max_length
        self.assertEqual(max_length, 500)

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        financial_code_group = FinancialCodeGroup.objects.all()

        for group in financial_code_group:
            if group.type == "e":
                test_string = "Expense - {}".format(group.title)
            elif group.type == "r":
                test_string = "Revenue - {}".format(group.title)

            self.assertEqual(str(group), test_string)

class FinancialCodeModelTest(TestCase):
    """Test functions for the FinancialCode model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/financial_code_system.json",
        "financial_codes/tests/fixtures/financial_code_group.json",
        "financial_codes/tests/fixtures/budget_year.json",
        "financial_codes/tests/fixtures/financial_code.json",
    ]
    
    def test_labels(self):
        """tests a series of fields for proper label generation"""
        test_list = [
            {"field_name": "financial_code_group", "label_name": "financial code group"},
            {"field_name": "code", "label_name": "code"},
            {"field_name": "description", "label_name": "description"},
        ]

        for test_item in test_list:
            financial_code = FinancialCode.objects.get(id=1)
            field_label = financial_code._meta.get_field(test_item["field_name"]).verbose_name

            self.assertEqual(field_label, test_item["label_name"])
            
    def test_code_max_length(self):
        """Tests the code field for a proper max length"""
        financial_code = FinancialCode.objects.get(id=1)
        max_length = financial_code._meta.get_field("code").max_length

        self.assertEqual(max_length, 6)

    def test_description_max_length(self):
        """Tests the description field for a proper max length"""
        financial_code = FinancialCode.objects.get(id=1)
        max_length = financial_code._meta.get_field("description").max_length

        self.assertEqual(max_length, 100)
        
    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        financial_code = FinancialCode.objects.get(id=1)
        
        self.assertEqual(
            str(financial_code),
            "{} - {}".format(financial_code.code, financial_code.description)
        )