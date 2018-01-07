"""Forms for the financial_codes app"""

from django import forms
from django.forms import inlineformset_factory

from .models import Transaction, Item
from financial_codes.models import BudgetYear, FinancialCodeGroup, FinancialCode

class TransactionForm(forms.ModelForm):
    """Form to add and edit transactions"""
    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = Transaction

        fields = [
            "payee_payer",
            "memo",
            "date_submitted",
        ]

class ItemForm(forms.ModelForm):
    """Form to add and edit Items"""
    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = Item
        fields = [
            "date_item",
            "description",
            "amount",
            "gst",
        ]

class FinancialCodeAssignmentForm(forms.Form):
    """Form to assign a financial code"""
    budget_year = forms.ChoiceField(
        choices=[],
        label="budget year",
        required=False,
    )
    code = forms.ChoiceField(
        choices=[],
        label="code",
        required=False,
    )
    
    def __init__(self, *args, **kwargs):
        # Get the financial code system
        financial_code_system = kwargs.pop("system")
        initial_values = kwargs.pop("initial", {})

        # Retrieve all the children BudgetYears entries
        budget_years = BudgetYear.objects.filter(
            financial_code_system=financial_code_system
        )

        # Create a choice list with the budget_years
        budget_year_choices = []

        for year in budget_years:
            budget_year_choices.append((year.id, str(year)))
            
        # Create a choice list with the budget_years
        code_choices = []

        # Retrieve all the children FinancialCodeGroup entries
        for year in budget_years:
            groups = year.financialcodegroup_set.all()

            for group in groups:
                codes = group.financialcode_set.all()

                for code in codes:
                    code_choices.append((code.id, str(code)))
            
        super(FinancialCodeAssignmentForm, self).__init__(*args, **kwargs)
        
        # Specify the choices
        self.fields["budget_year"].choices = budget_year_choices
        self.fields["code"].choices = code_choices
        
        # Update with the provided initial values (if provided)
        #if initial_values:
        #    self.fields["budget_year"].initial = initial_values["budget_year"]
        #    self.fields["code"].initial = initial_values["code"]

ItemFormSet = inlineformset_factory(
    Transaction,
    Item,
    form=ItemForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)