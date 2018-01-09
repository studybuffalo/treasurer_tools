"""Forms for the financial_codes app"""

from django import forms
from django.forms import inlineformset_factory

from financial_codes.models import BudgetYear
from financial_codes.widgets import FinancialCodeWithYearID

from .models import Transaction, Item

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
    financial_code_match_id = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput,
    )
    budget_year = forms.ChoiceField(
        choices=[],
        label="Budget year",
        required=False,
    )
    code = forms.ChoiceField(
        choices=[],
        label="Financial code",
        widget=FinancialCodeWithYearID,
    )
    
    def __init__(self, *args, **kwargs):
        # pylint: disable=no-member, invalid-name
        # Get the financial code system
        financial_code_system = kwargs.pop("system")
        transaction_type = "e" if kwargs.pop("transaction_type") == "expense" else "r"

        # Retrieve all the children BudgetYears entries
        budget_years = BudgetYear.objects.filter(
            financial_code_system=financial_code_system
        )

        # Create a choice list with the budget_years
        budget_year_choices = []

        for year in budget_years:
            budget_year_choices.append((year.id, str(year)))
            
        # Create a choice list with the budget_years
        financial_code_choices = [["", "---------"]]

        # Retrieve all the children FinancialCodeGroup entries
        for year in budget_years:
            groups = year.financialcodegroup_set.filter(type=transaction_type)

            for group in groups:
                code_list = []

                codes = group.financialcode_set.all()

                for code in codes:
                    code_list.append((code.id, str(code)))

                financial_code_choices.append([group.title, code_list])
            
        super(FinancialCodeAssignmentForm, self).__init__(*args, **kwargs)
        
        # Set the initial value
        # Specify the choices
        self.fields["budget_year"].choices = budget_year_choices
        self.fields["code"].choices = financial_code_choices

# pylint: disable=invalid-name
ItemFormSet = inlineformset_factory(
    Transaction,
    Item,
    form=ItemForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)
