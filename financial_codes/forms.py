from django import forms
from django.core.exceptions import ValidationError

from .models import (
    BudgetYear, FinancialCodeSystem, FinancialCodeGroup, FinancialCode,
)


class FinancialCodeSystemForm(forms.ModelForm):
    class Meta:
        model = FinancialCodeSystem

        fields = [
            "title",
            "status",
        ]