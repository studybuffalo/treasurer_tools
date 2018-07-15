"""Forms for the financial_codes app"""

from django import forms

from .models import Investment, InvestmentDetail


class InvestmentForm(forms.ModelForm):
    """Form to add and edit investments"""

    class Meta:
        model = Investment

        fields = ("name", "rate",)

class InvestmentDetailForm(forms.ModelForm):
    """Form to add details to an investment"""

    class Meta:
        model = InvestmentDetail

        fields = ("investment", "date_investment", "detail_status", "amount",)
