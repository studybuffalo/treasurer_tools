"""Test cases for the bank_transaction app forms"""

from django.test import TestCase

from bank_transactions.forms import StatementForm, BankTransactionForm

class StatementFormTest(TestCase):
    """Test functions for the Statement Form"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
    ]

    def test_custom_date_validation(self):
        """Tests that start date must be before end date"""
        # Generate the form
        statement_form = StatementForm({
            "account": 1,
            "date_start": "2018-01-01",
            "date_end": "2017-01-01"
        })

        # Check that the form is invalid
        self.assertFalse(statement_form.is_valid())

        # Check for proper error message
        self.assertEqual(
            statement_form["date_end"].errors[0],
            "The end date must occur after the start date."
        )

    def test_custom_date_validation_handles_invalid_dates(self):
        """Tests that the custom validation can handle invalid dates"""
        # Generate the form
        statement_form = StatementForm({
            "account": 1,
            "date_start": "1",
            "date_end": "2"
        })

        # Check that the form is invalid
        self.assertFalse(statement_form.is_valid())

        # Check for proper error messages
        self.assertEqual(
            statement_form["date_end"].errors[0],
            "Enter a valid date."
        )

class BankTransactionFormTest(TestCase):
    """Test functions for the Bank Transaction Form"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
    ]

    def test_custom_amount_validation(self):
        """Tests that only debit OR credit has a proper value"""
        # Generate the form
        bank_transaction_form = BankTransactionForm({
            "date_transaction": "2018-01-01",
            "description_bank": "CHQ",
            "description_user": "Cheque",
            "amount_debit": 1.00,
            "amount_credit": 1.00
        })

        # Check that the form is invalid
        self.assertFalse(bank_transaction_form.is_valid())

        # Check for proper error message
        self.assertEqual(
            bank_transaction_form["amount_credit"].errors[0],
            "A single transaction cannot have both debit and credit amounts entered."
        )

    def test_custom_amount_validation_handles_no_value(self):
        """Tests that only debit OR credit has a proper value"""
        # Generate the form
        bank_transaction_form = BankTransactionForm({
            "date_transaction": "2018-01-01",
            "description_bank": "CHQ",
            "description_user": "Cheque",
            "amount_debit": 0,
            "amount_credit": 0
        })

        # Check that the form is invalid
        self.assertFalse(bank_transaction_form.is_valid())

        # Check for proper error message
        self.assertEqual(
            bank_transaction_form["amount_debit"].errors[0],
            "Please enter a debit or credit value."
        )

    def test_custom_amount_validation_handles_invalid_value(self):
        """Tests that custom validation handles invalid debit/credit values"""
        # Generate the form
        bank_transaction_form = BankTransactionForm({
            "date_transaction": "2018-01-01",
            "description_bank": "CHQ",
            "description_user": "Cheque",
            "amount_debit": "a",
            "amount_credit": "a"
        })

        # Check that the form is invalid
        self.assertFalse(bank_transaction_form.is_valid())

        # Check for proper error messages
        self.assertEqual(
            bank_transaction_form["amount_debit"].errors[0],
            "Enter a number."
        )
        self.assertEqual(
            bank_transaction_form["amount_credit"].errors[0],
            "Enter a number."
        )