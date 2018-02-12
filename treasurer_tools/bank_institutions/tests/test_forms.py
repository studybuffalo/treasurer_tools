"""Test cases for the bank_institution app forms"""

from django.test import TestCase

from bank_institutions.forms import InstitutionForm, AccountFormSet
from bank_institutions.models import Institution, Account

from .utils import create_bank_institution


class InstitutionFormTest(TestCase):
    """Tests for the Institution Form"""

    def setUp(self):
        self.valid_data = {
            "name": "Another Financial Institution",
            "address": "444 Test Boulevard\nRich City $$ T1T 1T1",
            "phone": "111-222-1234",
            "fax": "222-111-1111",
        }

    def test_is_valid_with_valid_data(self):
        """Tests that a is_valid is true when provided valid data"""
        form = InstitutionForm(data=self.valid_data)

        self.assertTrue(form.is_valid())

    def test_is_valid_with_invalid_data(self):
        """Tests that a is_valid is true when provided valid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["name"] = None

        form = InstitutionForm(data=invalid_data)

        self.assertFalse(form.is_valid())

class AccountFormsetTest(TestCase):
    """Tests for the account formset"""

    def setUp(self):
        self.valid_data = {
            "account_set-0-account_number": "777888999",
            "account_set-0-name": "Savings Account",
            "account_set-0-status": "a",
            "account_set-TOTAL_FORMS": 1,
            "account_set-INITIAL_FORMS": 0,
            "account_set-MIN_NUM_FORMS": 1,
            "account_set-MAX_NUM_FORMS": 1000,
        }
        self.institution = create_bank_institution()

    def test_is_valid_with_valid_data(self):
        """Tests that a is_valid is true when provided valid data"""
        form = AccountFormSet(self.valid_data, instance=self.institution)

        self.assertTrue(form.is_valid())

    def test_is_valid_with_invalid_data(self):
        """Tests that a is_valid is true when provided valid data"""
        # Create invalid data
        invalid_data = self.valid_data
        invalid_data["account_set-0-name"] = None

        form = AccountFormSet(invalid_data, instance=self.institution)

        self.assertFalse(form.is_valid())

    def test_is_valid_with_nodata(self):
        """Tests that at least one form must be submitted"""
        form = AccountFormSet(
            {
                "account_set-TOTAL_FORMS": 0,
                "account_set-INITIAL_FORMS": 0,
                "account_set-MIN_NUM_FORMS": 1,
                "account_set-MAX_NUM_FORMS": 1000
            },
            instance=self.institution
        )

        self.assertFalse(form.is_valid())

    def test_account_is_added_on_save(self):
        """Tests that a new account entry is added when form is saved"""
        account_total = Account.objects.count()

        form = AccountFormSet(self.valid_data, instance=self.institution)
        form.save()

        self.assertEqual(
            Account.objects.count(),
            account_total + 1
        )
