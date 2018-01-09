"""Test cases for the transactions app forms"""

from django.test import TestCase

from financial_codes.models import BudgetYear, FinancialCode
from transactions.forms import FinancialCodeAssignmentForm


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
            self.assertEquals(
                BudgetYear.objects.get(id=budget_year[0]).financial_code_system.id,
                1
            )

    def test_expense_code_select(self):
        """Tests that code select generates properly for expense transactions"""
        form = FinancialCodeAssignmentForm(transaction_type="expense", system="1")
        code_select = form.fields["code"]
        
        # Confirm proper number of codes were collected (2 + 1 placeholder)
        self.assertEqual(3, len(code_select.choices))

        # Check that the codes are specific to this expense type
        for option_grouping in code_select.choices:
            if option_grouping[0]:
                for code in option_grouping[1]:
                    self.assertEquals(
                        FinancialCode.objects.get(id=code[0]).financial_code_group.type,
                        "e"
                    )

    def test_revenue_code_select(self):
        """Tests that code select generates properly for expense transactions"""
        form = FinancialCodeAssignmentForm(transaction_type="revenue", system="1")
        code_select = form.fields["code"]
        
        # Confirm proper number of codes were collected (2 + 1 placeholder)
        self.assertEqual(3, len(code_select.choices))

        # Check that the codes are specific to this expense type
        for option_grouping in code_select.choices:
            if option_grouping[0]:
                for code in option_grouping[1]:
                    self.assertEquals(
                        FinancialCode.objects.get(id=code[0]).financial_code_group.type,
                        "r"
                    )