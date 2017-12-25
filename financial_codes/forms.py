"""Forms for the financial_codes app"""

from django import forms

from .models import (
    BudgetYear, FinancialCodeSystem, FinancialCodeGroup, FinancialCode,
)


class FinancialCodeSystemForm(forms.ModelForm):
    """Code to add and edit financial code systems"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = FinancialCodeSystem

        fields = [
            "title",
            "status",
        ]
