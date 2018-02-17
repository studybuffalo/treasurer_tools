"""Widgets for the financial_transactions app"""

from django.forms.widgets import Select

from financial_codes.models import FinancialCode


class FinancialCodeWithYearID(Select):
    """Select widget that allows data-attribute addition to options"""
    # pylint: disable=too-many-arguments, no-member
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        """Modifies function to include the financial code system ID"""
        option = super(FinancialCodeWithYearID, self).create_option(
            name, value, label, selected, index, subindex, attrs
        )

        # Use the option value (i.e. the model ID) to retrieve budget year ID
        if option["value"]:
            year_id = FinancialCode.objects.get(id=option["value"]).financial_code_group.budget_year.id
        else:
            year_id = ""

        # Add the data attribute
        option["attrs"]["data-year_id"] = year_id

        # Return the modified option
        return option
