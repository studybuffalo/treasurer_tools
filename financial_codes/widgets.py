from django.forms.widgets import Select

from .models import FinancialCodeGroup, BudgetYear

class SelectWithSystemID(Select):
    """Select widget that allows data-attribute addition to options"""
    
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        """Modifies function to include the financial code system ID"""
        option = super(SelectWithSystemID, self).create_option(name, value, label, selected, index, subindex, attrs)
        
        # Use the option value (i.e. the model ID) to retrieve the system ID
        if option["value"]:
            if option["name"] == "code_group":
                system_id = FinancialCodeGroup.objects.get(id=option["value"]).financial_code_system.id
            elif option["name"] == "budget_year":
                system_id = BudgetYear.objects.get(id=option["value"]).financial_code_system.id
        else:
            system_id = ""

        # Add the data attribute
        option["attrs"]["data-system_id"] = system_id
        
        # Return the modified option
        return option