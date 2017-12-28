"""Forms for the financial_codes app"""

from django import forms
from django.forms import Textarea

from .models import Statement, Institution


class StatementForm(forms.ModelForm):
    """Form to add and edit transactions"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = Statement

        fields = ("account", "date_start", "date_end")
        labels = {
            "date_start": "Start date",
            "date_end": "End date",
        }

class InstitutionForm(forms.ModelForm):
    """Form to add and edit transactions"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = Institution

        fields = ("name", "address", "phone", "fax")
        labels = {
            "date_start": "Start date",
            "date_end": "End date",
        }
        widgets = {
            "address": Textarea(),
        }
