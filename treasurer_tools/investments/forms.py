"""Forms for the financial_codes app"""

from django import forms

from .models import Investment


class InvestmentForm(forms.ModelForm):
    """Form to add and edit investments"""

    class Meta:
        model = Investment

        fields = ("name", "date_invested", "amount_invested", "date_matured", "amount_matured", "rate")
