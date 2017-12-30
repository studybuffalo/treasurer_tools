"""Test cases for the bank_transaction app"""

from django.test import TestCase

from financial_codes.models import (
    FinancialCodeSystem, FinancialCodeGroup, BudgetYear, FinancialCode
)

class FinancialCodeSystemModelTest(TestCase):
    """Test functions for the Financial Code System model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/financial_code_system.json",
    ]

    def test_labels(self):
        """tests a series of fields for proper label generation"""
        test_list = [
            {"field_name": "title", "label_name": "title"},
            {"field_name": "status", "label_name": "status"},
        ]

        for test_item in test_list:
            financial_code_system = FinancialCodeSystem.objects.get(id=1)
            field_label = financial_code_system._meta.get_field(test_item["field_name"]).verbose_name
            self.assertEqual(field_label, test_item["label_name"])

    def test_title_max_length(self):
        """Tests a series of fields for proper max length"""
        financial_code_system = FinancialCodeSystem.objects.get(id=1)
        max_length = financial_code_system._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        financial_code_system = FinancialCodeSystem.objects.get(id=1)
        self.assertEqual(str(financial_code_system), financial_code_system.title)

class FinancialCodeGroupModelTest(TestCase):
    """Test functions for the Account model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/financial_code_system.json",
        "financial_codes/tests/fixtures/financial_code_group.json",
    ]

    def test_labels(self):
        """tests a series of fields for proper label generation"""
        test_list = [
            {"field_name": "title", "label_name": "title"},
            {"field_name": "description", "label_name": "description"},
            {"field_name": "type", "label_name": "type"},
            {"field_name": "status", "label_name": "status"},
        ]

        for test_item in test_list:
            financial_code_group = FinancialCodeGroup.objects.get(id=1)
            field_label = financial_code_group._meta.get_field(test_item["field_name"]).verbose_name
            self.assertEqual(field_label, test_item["label_name"])

    def test_title_max_length(self):
        """Tests a series of fields for proper max length"""
        financial_code_group = FinancialCodeGroup.objects.get(id=1)
        max_length = financial_code_group._meta.get_field("title").max_length
        self.assertEqual(max_length, 100)
        
    def test_description_max_length(self):
        """Tests a series of fields for proper max length"""
        financial_code_group = FinancialCodeGroup.objects.get(id=1)
        max_length = financial_code_group._meta.get_field("description").max_length
        self.assertEqual(max_length, 500)

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        financial_code_group = FinancialCodeGroup.objects.all()

        for group in financial_code_group:
            if group.type == "e":
                test_string = "Expense - {}".format(group.title)
            elif group.type == "r":
                test_string = "Revenue - {}".format(group.title)

            self.assertEqual(str(group), test_string)

#class BudgetYearModelTest(TestCase):
#    """Test functions for the Statement model"""
#    # pylint: disable=no-member,protected-access
    
#    fixtures = [
#        "bank_transactions/tests/fixtures/institution.json",
#        "bank_transactions/tests/fixtures/account.json",
#        "bank_transactions/tests/fixtures/statement.json",
#    ]

#    def test_labels(self):
#        """Tests a series of fields for proper label generation"""
#        test_list = [
#            {"field_name": "account", "label_name": "account"},
#            {"field_name": "date_start", "label_name": "start date"},
#            {"field_name": "date_end", "label_name": "end date"},
#        ]

#        for test_item in test_list:
#            statement = Statement.objects.get(id=1)
#            field_label = statement._meta.get_field(test_item["field_name"]).verbose_name
#            self.assertEqual(field_label, test_item["label_name"])

#    def test_string_representation(self):
#        """Tests that the model string representaton returns as expected"""
#        statement = Statement.objects.get(id=1)
#        self.assertEqual(
#            str(statement),
#            "{} to {} statement".format(statement.date_start, statement.date_end)
#        )

#class FinancialCodeModelTest(TestCase):
#    """Test functions for the BankTransaction model"""
#    # pylint: disable=no-member,protected-access
    
#    fixtures = [
#        "bank_transactions/tests/fixtures/institution.json",
#        "bank_transactions/tests/fixtures/account.json",
#        "bank_transactions/tests/fixtures/statement.json",
#        "bank_transactions/tests/fixtures/bank_transaction.json",
#    ]

#    def test_labels(self):
#        """Tests a series of fields for proper label generation"""
#        test_list = [
#            {"field_name": "statement", "label_name": "statement"},
#            {"field_name": "date_transaction", "label_name": "transaction date"},
#            {"field_name": "description_bank", "label_name": "bank description"},
#            {"field_name": "description_user", "label_name": "user description"},
#            {"field_name": "amount_debit", "label_name": "debit amount"},
#            {"field_name": "amount_credit", "label_name": "credit amount"},
#        ]

#        for test_item in test_list:
#            bank_transaction = BankTransaction.objects.get(id=1)
#            field_label = bank_transaction._meta.get_field(test_item["field_name"]).verbose_name
#            self.assertEqual(field_label, test_item["label_name"])
            
#    def test_max_length(self):
#        """Tests a series of fields for proper max length"""
#        test_list = [
#            {"field_name": "description_bank", "max_length": 100},
#            {"field_name": "description_user", "max_length": 100},
#        ]

#        for test_item in test_list:
#            bank_transaction = BankTransaction.objects.get(id=1)
#            max_length = bank_transaction._meta.get_field(test_item["field_name"]).max_length
#            self.assertEqual(max_length, test_item["max_length"])
            
#    def test_max_digits(self):
#        """Tests a series of fields for proper max digits"""
#        test_list = [
#            {"field_name": "amount_debit", "max_digits": 12},
#            {"field_name": "amount_credit", "max_digits": 12},
#        ]

#        for test_item in test_list:
#            bank_transaction = BankTransaction.objects.get(id=1)
#            max_digits = bank_transaction._meta.get_field(test_item["field_name"]).max_digits
#            self.assertEqual(max_digits, test_item["max_digits"])

#    def test_string_representation(self):
#        """Tests that the model string representaton returns as expected"""
#        bank_transactions = BankTransaction.objects.all()
        
#        for bank_transaction in bank_transactions:
#            if bank_transaction.description_user:
#                test_string = "{} - {}".format(
#                    bank_transaction.date_transaction,
#                    bank_transaction.description_user
#                )
#            else:
#                test_string = "{} - {}".format(
#                    bank_transaction.date_transaction,
#                    bank_transaction.description_bank
#                )

#            self.assertEqual(str(bank_transaction), test_string)
