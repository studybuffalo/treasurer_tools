"""Test cases for the transactions app forms"""

import tempfile

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import QueryDict
from django.test import TestCase
from django.utils.datastructures import MultiValueDict

from financial_codes.models import BudgetYear, FinancialCode
from financial_transactions.forms import FinancialCodeAssignmentForm, CompiledForms

from .utils import create_financial_codes, create_demographics


class FinancialCodeAssignmentFormTest(TestCase):
    """Test functions for the FinancialCode model"""

    def setUp(self):
        self.codes = create_financial_codes()

    def test_expense_code_select(self):
        """Tests that code select generates properly for expense transactions"""
        # Create the form reference
        transaction_type = self.codes[0].financial_code_group.type
        system_id = self.codes[0].financial_code_group.budget_year.financial_code_system.id
        form = FinancialCodeAssignmentForm(transaction_type=transaction_type, system=system_id)

        # Get the code select
        code_select = form.fields["code"]

        # Confirm proper number of codes were collected (# of codes + 1 placeholder)
        self.assertEqual(len(code_select.choices), 2)

        # Check that the codes are specific to this expense type
        for option_grouping in code_select.choices:
            if option_grouping[0]:
                for code in option_grouping[1]:
                    self.assertEqual(
                        transaction_type,
                        "e"
                    )

    def test_revenue_code_select(self):
        """Tests that code select generates properly for expense transactions"""
        # Create the form reference
        transaction_type = self.codes[1].financial_code_group.type
        system_id = self.codes[1].financial_code_group.budget_year.financial_code_system.id
        form = FinancialCodeAssignmentForm(transaction_type=transaction_type, system=system_id)

        # Get the code select
        code_select = form.fields["code"]

        # Confirm proper number of codes were collected (# of codes + 1 placeholder)
        self.assertEqual(len(code_select.choices), 2)

        # Check that the codes are specific to this expense type
        for option_grouping in code_select.choices:
            if option_grouping[0]:
                for code in option_grouping[1]:
                    self.assertEqual(
                        transaction_type,
                        "r"
                    )

    # TODO: Add tests to confirm the custom budget year choices

class CompiledFormsTest(TestCase):
    """Additional tests for object not covered elsewhere"""

    def setUp(self):
        payee_payer = create_demographics()
        codes = create_financial_codes()

        self.correct_data = {
            "payee_payer": payee_payer.id,
            "memo": "Travel Grant award 2017",
            "date_submitted": "2017-06-01",
            "item_set-0-date_item": "2017-06-01",
            "item_set-0-description": "Taxi costs",
            "item_set-0-amount": "100.0",
            "item_set-0-gst": "5.0",
            "item_set-0-id": "",
            "item_set-0-transaction": "",
            "item_set-0-coding_set-0-financial_code_match_id": "",
            "item_set-0-coding_set-0-budget_year": codes[0].financial_code_group.budget_year.id,
            "item_set-0-coding_set-0-code": codes[0].id,
            "item_set-0-coding_set-1-financial_code_match_id": "",
            "item_set-0-coding_set-1-budget_year": codes[2].financial_code_group.budget_year.id,
            "item_set-0-coding_set-1-code": codes[2].id,
            "item_set-TOTAL_FORMS": "1",
            "item_set-INITIAL_FORMS": "0",
            "item_set-MIN_NUM_FORMS": "1",
            "item_set-MAX_NUM_FORMS": "1000",
            "financialtransactionmatch_set-TOTAL_FORMS": "0",
            "financialtransactionmatch_set-INITIAL_FORMS": "0",
            "financialtransactionmatch_set-MIN_NUM_FORMS": "0",
            "financialtransactionmatch_set-MAX_NUM_FORMS": "20",
        }
        self.codes = codes
        self.payee_payer = payee_payer

    def test_is_valid_is_true(self):
        """Confirms setup data returns true for is_valid"""
        forms = CompiledForms("expense", "POST", self.correct_data)

        self.assertTrue(forms.is_valid())

#    def test_invalid_transaction_payee_payer(self):
#        """Confirms is_valid() returns false with invalid payee-payer"""
#        edited_data = self.correct_data
#        edited_data["payee_payer"] = ""

#        forms = CompiledForms("expense", "POST", edited_data)

#        # Check that CompiledForm is invalid
#        self.assertFalse(forms.is_valid())

#    def test_invalid_transaction_memo(self):
#        """Confirms is_valid() returns false with invalid transaction form"""
#        edited_data = self.correct_data
#        edited_data["memo"] = ""
        
#        forms = CompiledForms("expense", "POST", edited_data)

#        # Check that CompiledForm is invalid
#        self.assertFalse(forms.is_valid())

#    def test_invalid_transaction_date(self):
#        """Confirms is_valid() returns false with invalid transaction form"""
#        edited_data = self.correct_data
#        edited_data["date_submitted"] = ""
        
#        forms = CompiledForms("expense", "POST", edited_data)

#        # Check that CompiledForm is invalid
#        self.assertFalse(forms.is_valid())

#    def test_invalid_item_date(self):
#        """Confirms is_valid() returns false with invalid item date"""
#        edited_data = self.correct_data
#        edited_data["item_set-0-date_item"] = ""
        
#        forms = CompiledForms("expense", "POST", edited_data)

#        # Check that CompiledForm is invalid
#        self.assertFalse(forms.is_valid())

#    def test_invalid_item_description(self):
#        """Confirms is_valid() returns false with invalid item date"""
#        edited_data = self.correct_data
#        edited_data["item_set-0-description"] = ""
        
#        forms = CompiledForms("expense", "POST", edited_data)

#        # Check that CompiledForm is invalid
#        self.assertFalse(forms.is_valid())
        
#    def test_invalid_item_amount(self):
#        """Confirms is_valid() returns false with invalid item date"""
#        edited_data = self.correct_data
#        edited_data["item_set-0-amount"] = ""
        
#        forms = CompiledForms("expense", "POST", edited_data)

#        # Check that CompiledForm is invalid
#        self.assertFalse(forms.is_valid())

#    def test_invalid_item_gst(self):
#        """Confirms is_valid() returns false with invalid item date"""
#        edited_data = self.correct_data
#        edited_data["item_set-0-gst"] = ""
        
#        forms = CompiledForms("expense", "POST", edited_data)

#        # Check that CompiledForm is invalid
#        self.assertFalse(forms.is_valid())

#    def test_invalid_financial_code_code(self):
#        """Confirms is_valid() returns false with invalid code"""
#        edited_data = self.correct_data
#        edited_data["item_set-0-coding_set-0-code"] = ""
        
#        forms = CompiledForms("expense", "POST", edited_data)

#        # Check that CompiledForm is invalid
#        self.assertFalse(forms.is_valid())

#    def test_invalid_attachment_file_size(self):
#        """Confirms is_valid() returns false with file > 10 mb"""
#        # Creates control test for file creation
#        with tempfile.NamedTemporaryFile("w+b", suffix=".txt") as test_file:
#            # Create a 1 mb file
#            test_file.write(b"1" * 1024 * 1024)
#            test_file.seek(0)
            
#            # Creates a proper MultiValueDict to mimic request.FILES
#            files = MultiValueDict({
#                "newattachment-attachment_files": [
#                    InMemoryUploadedFile(test_file, None, "test.txt", "text/plain", 1024 * 1024, None),
#                ]
#            })
            
#            # Creats a QueryDict to mimic request.POST
#            data = QueryDict('', mutable=True)
#            data.update(self.correct_data)

#            # Create the compiled forms
#            forms = CompiledForms(
#                "expense",
#                "POST",
#                data,
#                files
#            )

#            # Check that CompiledForm is valid
#            self.assertTrue(forms.is_valid())

#        # Creates invalid file (10 mb + 1 b) and test validation
#        with tempfile.NamedTemporaryFile("w+b", suffix=".txt") as test_file:
#            # Create file
#            test_file.write(b"1" * ((1024 * 1024 * 10) + 1))
#            test_file.seek(0)

#            # Add the file the data
#            files = MultiValueDict({
#                "newattachment-attachment_files": [
#                    InMemoryUploadedFile(test_file, None, "test.txt", "text/plain", (1024 * 1024 * 10) + 1, None),
#                ]
#            })

#            # Create the compiled forms
#            forms = CompiledForms("expense", "POST", self.correct_data, files)

#            # Check that CompiledForm is invalid
#            self.assertFalse(forms.is_valid())
            
#    def test_invalid_old_attachment(self):
#        """Confirms is_valid() returns false with invalid old attachment"""
#        # Control test
#        edited_data = self.correct_data
#        edited_data["attachmentmatch_set-0-id"] = "1"
#        edited_data["attachmentmatch_set-0-attachment"] = "1"
#        edited_data["attachmentmatch_set-TOTAL_FORMS"] = 1
#        edited_data["attachmentmatch_set-INITIAL_FORMS"] = 1

#        # Create the compiled forms
#        valid_forms = CompiledForms(
#            "expense",
#            "POST",
#            edited_data,
#        )

#        # Check that CompiledForm is valid
#        self.assertTrue(valid_forms.is_valid())
        
#        # Test that invalid attachment returns false
#        edited_data["attachmentmatch_set-0-attachment"] = ""

#        invalid_forms = CompiledForms(
#            "expense",
#            "POST",
#            edited_data,
#        )

#        # Check that CompiledForm is invalid
#        self.assertFalse(invalid_forms.is_valid())

#    def test_corrupt_financial_code_match_when_setting_initial_data(self):
#        """
#            Tests handling when a financial code match is not
#            available for an item ID
#        """
#        form = CompiledForms(
#            "expense"
#            "GET"
#        )

        
#        self.assertIsNone(
#            form._CompiledForms__set_financial_code_data(999999999, 1, "")
#        )
