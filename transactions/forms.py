"""Forms for the financial_codes app"""

from django import forms
from django.forms import inlineformset_factory

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

ItemFormSet = inlineformset_factory(
    Transaction,
    Item,
    form=ItemForm,
    extra=0,
    min_num=1,
    validate_min=True,
    can_delete=True,
)