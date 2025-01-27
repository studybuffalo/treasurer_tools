"""Test cases for the financial codes app widgets"""

from django.test import TestCase

from financial_transactions.forms import FinancialCodeAssignmentForm
from .utils import create_financial_codes

class FinancialCodeWithYearIDTest(TestCase):
    """Test functions for the FinancialCodeWithYearID widget"""

    def setUp(self):
        self.codes = create_financial_codes()

        system_id = self.codes[0].financial_code_group.budget_year.financial_code_system.id

        # Need to retrieve widget from form to get options initialized
        self.form = FinancialCodeAssignmentForm(system=system_id, transaction_type="e")

    def test_option_values(self):
        """Checks that the budget year is appropriately added"""
        # Collect all the choices
        choices = []

        for choice in self.form.fields["code"].choices:
            choices.append(choice)

        # Check that lists are equal
        self.assertCountEqual(
            choices,
            [
                ("", "---------"),
                (
                    self.codes[0].financial_code_group.title,
                    [(self.codes[0].id, str(self.codes[0]))]
                ),
            ]
        )

    def test_budget_year_attribute(self):
        # Create the expect Select HTML
        select_html = (
            '<select name="code" required id="id_code">\n'
            '  <option value="" selected data-year_id="">---------</option>\n\n'
            '  <optgroup label="{}">\n'
            '  <option value="{}" data-year_id="{}">{}</option>\n\n'
            '  </optgroup>\n'
            '</select>'
        ).format(
            self.codes[0].financial_code_group.title,
            self.codes[0].id,
            self.codes[0].financial_code_group.budget_year.id,
            str(self.codes[0])
        ).replace("&", "&amp;")

        # Check that html is correct
        self.assertEqual(
            str(self.form["code"]),
            select_html
        )
