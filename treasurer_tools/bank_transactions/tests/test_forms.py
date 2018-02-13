"""Test cases for the bank_transaction app forms"""

from django.test import TestCase

from bank_transactions.forms import StatementForm, BankTransactionFormSet, NewBankAttachmentForm

from .utils import create_bank_account, create_bank_statement

class StatementFormTest(TestCase):
    """test functions for the statement form"""

    def setUp(self):
        account = create_bank_account()
        self.valid_data = {
            "account": account.id,
            "date_start": "2017-01-01",
            "date_end": "2017-01-31",
        }

    def test_custom_date_validation(self):
        """tests that start date must be before end date"""
        # Generate invalid data
        invalid_data = self.valid_data
        invalid_data["date_start"] = "2018-01-01"

        # Generate the form
        statement_form = StatementForm(invalid_data)

        # check that the form is invalid
        self.assertFalse(statement_form.is_valid())

        # check for proper error message
        self.assertEqual(
            statement_form["date_end"].errors[0],
            "The end date must occur after the start date."
        )

    def test_custom_date_validation_handles_invalid_dates(self):
        """tests that the custom validation can handle invalid dates"""
        # Generate invalid data
        invalid_data = self.valid_data
        invalid_data["date_end"] = "a"

        # Generate the form
        statement_form = StatementForm(invalid_data)
        
        # Check that the form is invalid
        self.assertFalse(statement_form.is_valid())

        # Check for proper error messages
        self.assertEqual(
            statement_form["date_end"].errors[0],
            "Enter a valid date."
        )

    def test_is_valid_with_valid_data(self):
        """Tests that is_valid is true when provided with valid data"""

        # Generate the form
        statement_form = StatementForm(self.valid_data)

        # Check that the form is valid
        self.assertTrue(statement_form.is_valid())

class BankTransactionFormSetTest(TestCase):
    """Test functions for the Bank Transaction FormSet"""

    def setUp(self):
        self.valid_data = {
            "banktransaction_set-0-date_transaction": "2017-01-02",
            "banktransaction_set-0-description_bank": "CHQ 001",
            "banktransaction_set-0-description_user": "Cheque #0001",
            "banktransaction_set-0-amount_debit": "100.00",
            "banktransaction_set-0-amount_credit": "0",
            "banktransaction_set-TOTAL_FORMS": 1,
            "banktransaction_set-INITIAL_FORMS": 0,
            "banktransaction_set-MIN_NUM_FORMS": 1,
            "banktransaction_set-MAX_NUM_FORMS": 1000,
        }
        self.statement = create_bank_statement()

    def test_is_valid_with_valid_data(self):
        """Tests that a is_valid is true when provided valid data"""
        form = BankTransactionFormSet(self.valid_data, instance=self.statement)

        self.assertTrue(form.is_valid())

    def test_custom_amount_validation(self):
        """Tests that only debit OR credit has a proper value"""
        # Generate invalid data
        invalid_data = self.valid_data
        invalid_data["banktransaction_set-0-amount_credit"] = "200.00"

        # Generate the form
        bank_transaction_formset = BankTransactionFormSet(invalid_data, instance=self.statement)

        # Check that the form is invalid
        self.assertFalse(bank_transaction_formset.is_valid())

        # Check for proper error message
        self.assertEqual(
            bank_transaction_formset[0]["amount_credit"].errors[0],
            "A single transaction cannot have both debit and credit amounts entered."
        )

    def test_custom_amount_validation_handles_no_value(self):
        """Tests that only debit OR credit has a proper value"""
        # Generate invalid data
        invalid_data = self.valid_data
        invalid_data["banktransaction_set-0-amount_debit"] = "0"

        # Generate the form
        bank_transaction_formset = BankTransactionFormSet(invalid_data)

        # Check that the form is invalid
        self.assertFalse(bank_transaction_formset.is_valid())

        # Check for proper error message
        self.assertEqual(
            bank_transaction_formset[0]["amount_debit"].errors[0],
            "Please enter a debit or credit value."
        )

    def test_custom_amount_validation_handles_invalid_value(self):
        """Tests that custom validation handles invalid debit/credit values"""
        # Generate invalid data
        invalid_data = self.valid_data
        invalid_data["banktransaction_set-0-amount_debit"] = "a"
        invalid_data["banktransaction_set-0-amount_credit"] = "a"
        
        # Generate the form
        bank_transaction_formset = BankTransactionFormSet(invalid_data)

        # Check that the form is invalid
        self.assertFalse(bank_transaction_formset.is_valid())

        # Check for proper error messages
        self.assertEqual(
            bank_transaction_formset[0]["amount_debit"].errors[0],
            "Enter a number."
        )
        self.assertEqual(
            bank_transaction_formset[0]["amount_credit"].errors[0],
            "Enter a number."
        )
