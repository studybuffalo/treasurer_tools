from django import forms
from django.core.exceptions import ValidationError

from .models import Country, Demographics

class PayeePayerForm(forms.ModelForm):
    class Meta:
        model = Demographics

        fields = [
            "name",
            "address",
            "country",
            "province",
            "city",
            "postal_code",
            "phone",
            "fax",
            "email",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super(PayeePayerForm, self).__init__(*args, **kwargs)

        # Sort country select by country name (alphabetical)
        self.fields["country"].queryset = Country.objects.order_by(
            "country_name"
        )