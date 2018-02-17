"""Test cases for the financial codes app widgets"""

from django.test import TestCase

from financial_codes.forms import FinancialCodeForm
from .utils import create_financial_code_groups

class FinancialCodeGroupWithYearIDTest(TestCase):
    """Test functions for the FinancialCodeGroupWithYearID widget"""

    def setUp(self):
        self.groups = create_financial_code_groups()

        # Need to retrieve widget from form to get options initialized
        self.form = FinancialCodeForm()

    def test_option_values(self):
        """Checks that the budget year is appropriately added"""
        # Collect all the choices
        choices = []

        for choice in self.form.fields["financial_code_group"].choices:
            choices.append(choice)

        # Check that lists are equal
        self.assertCountEqual(
            choices,
            [
                ("", "---------"),
                (self.groups[0].id, str(self.groups[0])),
                (self.groups[1].id, str(self.groups[1]))
            ]
        )
    def test_budget_year_attribute(self):
        # Create the expect Select HTML
        select_html = (
            '<select name="financial_code_group" required id="id_financial_code_group">\n'
            '  <option value="" selected data-year_id="">---------</option>\n\n'
            '  <option value="{}" data-year_id="{}">{}</option>\n\n'
            '  <option value="{}" data-year_id="{}">{}</option>\n\n'
            '</select>'
        ).format(
            self.groups[0].id, self.groups[0].budget_year.id, str(self.groups[0]),
            self.groups[1].id, self.groups[1].budget_year.id, str(self.groups[1])
        ).replace("&", "&amp;")

        # Check that html is correct
        self.assertEqual(
            str(self.form["financial_code_group"]),
            select_html
        )
