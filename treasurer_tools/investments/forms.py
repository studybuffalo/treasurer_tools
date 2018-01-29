"""Forms for the financial_codes app"""

from django import forms

from .models import Investment


class InvestmentForm(forms.ModelForm):
    """Form to add and edit investments"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = Investment

        fields = ("name", "date_invested", "amount", "rate")
