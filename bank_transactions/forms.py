"""Forms for the financial_codes app"""

from django import forms

from .models import Statement


class StatementForm(forms.ModelForm):
    """Form to add and edit transactions"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = Statement

        fields = ()
