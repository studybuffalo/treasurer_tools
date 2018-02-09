"""Forms for the payee_payer app"""

from django import forms

from .models import Country, PayeePayer

class PayeePayerForm(forms.ModelForm):
    """Form for adding/editing payee/payer data"""

    # pylint: disable=missing-docstring,too-few-public-methods
    class Meta:
        model = PayeePayer

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

        # pylint: disable=no-member
        # Sort country select by country name (alphabetical)
        self.fields["country"].queryset = Country.objects.order_by(
            "country_name"
        )
