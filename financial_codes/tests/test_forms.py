"""Test cases for the bank_transactions app forms"""

from django.test import TestCase

from payee_payer.forms import PayeePayerForm
from payee_payer.models import Country

class CountryModelTest(TestCase):
    """Test functions for the Demographics model"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "payee_payer/tests/fixtures/country.json",
    ]

    def test_country_order(self):
        """Tests for countries in proper sorted order"""
        correct_order = True

        # Create a list of the database values
        db_list = sorted(
            Country.objects.all().values_list("country_name", flat=True)
        )

        # Create a list of the form choices
        form = PayeePayerForm()

        form_list = []

        for choice in form.fields["country"].choices:
            form_list.append(choice[1])

        # Remove the first entry (the "-----" entry)
        form_list = form_list[1:]

        # Check if the two lists match in length
        if len(form_list) == len(db_list):
            # Check if the two lists match in values
            for i, db_value in enumerate(db_list):
                if db_value != form_list[i]:
                    correct_order = False
        else:
            correct_order = False

        self.assertTrue(correct_order)
