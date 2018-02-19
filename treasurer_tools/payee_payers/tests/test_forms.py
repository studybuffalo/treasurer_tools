"""Test cases for the bank_transactions app forms"""

from django.test import TestCase

from payee_payers.forms import PayeePayerForm
from payee_payers.models import Country, PayeePayer

from .utils import create_country, create_demographics


class PayeePayerFormTest(TestCase):
    """Test functions for the PayeePayer model"""

    def setUp(self):
        country = create_country()
        self.valid_data = {
            "user": None,
            "name": "Another Test User",
            "address": "111-222 Fake Street",
            "city": "Edmonton",
            "province": "Alberta",
            "country": country.id,
            "postal_code": "T1T 1T1",
            "phone": "111-222-3333",
            "fax": "444-555-6666",
            "email": "test@email.com",
            "status": "a"
        }

    def test_country_order(self):
        """Tests for countries in proper sorted order"""
        # Create additional country entries
        Country.objects.create(country_code="US", country_name="United States")
        Country.objects.create(country_code="AU", country_name="Australia")

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

        # Check if the two lists are identical
        correct_order = True

        if len(form_list) == len(db_list):
            # Check if the two lists match in values
            for i, db_value in enumerate(db_list):
                if db_value != form_list[i]:
                    correct_order = False
        else:
            correct_order = False

        self.assertTrue(correct_order)

    def test_is_valid_with_valid_data(self):
        """Tests that a is_valid is true when provided valid data"""
        form = PayeePayerForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_is_valid_with_invalid_data(self):
        """Tests that a is_valid is true when provided valid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["name"] = None

        form = PayeePayerForm(data=invalid_data)

        self.assertFalse(form.is_valid())

    def test_can_add_entry(self):
        """Tests that form properly add new entry"""
        # Count number of investments
        payee_payer_total = PayeePayer.objects.count()

        # Create and save form
        form = PayeePayerForm(self.valid_data)
        self.assertTrue(form.is_valid())
        form.save()

        # Check that number of entries increased
        self.assertEqual(PayeePayer.objects.count(), payee_payer_total + 1)

        # Check that name has saved properly
        self.assertEqual(PayeePayer.objects.last().name, self.valid_data["name"])

    def test_can_update_original_entry(self):
        """Tests that form properly updates an old entry"""
        # Create investment
        payee_payer_instance = create_demographics()

        # Count number of investments
        payee_payer_total = PayeePayer.objects.count()

        # Create and save form
        form = PayeePayerForm(self.valid_data, instance=payee_payer_instance)
        self.assertTrue(form.is_valid())
        form.save()

        # Check that number of entries remains the same
        self.assertEqual(PayeePayer.objects.count(), payee_payer_total)

        # Check that name has updated
        self.assertEqual(PayeePayer.objects.last().name, self.valid_data["name"])
