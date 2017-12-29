"""Test cases for the bank_transaction app"""

from django.test import TestCase

from bank_transactions.models import BankTransaction, Account, Institution, Statement

class InstitutionModelTest(TestCase):
    """Test functions for the Institution model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/institution.json",
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

    def test_max_length(self):
        """Tests a series of fields for proper max length"""
        test_list = [
            {"field_name": "name", "max_length": 250},
            {"field_name": "address", "max_length": 1000},
            {"field_name": "phone", "max_length": 30},
            {"field_name": "fax", "max_length": 30},
        ]

        for test_item in test_list:
            institution = Institution.objects.get(id=1)
            max_length = institution._meta.get_field(test_item["field_name"]).max_length
            self.assertEqual(max_length, test_item["max_length"])

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        institution = Institution.objects.get(id=1)
        self.assertEqual(str(institution), institution.name)

class AccountModelTest(TestCase):
    """Test functions for the Account model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
    ]

    def test_labels(self):
        """Tests a series of fields for proper label generation"""
        test_list = [
            {"field_name": "institution", "label_name": "institution"},
            {"field_name": "account_number", "label_name": "account number"},
            {"field_name": "name", "label_name": "name"},
            {"field_name": "status", "label_name": "status"},
        ]

        for test_item in test_list:
            account = Account.objects.get(id=1)
            field_label = account._meta.get_field(test_item["field_name"]).verbose_name
            self.assertEqual(field_label, test_item["label_name"])

    def test_max_length(self):
        """Tests a series of fields for proper max length"""
        test_list = [
            {"field_name": "account_number", "max_length": 100},
            {"field_name": "name", "max_length": 100},
            {"field_name": "status", "max_length": 1},
        ]

        for test_item in test_list:
            account = Account.objects.get(id=1)
            max_length = account._meta.get_field(test_item["field_name"]).max_length
            self.assertEqual(max_length, test_item["max_length"])

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        account = Account.objects.get(id=1)
        self.assertEqual(
            str(account),
            "{} {} ({})".format(
                account.institution, account.account_number, account.account_number
            )
        )
        
class StatementModelTest(TestCase):
    """Test functions for the Statement model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
        "bank_transactions/tests/fixtures/statement.json",
    ]

    def test_labels(self):
        """Tests a series of fields for proper label generation"""
        test_list = [
            {"field_name": "account", "label_name": "account"},
            {"field_name": "date_start", "label_name": "start date"},
            {"field_name": "date_end", "label_name": "end date"},
        ]

        for test_item in test_list:
            statement = Statement.objects.get(id=1)
            field_label = statement._meta.get_field(test_item["field_name"]).verbose_name
            self.assertEqual(field_label, test_item["label_name"])

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        statement = Statement.objects.get(id=1)
        self.assertEqual(
            str(statement),
            "{} to {} statement".format(statement.date_start, statement.date_end)
        )
