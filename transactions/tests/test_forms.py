"""Test cases for the transactions app forms"""

from django.test import TestCase

from financial_codes.models import BudgetYear, FinancialCode
from transactions.forms import FinancialCodeAssignmentForm, CompiledForms


class FinancialCodeAssignmentFormTest(TestCase):
    """Test functions for the Demographics model"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "transactions/tests/fixtures/financial_code_system.json",
        "transactions/tests/fixtures/budget_year.json",
        "transactions/tests/fixtures/financial_code_group.json",
        "transactions/tests/fixtures/financial_code.json",
    ]

    def test_budget_year_select(self):
        """Tests that budget year select generates properly"""
        form = FinancialCodeAssignmentForm(transaction_type="expense", system="1")
        budget_select = form.fields["budget_year"]

        # Confirm proper number of budget years were collected
        self.assertEqual(2, len(budget_select.choices))

        # Check that these budget years belong to this financial code system
        for budget_year in budget_select.choices:
            self.assertEqual(
                BudgetYear.objects.get(id=budget_year[0]).financial_code_system.id,
                1
            )

    def test_expense_code_select(self):
        """Tests that code select generates properly for expense transactions"""
        form = FinancialCodeAssignmentForm(transaction_type="e", system="1")
        code_select = form.fields["code"]
        
        # Confirm proper number of codes were collected (2 + 1 placeholder)
        self.assertEqual(3, len(code_select.choices))

        # Check that the codes are specific to this expense type
        for option_grouping in code_select.choices:
            if option_grouping[0]:
                for code in option_grouping[1]:
                    self.assertEqual(
                        FinancialCode.objects.get(id=code[0]).financial_code_group.type,
                        "e"
                    )

    def test_revenue_code_select(self):
        """Tests that code select generates properly for expense transactions"""
        form = FinancialCodeAssignmentForm(transaction_type="r", system="1")
        code_select = form.fields["code"]
        
        # Confirm proper number of codes were collected (2 + 1 placeholder)
        self.assertEqual(3, len(code_select.choices))

        # Check that the codes are specific to this expense type
        for option_grouping in code_select.choices:
            if option_grouping[0]:
                for code in option_grouping[1]:
                    self.assertEqual(
                        FinancialCode.objects.get(id=code[0]).financial_code_group.type,
                        "r"
                    )

class CompiledFormsTest(TestCase):
    """Additional tests for object not covered elsewhere"""

    fixtures = [
        "transactions/tests/fixtures/authentication.json",
        "transactions/tests/fixtures/country.json",
        "transactions/tests/fixtures/demographics.json",
        "transactions/tests/fixtures/financial_code_system.json",
        "transactions/tests/fixtures/budget_year.json",
        "transactions/tests/fixtures/financial_code_group.json",
        "transactions/tests/fixtures/financial_code.json",
    ]

    def setUp(self):
        self.correct_data = {
            "payee_payer": 1,
            "memo": "Travel Grant award 2017",
            "date_submitted": "2017-06-01",
            "item_set-0-date_item": "2017-06-01",
            "item_set-0-description": "Taxi costs",
            "item_set-0-amount": 100.00,
            "item_set-0-gst": 5.00,
            "item_set-0-id": "",
            "item_set-0-transaction": "",
            "item_set-0-coding_set-0-financial_code_match_id": "",
            "item_set-0-coding_set-0-budget_year": 1,
            "item_set-0-coding_set-0-code": 1,
            "item_set-0-coding_set-1-financial_code_match_id": "",
            "item_set-0-coding_set-1-budget_year": 3,
            "item_set-0-coding_set-1-code": 5,
            "item_set-TOTAL_FORMS": 1,
            "item_set-INITIAL_FORMS": 0,
            "item_set-MIN_NUM_FORMS": 1,
            "item_set-MAX_NUM_FORMS": 1000,
            "attachmentmatch_set-TOTAL_FORMS": 0,
            "attachmentmatch_set-INITIAL_FORMS": 0,
            "attachmentmatch_set-MIN_NUM_FORMS": 0,
            "attachmentmatch_set-MAX_NUM_FORMS": 20,
        }

    def test_is_valid_is_true(self):
        """Confirms setup data returns true for is_valid"""
        forms = CompiledForms("expense", "POST", self.correct_data)

        self.assertTrue(forms.is_valid())

    def test_invalid_transaction_memo(self):
        """Confirms is_valid() returns false with invalid transaction form"""
        edited_data = self.correct_data
        edited_data["memo"] = ""
        
        forms = CompiledForms("expense", "POST", edited_data)

        # Check that CompiledForm is invalid
        self.assertFalse(forms.is_valid())

    def test_invalid_transaction_date(self):
        """Confirms is_valid() returns false with invalid transaction form"""
        edited_data = self.correct_data
        edited_data["date_submitted"] = ""
        
        forms = CompiledForms("expense", "POST", edited_data)

        # Check that CompiledForm is invalid
        self.assertFalse(forms.is_valid())