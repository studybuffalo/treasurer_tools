"""Forms for the financial_codes app"""

from django import forms

from .models import Transaction, Item


class TransactionForm(forms.ModelForm):
    """Form to add and edit transactions"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = Transaction

        fields = (
            "payee_payer",
            "memo",
            "date_submitted",
        )