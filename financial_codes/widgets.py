from django.forms.widgets import Select

from .models import FinancialCodeGroup

class SelectWithYearID(Select):
    """Select widget that allows data-attribute addition to options"""
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        """Modifies function to include the financial code system ID"""
        option = super(SelectWithYearID, self).create_option(name, value, label, selected, index, subindex, attrs)
        
        # Use the option value (i.e. the model ID) to retrieve budget year ID
        if option["value"]:
            year_id = FinancialCodeGroup.objects.get(id=option["value"]).budget_year.id
        else:
            year_id = ""

        # Add the data attribute
        option["attrs"]["data-year_id"] = year_id
        
        # Return the modified option
        return option