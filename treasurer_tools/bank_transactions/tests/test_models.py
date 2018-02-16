"""Test cases for the bank_transaction app"""

from django.test import TestCase

from .utils import create_bank_statement, create_bank_transactions

class StatementModelTest(TestCase):
    """Test functions for the Statement model"""

    def setUp(self):
        self.statement = create_bank_statement()

    def test_labels(self):
        """Tests a series of fields for proper label generation"""

        # Get statement reference
        statement = self.statement

        # Test account label
        self.assertEqual(
            statement._meta.get_field("account").verbose_name,
            "account"
        )

        # Test date_start label
        self.assertEqual(
            statement._meta.get_field("date_start").verbose_name,
            "start date"
        )

        # Test date_end label
        self.assertEqual(
            statement._meta.get_field("date_end").verbose_name,
            "end date"
        )

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        self.assertEqual(
            str(self.statement),
            "2017-01-01 to 2017-01-31 statement"
        )

class BankTransactionModelTest(TestCase):
    """Test functions for the BankTransaction model"""

    def setUp(self):
        self.transactions = create_bank_transactions()

    def test_labels(self):
        """Tests a series of fields for proper label generation"""

        transaction = self.transactions[0]

        # Test statement label
        self.assertEqual(
            transaction._meta.get_field("statement").verbose_name,
            "bank statement"
        )

        # Test date_transaction label
        self.assertEqual(
            transaction._meta.get_field("date_transaction").verbose_name,
            "transaction date"
        )

        # Test description_bank label
        self.assertEqual(
            transaction._meta.get_field("description_bank").verbose_name,
            "bank description"
        )

        # Test description_user label
        self.assertEqual(
            transaction._meta.get_field("description_user").verbose_name,
            "custom description"
        )

        # Test amount_debit label
        self.assertEqual(
            transaction._meta.get_field("amount_debit").verbose_name,
            "debit amount"
        )

        # Test amount_credit label
        self.assertEqual(
            transaction._meta.get_field("amount_credit").verbose_name,
            "credit amount"
        )

    def test_max_length(self):
        """Tests a series of fields for proper max length"""

        transaction = self.transactions[0]

        # Test description_bank max length
        self.assertEqual(
            transaction._meta.get_field("description_bank").max_length,
            100
        )

        # Test description_user max length
        self.assertEqual(
            transaction._meta.get_field("description_user").max_length,
            100
        )

    def test_max_digits(self):
        """Tests a series of fields for proper max digits"""

        transaction = self.transactions[0]

        # Test amount_debit max digits
        self.assertEqual(
            transaction._meta.get_field("amount_debit").max_digits,
            12
        )

        # Test amount_credit max digits
        self.assertEqual(
            transaction._meta.get_field("amount_credit").max_digits,
            12
        )

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""

        # Test string without description_user
        self.assertEqual(
            str(self.transactions[2]),
            "2017-01-03 - DEP3333"
        )

        # Test string with description_user
        self.assertEqual(
            str(self.transactions[0]),
            "2017-01-01 - Cheque #0001"
        )
