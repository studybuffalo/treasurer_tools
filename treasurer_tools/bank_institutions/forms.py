"""Forms for the financial_codes app"""

from django import forms
from django.forms import Textarea

from .models import Institution


class InstitutionForm(forms.ModelForm):
    """Form to add and edit transactions"""

    class Meta:
        model = Institution

        fields = ("name", "address", "phone", "fax")
        widgets = {
            "address": Textarea(),
        }
