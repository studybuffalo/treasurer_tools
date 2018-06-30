"""Test cases for the bank_transactions app views"""

import tempfile

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.test import TestCase, override_settings

from bank_transactions.models import Statement, BankTransaction
from documents.models import Attachment, BankStatementMatch

from .utils import (
    create_user, create_bank_account, create_bank_transactions, create_temp_pdf,
    create_bank_statement_match
)


class BankDashboardTest(TestCase):
    """Tests for the dashboard view"""

    def setUp(self):
        create_user()

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get("/banking/")

        self.assertRedirects(response, "/accounts/login/?next=/banking/")

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/")

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_transactions:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_transactions:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/index.html")

class StatementAddTest(TestCase):
    """Tests for the add statement view"""
    # Setup a temporary media_root folder to hold any attachments
    MEDIA_ROOT = tempfile.mkdtemp()

    def setUp(self):
        create_user()
        account = create_bank_account()

        self.valid_data = {
            "account": account.id,
            "date_start": "2017-01-01",
            "date_end": "2017-01-31",
            "banktransaction_set-0-date_transaction": "2017-01-01",
            "banktransaction_set-0-description_bank": "CHQ#0001",
            "banktransaction_set-0-description_user": "Cheque #0001",
            "banktransaction_set-0-amount_debit": 100.00,
            "banktransaction_set-0-amount_credit": 0.00,
            "banktransaction_set-TOTAL_FORMS": 1,
            "banktransaction_set-INITIAL_FORMS": 0,
            "banktransaction_set-MIN_NUM_FORMS": 0,
            "banktransaction_set-MAX_NUM_FORMS": 1000,
        }

    def test_statement_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("bank_transactions:add"))

        self.assertEqual(response.status_code, 302)

    def test_statement_add_no_redirect_if_logged_in(self):
        """Checks that user is not redirected if logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_transactions:add"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that 200 status code returned (i.e. no redirect)
        self.assertEqual(response.status_code, 200)

    def test_statement_add_url_exists_at_desired_location(self):
        """Checks that the add statement page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/statement/add/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_statement_add_accessible_by_name(self):
        """Checks that add statement page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_transactions:add"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_statement_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_transactions:add"))

        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/add.html")

    def test_statement_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_transactions:add"),
            self.valid_data,
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_transactions:dashboard"))

    def test_statement_add_transaction_add(self):
        """Confirms that a transaction can be added along with statement"""
        # Get current counts
        statement_total = Statement.objects.count()
        transaction_total = BankTransaction.objects.count()

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("bank_transactions:add"),
            self.valid_data,
            follow=True,
        )

        # Check that one statement was added
        self.assertEqual(
            Statement.objects.count(),
            statement_total + 1
        )

        # Check that one transaction as added
        self.assertEqual(
            BankTransaction.objects.count(),
            transaction_total + 1
        )

    def test_statement_add_invalid_statement_data(self):
        """Confirms statement cannot be processed with invalid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["date_start"] = ""

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_transactions:add"),
            invalid_data,
            follow=True,
        )

        # Check that page was not redirected to dashboard
        self.assertEqual(response.status_code, 200)

        # Check that other statement data returned
        self.assertEqual(
            response.context["statement_form"]["account"].value(),
            str(invalid_data["account"])
        )

        self.assertEqual(
            response.context["statement_form"]["date_end"].value(),
            invalid_data["date_end"]
        )

    def test_statement_add_invalid_transaction_data(self):
        """Confirms transaction cannot be processed with invalid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["banktransaction_set-0-date_transaction"] = ""

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_transactions:add"),
            invalid_data,
            follow=True,
        )

        # Check that page was not redirected to dashboard
        self.assertEqual(response.status_code, 200)

        # Check that other transaction data returned
        self.assertEqual(
            response.context["bank_transaction_formsets"][0]["description_bank"].value(),
            str(invalid_data["banktransaction_set-0-description_bank"])
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_statement_add_attachment(self):
        """Tests the file upload and attachment matching"""
        # Get current count of attachments
        attachment_total = Attachment.objects.count()
        match_total = BankStatementMatch.objects.count()

        # Create a test file to upload
        temp_file = InMemoryUploadedFile(
            create_temp_pdf(), None, "test.pdf", "application/pdf", None, None
        )

        file_data = self.valid_data
        file_data["files"] = temp_file

        # Make the POST request
        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("bank_transactions:add"),
            file_data,
            format="multipart/form-data",
            follow=True,
        )

        # Check that the attachment was added
        self.assertEqual(
            Attachment.objects.count(),
            attachment_total + 1
        )

        # Check that the attachment match was added
        self.assertEqual(
            BankStatementMatch.objects.count(),
            match_total + 1
        )

class StatementEditTest(TestCase):
    """Tests for the edit statement view"""
    # Setup a temporary media_root folder to hold any attachments
    MEDIA_ROOT = tempfile.mkdtemp()

    def setUp(self):
        create_user()
        transactions = create_bank_transactions()

        self.valid_data = {
            "account": transactions[0].statement.account.id,
            "date_start": transactions[0].statement.date_start,
            "date_end": transactions[0].statement.date_end,
            "banktransaction_set-0-date_transaction": transactions[0].date_transaction,
            "banktransaction_set-0-description_bank": transactions[0].description_bank,
            "banktransaction_set-0-description_user": transactions[0].description_user,
            "banktransaction_set-0-amount_debit": transactions[0].amount_debit,
            "banktransaction_set-0-amount_credit": transactions[0].amount_credit,
            "banktransaction_set-0-id": transactions[0].id,
            "banktransaction_set-0-statement": transactions[0].statement.id,
            "banktransaction_set-1-date_transaction": transactions[1].date_transaction,
            "banktransaction_set-1-description_bank": transactions[1].description_bank,
            "banktransaction_set-1-description_user": transactions[1].description_user,
            "banktransaction_set-1-amount_debit": transactions[1].amount_debit,
            "banktransaction_set-1-amount_credit": transactions[1].amount_credit,
            "banktransaction_set-1-id": transactions[1].id,
            "banktransaction_set-1-statement": transactions[1].statement.id,
            "banktransaction_set-2-date_transaction": transactions[2].date_transaction,
            "banktransaction_set-2-description_bank": transactions[2].description_bank,
            "banktransaction_set-2-description_user": transactions[2].description_user,
            "banktransaction_set-2-amount_debit": transactions[2].amount_debit,
            "banktransaction_set-2-amount_credit": transactions[2].amount_credit,
            "banktransaction_set-2-id": transactions[2].id,
            "banktransaction_set-2-statement": transactions[2].statement.id,
            "banktransaction_set-3-date_transaction": transactions[3].date_transaction,
            "banktransaction_set-3-description_bank": transactions[3].description_bank,
            "banktransaction_set-3-description_user": transactions[3].description_user,
            "banktransaction_set-3-amount_debit": transactions[3].amount_debit,
            "banktransaction_set-3-amount_credit": transactions[3].amount_credit,
            "banktransaction_set-3-id": transactions[3].id,
            "banktransaction_set-3-statement": transactions[3].statement.id,
            "banktransaction_set-4-date_transaction": "",
            "banktransaction_set-4-description_bank": "",
            "banktransaction_set-4-description_user": "",
            "banktransaction_set-4-amount_debit": 0,
            "banktransaction_set-4-amount_credit": 0,
            "banktransaction_set-4-id": "",
            "banktransaction_set-4-statement": "",
            "banktransaction_set-TOTAL_FORMS": 5,
            "banktransaction_set-INITIAL_FORMS": 4,
            "banktransaction_set-MIN_NUM_FORMS": 0,
            "banktransaction_set-MAX_NUM_FORMS": 1000,
            "bankstatementmatch_set-TOTAL_FORMS": 0,
            "bankstatementmatch_set-INITIAL_FORMS": 0,
            "bankstatementmatch_set-MIN_FORMS": 0,
            "bankstatementmatch_set-MAX_FORMS": 10,
        }
        self.valid_url = "/banking/statement/edit/{}".format(transactions[0].statement.id)
        self.valid_args = {"statement_id": transactions[0].statement.id}
        self.transactions = transactions

    def test_statement_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("bank_transactions:edit", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_statement_edit_no_redirect_if_logged_in(self):
        """Checks that user is not redirected if logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("bank_transactions:edit", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that 200 status code returned (i.e. no redirect)
        self.assertEqual(response.status_code, 200)

    def test_statement_edit_url_exists_at_desired_location(self):
        """Checks that the edit statement page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_statement_edit_html404_on_invalid_url(self):
        """Checks that the edit statement page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/statement/edit/999999999")

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_statement_edit_accessible_by_name(self):
        """Checks that edit statement page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("bank_transactions:edit", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_statement_edit_html404_on_invalid_name(self):
        """Checks that edit statement page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("bank_transactions:edit", kwargs={"statement_id": 999999999})
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_statement_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("bank_transactions:edit", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/edit.html")

    def test_statement_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_transactions:edit", kwargs=self.valid_args),
            self.valid_data,
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_transactions:dashboard"))

    def test_statement_edit_post_failed_on_invalid_statement_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_transactions:edit", kwargs={"statement_id": 999999999}),
            self.valid_data,
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_statement_edit_post_confirm_statement_edit(self):
        """Confirms banktransaction is properly edited via the statement edit form"""
        statement_total = Statement.objects.count()

        # Setup edited data
        edited_data = self.valid_data
        edited_data["date_end"] = "2017-12-31"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("bank_transactions:edit", kwargs=self.valid_args),
            edited_data
        )

        # Confirm no new entries added
        self.assertEqual(
            Statement.objects.count(),
            statement_total
        )

        # Confirm name has been updated properly
        self.assertEqual(
            str(Statement.objects.get(id=self.valid_args["statement_id"]).date_end),
            edited_data["date_end"]
        )

    def test_statement_edit_post_confirm_bank_transaction_edit(self):
        """Confirms that transaction can be edited in edit statement form"""
        # Get current count of banktransactions
        transaction_total = BankTransaction.objects.count()

        # Setup modified data
        edited_data = self.valid_data
        edited_data["banktransaction_set-0-description_bank"] = "4"
        edited_data["banktransaction_set-0-description_user"] = "5"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("bank_transactions:edit", kwargs=self.valid_args),
            edited_data
        )

        # Confirm no bank transactions were added
        self.assertEqual(transaction_total, BankTransaction.objects.count())

        # Confirm banktransaction number has been updated properly
        transaction_id = edited_data["banktransaction_set-0-id"]
        self.assertEqual(
            BankTransaction.objects.get(id=transaction_id).description_bank,
            edited_data["banktransaction_set-0-description_bank"]
        )

        # Confirm name has been updated properly
        self.assertEqual(
            BankTransaction.objects.get(id=transaction_id).description_user,
            edited_data["banktransaction_set-0-description_user"]
        )

    def test_statement_edit_post_fail_on_invalid_bank_transaction_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Setup edited data
        edited_data = self.valid_data
        edited_data["banktransaction_set-0-id"] = "999999999"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_transactions:edit", kwargs=self.valid_args),
            edited_data
        )

        # Check for the expected ValidationError
        self.assertEqual(
            response.context["bank_transaction_formsets"][0].errors["id"][0],
            "Select a valid choice. That choice is not one of the available choices."
        )

    def test_statement_edit_post_delete_bank_transaction(self):
        """Checks that bank transaction is deleted via the edit statement form"""
        # Coutn the transactions
        transaction_total = BankTransaction.objects.count()

        # Setup the delete data
        delete_data = self.valid_data
        delete_data["banktransaction_set-0-DELETE"] = "on"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("bank_transactions:edit", kwargs=self.valid_args),
            delete_data
        )

        # Check that the number of banktransactions has decreased
        self.assertEqual(BankTransaction.objects.count(), transaction_total - 1)

    def test_statement_edit_fail_on_changed_statement_id(self):
        """Confirms fail when statement ID changed for transaction"""

        # Setup modified data
        edited_data = self.valid_data
        edited_data["banktransaction_set-0-statement"] = "2"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_transactions:edit", kwargs=self.valid_args),
            edited_data
        )

        # Check for the expected error
        self.assertEqual(
            response.context["bank_transaction_formsets"][0].errors["statement"][0],
            "The inline value did not match the parent instance."
        )

    def test_statement_edit_delete_attachment(self):
        """Tests deletion of attachment match"""
        # Create an attachment match
        match = create_bank_statement_match(self.transactions[0].statement)

        # Get current count of attachments
        match_total = BankStatementMatch.objects.count()
        attachment_total = Attachment.objects.count()

        # Setup the data for attachment deletion
        delete_data = self.valid_data
        delete_data["bankstatementmatch_set-TOTAL_FORMS"] = 1
        delete_data["bankstatementmatch_set-INITIAL_FORMS"] = 1
        delete_data["bankstatementmatch_set-0-DELETE"] = "on"
        delete_data["bankstatementmatch_set-0-attachment"] = match.attachment.id
        delete_data["bankstatementmatch_set-0-id"] = match.id
        delete_data["bankstatementmatch_set-0-statement"] = match.statement.id

        # Make the POST request
        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("bank_transactions:edit", kwargs=self.valid_args),
            delete_data,
            format="multipart/form-data",
            follow=True,
        )

        # Check that the attachment match was removed
        self.assertEqual(
            BankStatementMatch.objects.count(),
            match_total - 1
        )

        # Check that the attachment was removed
        self.assertEqual(
            Attachment.objects.count(),
            attachment_total - 1
        )

    @override_settings(MEDIA_ROOT=MEDIA_ROOT)
    def test_statement_edit_add_attachment(self):
        """Tests addition of attachment to statement"""
        # Get current count of attachments
        attachment_total = Attachment.objects.count()
        match_total = BankStatementMatch.objects.count()

        # Create a test file to upload
        temp_file = InMemoryUploadedFile(
            create_temp_pdf(), None, "test.pdf", "application/pdf", None, None
        )

        file_data = self.valid_data
        file_data["files"] = temp_file

        # Make the POST request
        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("bank_transactions:edit", kwargs=self.valid_args),
            file_data,
            format="multipart/form-data",
            follow=True,
        )

        # Check that the attachment was added
        self.assertEqual(
            Attachment.objects.count(),
            attachment_total + 1
        )

        # Check that the attachment match was added
        self.assertEqual(
            BankStatementMatch.objects.count(),
            match_total + 1
        )

class StatementDeleteTest(TestCase):
    """Tests for the delete statement view"""

    def setUp(self):
        create_user()
        transactions = create_bank_transactions()

        self.id = transactions[0].statement.id
        self.transactions = transactions

    def test_statement_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("bank_transactions:delete", kwargs={"statement_id": self.id})
        )

        self.assertEqual(response.status_code, 302)

    def test_statement_delete_no_redirect_if_logged_in(self):
        """Checks that user is not redirected if logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("bank_transactions:delete", kwargs={"statement_id": self.id})
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that 200 status code returned (i.e. no redirect)
        self.assertEqual(response.status_code, 200)

    def test_statement_delete_url_exists_at_desired_location(self):
        """Checks that the delete statement page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/statement/delete/{}".format(self.id))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_statement_delete_html404_on_invalid_url(self):
        """Checks that the delete statement page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/statement/delete/999999999")

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_statement_delete_accessible_by_name(self):
        """Checks that delete statement page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("bank_transactions:delete", kwargs={"statement_id": self.id})
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_statement_delete_html404_on_invalid_name(self):
        """Checks that delete statement page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("bank_transactions:delete", kwargs={"statement_id": 999999999})
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_statement_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("bank_transactions:delete", kwargs={"statement_id": self.id})
        )

        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/delete.html")

    def test_statement_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("bank_transactions:delete", kwargs={"statement_id": self.id}),
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_transactions:dashboard"))

    def test_statement_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Get original database counts
        statement_total = Statement.objects.count()
        transaction_total = BankTransaction.objects.count()

        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse("bank_transactions:delete", kwargs={"statement_id": self.id})
        )

        # Checks that statement was deleted
        self.assertEqual(Statement.objects.count(), statement_total - 1)

        # Checks that BankTransactions were deleted
        self.assertEqual(BankTransaction.objects.count(), transaction_total - 4)

    def test_statement_delete_confirm_attachment_match_deletion(self):
        """Confirms deletion form works properly"""
        # Create an attachment match
        create_bank_statement_match(self.transactions[0].statement)

        # Get original database counts
        statement_total = Statement.objects.count()
        transaction_total = BankTransaction.objects.count()
        attachment_match_total = BankStatementMatch.objects.count()

        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse("bank_transactions:delete", kwargs={"statement_id": self.id})
        )

        # Checks that statement was deleted
        self.assertEqual(Statement.objects.count(), statement_total - 1)

        # Checks that BankTransactions were deleted
        self.assertEqual(BankTransaction.objects.count(), transaction_total - 4)

        # Checks that the attachment match was deleted
        self.assertEqual(BankStatementMatch.objects.count(), attachment_match_total - 1)
