"""Test cases for the bank_transaction app"""

from django.test import TestCase

from bank_transactions.models import Institution

class InstitutionModelTest(TestCase):
    """Test functions for the Demographics model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/account.json",
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/bank_transaction.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/statement.json",
    ]

    def test_labels(self):
        """Tests a series of fields for proper label generation"""
        test_list = [
            {"field_name": "name", "label_name": "name"},
            {"field_name": "address", "label_name": "address"},
            {"field_name": "phone", "label_name": "phone number"},
            {"field_name": "fax", "label_name": "fax number"},
        ]

        for test_item in test_list:
            institution = Institution.objects.get(id=1)
            field_label = institution._meta.get_field(test_item["field_name"]).verbose_name
            self.assertEqual(field_label, test_item["label_name"])
