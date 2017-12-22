from django import forms
from django.core.exceptions import ValidationError

from .models import Demographics

class PayeePayerForm(forms.ModelForm):
    class Meta:
        model = Demographics

        fields = [
            "user",
            "name",
            "address",
            "city",
            "province",
            "country",
            "postal_code",
            "phone",
            "fax",
            "email",
            "status",
        ]