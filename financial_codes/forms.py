"""Forms for the financial_codes app"""

from django import forms
from django.core.exceptions import ValidationError

from .models import (
    BudgetYear, FinancialCodeSystem, FinancialCodeGroup, FinancialCode,
)
from. widgets import SelectWithSystemID

class FinancialCodeSystemForm(forms.ModelForm):
    """Form to add & edit entries in the FinancialCodeSystem model"""
    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = FinancialCodeSystem

        fields = [
            "title",
            "date_start",
            "date_end",
        ]

    def clean_date_end(self):
        """Checks that a valid date is provided"""
        date_start = self.cleaned_data["date_start"]
        date_end = self.cleaned_data["date_end"]

        # Check that the end date is greater than the start date
        if date_end and date_end < date_start:
            raise ValidationError("End date must occur after the start date.")

        return date_end

class FinancialCodeGroupForm(forms.ModelForm):
    """Form to add and edit financial code systems"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = FinancialCodeGroup

        fields = [
            "financial_code_system",
            "title",
            "description",
            "type",
            "status",
        ]

class BudgetYearForm(forms.ModelForm):
    """Form to add and edit budget years"""
    # pylint: disable=missing-docstring,too-few-public-methods

    class Meta:
        model = BudgetYear

        fields = [
            "financial_code_system",
            "date_start",
            "date_end",
        ]

class FinancialCodeForm(forms.ModelForm):
    """Form to add and edit financial codes"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = FinancialCode

        fields = [
            "code",
            "description",
            "code_system",
            "code_group",
            "budget_year",
        ]
        widgets = {
            "code_group": SelectWithSystemID(attrs={"disabled": "disabled"}),
            "budget_year": SelectWithSystemID(attrs={"disabled": "disabled"}),
        }
