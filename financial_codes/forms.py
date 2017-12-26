"""Forms for the financial_codes app"""

from django import forms

from .models import (
    BudgetYear, FinancialCodeSystem, FinancialCodeGroup, FinancialCode,
)


class FinancialCodeSystemForm(forms.ModelForm):
    """Form to add and edit financial code systems"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = FinancialCodeSystem

        fields = [
            "title",
            "status",
        ]

class FinancialCodeGroupForm(forms.ModelForm):
    """Form to add and edit financial code systems"""
    
    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = FinancialCodeGroup

        fields = [
            "title",
            "description",
            "status",
        ]

class BudgetYearForm(forms.ModelForm):
    """Form to add and edit budget years"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = BudgetYear

        fields = [
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
