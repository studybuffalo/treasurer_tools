"""Forms for the financial_codes app"""

from django import forms
from django.forms import Textarea, inlineformset_factory

from .models import Institution, Account


class InstitutionForm(forms.ModelForm):
    """Form to add and edit transactions"""

    class Meta:
        model = Institution

        fields = ("name", "address", "phone", "fax")
        widgets = {
            "address": Textarea(),
        }

# Setup the inline formset for the Item model
AccountFormSet = inlineformset_factory(
    Institution,
    Account,
    fields=("account_number", "name", "status",),
    min_num=1,
    validate_min=True,
    extra=0,
    can_delete=False,
)