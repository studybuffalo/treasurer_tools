"""Custom widgets for the Financial Codes app"""
from django.forms.widgets import Select

from .models import FinancialCodeGroup

class FinancialCodeGroupWithYearID(Select):
    """Select widget that allows data-attribute addition to options"""
    # pylint: disable=too-many-arguments
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        """Modifies function to include the budget year ID"""
        option = super(FinancialCodeGroupWithYearID, self).create_option(
            name, value, label, selected, index, subindex, attrs
        )

        # Use the option value (i.e. the model ID) to retrieve budget year ID
        if option["value"]:
            # Coerce value into a string to allow lookup to pass
            option_id = str(option["value"])
            year_id = FinancialCodeGroup.objects.get(id=option_id).budget_year.id
        else:
            year_id = ""

        # Add the data attribute
        option["attrs"]["data-year_id"] = year_id

        # Return the modified option
        return option
