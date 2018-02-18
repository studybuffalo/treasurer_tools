"""Test cases for the transactions app forms"""

import tempfile

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import QueryDict
from django.test import TestCase, override_settings
from django.utils.datastructures import MultiValueDict

from documents.models import Attachment, FinancialTransactionMatch
from financial_codes.models import BudgetYear, FinancialCode
from financial_transactions.forms import FinancialCodeAssignmentForm, CompiledForms
from financial_transactions.models import FinancialTransaction, Item, FinancialCodeMatch
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
    # Setup a temporary media_root folder to hold any attachments
    MEDIA_ROOT = tempfile.mkdtemp()

    def setUp(self):
        payee_payer = create_demographics()
        codes = create_financial_codes()

        self.valid_data = {
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
        forms = CompiledForms("expense", "POST", self.valid_data)

        self.assertTrue(forms.is_valid())

    def test_save_of_new_valid_data(self):
        """Confirms data is added to database on successful form submission"""
        # Get current counts on models
        transaction_total = FinancialTransaction.objects.count()
        item_total = Item.objects.count()
        code_match_total = FinancialCodeMatch.objects.count()

        forms = CompiledForms("expense", "POST", self.valid_data)

        # Check that forms are valid
        self.assertTrue(forms.is_valid())

        # Save forms
        forms.save()

        # Check counts of database entries
        self.assertEqual(FinancialTransaction.objects.count(), transaction_total + 1)

        # Check that one item was added
        self.assertEqual(Item.objects.count(), item_total + 1)

        # Check that financial code matches were added
        self.assertEqual(FinancialCodeMatch.objects.count(), code_match_total + 2)

    def test_save_of_edited_valid_data(self):
        """Tests ability to save valid edited data"""
        # Create the initial entries
        forms = CompiledForms("expense", "POST", self.valid_data)

        # Save entries
        self.assertTrue(forms.is_valid())
        forms.save()

        # Get current entry counts
        transaction_total = FinancialTransaction.objects.count()
        item_total = Item.objects.count()
        code_total = FinancialCodeMatch.objects.count()

        # Get the newly saved values
        transaction = FinancialTransaction.objects.last()
        item = transaction.item_set.all()[0]
        code_matches = item.financialcodematch_set.all()

        # Create the edited data
        edited_data = self.valid_data
        edited_data["item_set-0-id"] = item.id
        edited_data["item_set-0-transaction"] = transaction.id
        edited_data["item_set-0-coding_set-0-financial_code_match_id"] = code_matches[0].id
        edited_data["item_set-0-coding_set-1-financial_code_match_id"] = code_matches[1].id
        edited_data["item_set-INITIAL_FORMS"] = "1"
        edited_data["memo"] = "Travel Grant award 2018"
        edited_data["item_set-0-description"] = "Food costs"

        new_forms = CompiledForms("expense", "POST", edited_data, transaction_id=transaction.id)

        # Save new data
        self.assertTrue(new_forms.is_valid())
        new_forms.save()

        # Check that no new entries were created
        self.assertEqual(FinancialTransaction.objects.count(), transaction_total)
        self.assertEqual(Item.objects.count(), item_total)
        self.assertEqual(FinancialCodeMatch.objects.count(), code_total)

        # Check that values saved
        new_transaction = FinancialTransaction.objects.last()
        self.assertEqual(new_transaction.memo, "Travel Grant award 2018")

        new_item = new_transaction.item_set.all()[0]
        self.assertEqual(new_item.description, "Food costs")

    def test_retrieval_of_saved_data(self):
        """Tests that compiled form retrieves saved data properly"""
        # Create the initial entries
        forms = CompiledForms("expense", "POST", self.valid_data)

        # Save entries
        self.assertTrue(forms.is_valid())
        forms.save()

        # Get the saved transaction
        transaction = FinancialTransaction.objects.last()

        # Retrieve the saved values in the form
        retrieval_form = CompiledForms("expense", "GET", None, None, transaction_id=transaction.id)

        # Check that transaction values are accessible
        self.assertEqual(
            retrieval_form.forms.transaction_form["memo"].value(),
            "Travel Grant award 2017"
        )

        # Check that item values are accessible
        self.assertEqual(
            retrieval_form.forms.item_formset[0]["description"].value(),
            "Taxi costs"
        )

        # Collect all the financial code IDs from the form and models
        form_ids = []

        for form in retrieval_form.forms.item_formsets[0].financial_code_forms:
            form_ids.append(form.form["code"].value())

        model_ids = []

        for instance in transaction.item_set.all()[0].financialcodematch_set.all():
            model_ids.append(instance.financial_code.id)

        # Check that the listed codes match
        self.assertCountEqual(form_ids, model_ids)

    def test_proper_item_deletion_on_save(self):
        """Tests that an item can be deleted via .save()"""
        # First save two items
        valid_data = self.valid_data
        valid_data["item_set-1-date_item"] = "2017-06-02"
        valid_data["item_set-1-description"] = "Meal"
        valid_data["item_set-1-amount"] = "20.0"
        valid_data["item_set-1-gst"] = "2.0"
        valid_data["item_set-1-id"] = ""
        valid_data["item_set-1-transaction"] = ""
        valid_data["item_set-1-coding_set-0-financial_code_match_id"] = ""
        valid_data["item_set-1-coding_set-0-budget_year"] = self.codes[0].financial_code_group.budget_year.id
        valid_data["item_set-1-coding_set-0-code"] = self.codes[0].id
        valid_data["item_set-1-coding_set-1-financial_code_match_id"] = ""
        valid_data["item_set-1-coding_set-1-budget_year"] = self.codes[2].financial_code_group.budget_year.id
        valid_data["item_set-1-coding_set-1-code"] = self.codes[2].id
        valid_data["item_set-TOTAL_FORMS"] = "2"

        # Save the items
        forms = CompiledForms("expense", "POST", valid_data)
        self.assertTrue(forms.is_valid())
        forms.save()

        # Get the current item count
        item_total = Item.objects.count()

        # Retrieve the newly saved items to re-populate form
        transaction = FinancialTransaction.objects.last()
        items = transaction.item_set.all().order_by("id")
        code_matches = items[0].financialcodematch_set.all().order_by("id")

        # Update the data
        delete_data = valid_data
        delete_data["item_set-0-id"] = items[0].id
        delete_data["item_set-0-transaction"] = transaction.id
        delete_data["item_set-1-id"] = items[1].id
        delete_data["item_set-1-transaction"] = transaction.id
        delete_data["item_set-1-DELETE"] = "on"
        delete_data["item_set-0-coding_set-0-financial_code_match_id"] = code_matches[0].id
        delete_data["item_set-0-coding_set-1-financial_code_match_id"] = code_matches[1].id
        delete_data["item_set-1-coding_set-0-financial_code_match_id"] = code_matches[0].id
        delete_data["item_set-1-coding_set-1-financial_code_match_id"] = code_matches[1].id
        delete_data["item_set-INITIAL_FORMS"] = 2

        # Delete the item
        delete_forms = CompiledForms("expense", "POST", delete_data, transaction_id=transaction.id)
        self.assertTrue(delete_forms.is_valid())
        delete_forms.save()

        # Check that items have descreased
        self.assertEqual(Item.objects.count(), item_total - 1)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_valid_attachment_file(self):
        """Confirms is_valid() returns false with file > 10 mb"""
        # Count current number of attachments
        attachment_total = Attachment.objects.count()
        match_total = FinancialTransactionMatch.objects.count()

        with tempfile.NamedTemporaryFile("w+b", suffix=".txt") as test_file:
            # Create a 1 mb file
            test_file.write(b"1" * 1024 * 1024)
            test_file.seek(0)
            
            # Creates a proper MultiValueDict to mimic request.FILES
            files = MultiValueDict({
                "newattachment-attachment_files": [
                    InMemoryUploadedFile(test_file, None, "test.txt", "text/plain", 1024 * 1024, None),
                ]
            })
            
            # Creats a QueryDict to mimic request.POST
            data = QueryDict('', mutable=True)
            data.update(self.valid_data)

            # Create the compiled forms
            forms = CompiledForms("expense", "POST", data, files)

            # Check that CompiledForm is valid
            self.assertTrue(forms.is_valid())

            # Save the data
            forms.save()

        # Check that total increased properly
        self.assertEqual(Attachment.objects.count(), attachment_total + 1)
        self.assertEqual(FinancialTransactionMatch.objects.count(), match_total + 1)

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_valid_old_attachment(self):
        """Confirms forms validate properly with an old attachment"""
        # Create and save a temporary file
        with tempfile.NamedTemporaryFile("w+b", suffix=".txt") as test_file:
            # Create a 1 mb file
            test_file.write(b"1" * 1024 * 1024)
            test_file.seek(0)
            
            # Creates a proper MultiValueDict to mimic request.FILES
            files = MultiValueDict({
                "newattachment-attachment_files": [
                    InMemoryUploadedFile(test_file, None, "test.txt", "text/plain", 1024 * 1024, None),
                ]
            })
            
            # Creats a QueryDict to mimic request.POST
            data = QueryDict('', mutable=True)
            data.update(self.valid_data)

            # Create the compiled forms
            forms = CompiledForms("expense", "POST", data, files)

            # Check that CompiledForm is valid
            self.assertTrue(forms.is_valid())

            # Save the data
            forms.save()

        # Count current number of attachments
        attachment_total = Attachment.objects.count()
        match_total = FinancialTransactionMatch.objects.count()

        # Get the newly saved data
        transaction = FinancialTransaction.objects.last()
        item = Item.objects.last()
        code_matches = item.financialcodematch_set.all()
        attachment_match = FinancialTransactionMatch.objects.last()

        # Create test data with the new attachment
        edited_data = self.valid_data
        edited_data["item_set-0-id"] = item.id
        edited_data["item_set-0-transaction"] = transaction.id
        edited_data["item_set-0-coding_set-0-financial_code_match_id"] = code_matches[0].id
        edited_data["item_set-0-coding_set-1-financial_code_match_id"] = code_matches[1].id
        edited_data["financialtransactionmatch_set-0-id"] = 1
        edited_data["financialtransactionmatch_set-0-attachment"] = 1
        edited_data["financialtransactionmatch_set-TOTAL_FORMS"] = 1
        edited_data["financialtransactionmatch_set-INITIAL_FORMS"] = 1
        edited_data["financialtransactionmatch_set-0-attachment"] = attachment_match.attachment.id
        edited_data["financialtransactionmatch_set-0-id"] = attachment_match.id
        edited_data["financialtransactionmatch_set-0-transaction"] = attachment_match.transaction.id

        # Create the compiled forms
        valid_forms = CompiledForms("expense", "POST", edited_data, None, transaction_id=transaction.id)

        # Check that CompiledForm is valid
        self.assertTrue(valid_forms.is_valid())

        # Save the form
        valid_forms.save()

        # Check that no new entries saved
        self.assertEqual(Attachment.objects.count(), attachment_total)
        self.assertEqual(FinancialTransactionMatch.objects.count(), match_total)

    def test_invalid_transaction_payee_payer(self):
        """Confirms is_valid() returns false with invalid payee-payer"""
        edited_data = self.valid_data
        edited_data["payee_payer"] = ""

        forms = CompiledForms("expense", "POST", edited_data)

        # Check that CompiledForm is invalid
        self.assertFalse(forms.is_valid())

    def test_invalid_transaction_memo(self):
        """Confirms is_valid() returns false with invalid transaction form"""
        edited_data = self.valid_data
        edited_data["memo"] = ""
        
        forms = CompiledForms("expense", "POST", edited_data)

        # Check that CompiledForm is invalid
        self.assertFalse(forms.is_valid())

    def test_invalid_transaction_date(self):
        """Confirms is_valid() returns false with invalid transaction form"""
        edited_data = self.valid_data
        edited_data["date_submitted"] = ""
        
        forms = CompiledForms("expense", "POST", edited_data)

        # Check that CompiledForm is invalid
        self.assertFalse(forms.is_valid())

    def test_invalid_item_date(self):
        """Confirms is_valid() returns false with invalid item date"""
        edited_data = self.valid_data
        edited_data["item_set-0-date_item"] = ""
        
        forms = CompiledForms("expense", "POST", edited_data)

        # Check that CompiledForm is invalid
        self.assertFalse(forms.is_valid())

    def test_invalid_item_description(self):
        """Confirms is_valid() returns false with invalid item description"""
        edited_data = self.valid_data
        edited_data["item_set-0-description"] = ""
        
        forms = CompiledForms("expense", "POST", edited_data)

        # Check that CompiledForm is invalid
        self.assertFalse(forms.is_valid())

    def test_invalid_item_amount(self):
        """Confirms is_valid() returns false with invalid item amount"""
        edited_data = self.valid_data
        edited_data["item_set-0-amount"] = ""
        
        forms = CompiledForms("expense", "POST", edited_data)

        # Check that CompiledForm is invalid
        self.assertFalse(forms.is_valid())

    def test_invalid_item_gst(self):
        """Confirms is_valid() returns false with invalid item gst"""
        edited_data = self.valid_data
        edited_data["item_set-0-gst"] = ""
        
        forms = CompiledForms("expense", "POST", edited_data)

        # Check that CompiledForm is invalid
        self.assertFalse(forms.is_valid())

    def test_invalid_financial_code_code(self):
        """Confirms is_valid() returns false with invalid code"""
        edited_data = self.valid_data
        edited_data["item_set-0-coding_set-0-code"] = ""
        
        forms = CompiledForms("expense", "POST", edited_data)

        # Check that CompiledForm is invalid
        self.assertFalse(forms.is_valid())

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_invalid_attachment_file_size(self):
        """Confirms is_valid() returns false with file > 10 mb"""
        # Creates invalid file (10 mb + 1 b) and test validation
        with tempfile.NamedTemporaryFile("w+b", suffix=".txt") as test_file:
            # Create file
            test_file.write(b"1" * ((1024 * 1024 * 10) + 1))
            test_file.seek(0)

            # Add the file the data
            files = MultiValueDict({
                "newattachment-attachment_files": [
                    InMemoryUploadedFile(test_file, None, "test.txt", "text/plain", (1024 * 1024 * 10) + 1, None),
                ]
            })

            # Create the compiled forms
            forms = CompiledForms("expense", "POST", self.valid_data, files)

            # Check that CompiledForm is invalid
            self.assertFalse(forms.is_valid())

    def test_invalid_old_attachment(self):
        """Confirms is_valid() returns false with invalid old attachment"""
        invalid_data = self.valid_data
        invalid_data["financialtransactionmatch_set-0-id"] = 1
        invalid_data["financialtransactionmatch_set-0-attachment"] = ""
        invalid_data["financialtransactionmatch_set-TOTAL_FORMS"] = 1
        invalid_data["financialtransactionmatch_set-INITIAL_FORMS"] = 1

        invalid_forms = CompiledForms(
            "expense",
            "POST",
            invalid_data,
        )

        # Check that CompiledForm is invalid
        self.assertFalse(invalid_forms.is_valid())

    def test_invalid_with_no_items(self):
        """Tests that form is invalid if no items are submitted"""
        invalid_data = self.valid_data
        invalid_data["item_set-0-date_item"] = ""
        invalid_data["item_set-0-description"] = ""
        invalid_data["item_set-0-amount"] = ""
        invalid_data["item_set-0-gst"] = ""

        forms = CompiledForms("expense", "POST", invalid_data)

        self.assertFalse(forms.is_valid())

    def test_corrupt_financial_code_match_when_setting_initial_data(self):
        """
            Tests handling when a financial code match is not
            available for an item ID
        """
        form = CompiledForms(
            "expense"
            "GET"
        )

        self.assertIsNone(
            form._CompiledForms__set_financial_code_data(999999999, 1, "")
        )

    def test_invalid_when_all_items_deleted(self):
        """Tests forms invalid when all items marked for deletion"""
        # Save initial item
        forms = CompiledForms("expense", "POST", self.valid_data)
        self.assertTrue(forms.is_valid())
        forms.save()

        # Retrieve the newly saved items to re-populate form
        transaction = FinancialTransaction.objects.last()
        item = Item.objects.last()
        code_matches = item.financialcodematch_set.all().order_by("id")

        # Update the data
        delete_data = self.valid_data
        delete_data["item_set-0-id"] = item.id
        delete_data["item_set-0-transaction"] = transaction.id
        delete_data["item_set-0-DELETE"] = "on"
        delete_data["item_set-0-coding_set-0-financial_code_match_id"] = code_matches[0].id
        delete_data["item_set-0-coding_set-1-financial_code_match_id"] = code_matches[1].id
        delete_data["item_set-INITIAL_FORMS"] = 1

        # Check that form is now invalid
        delete_forms = CompiledForms("expense", "POST", delete_data, transaction_id=transaction.id)
        self.assertFalse(delete_forms.is_valid())
