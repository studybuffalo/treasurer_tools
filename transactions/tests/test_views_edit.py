"""Test cases for the transactions app views"""

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls.exceptions import NoReverseMatch

from transactions.models import Transaction, Item, FinancialCodeMatch, AttachmentMatch
from documents.models import Attachment

EDIT_FIXTURES = [
    "transactions/tests/fixtures/authentication.json",
    "transactions/tests/fixtures/country.json",
    "transactions/tests/fixtures/demographics.json",
    "transactions/tests/fixtures/financial_code_system.json",
    "transactions/tests/fixtures/budget_year.json",
    "transactions/tests/fixtures/financial_code_group.json",
    "transactions/tests/fixtures/financial_code.json",
    "transactions/tests/fixtures/attachment.json",
    "transactions/tests/fixtures/transaction.json",
    "transactions/tests/fixtures/item.json",
    "transactions/tests/fixtures/financial_code_match.json",
    "transactions/tests/fixtures/attachment_match.json",
]

class ExpenseEditTest(TestCase):
    """Tests for the edit expense view"""
    # pylint: disable=no-member,protected-access,duplicate-code
    fixtures = EDIT_FIXTURES
       
    def setUp(self):
        # Add standard test data
        self.correct_data = {
            "payee_payer": 1,
            "memo": "Travel Grant award 2017",
            "date_submitted": "2017-06-01",
            "item_set-0-id": 1,
            "item_set-0-transaction": 1,
            "item_set-0-date_item": "2017-06-01",
            "item_set-0-description": "Taxi costs",
            "item_set-0-amount": 100.00,
            "item_set-0-gst": 5.00,
            "item_set-0-coding_set-0-financial_code_match_id": 1,
            "item_set-0-coding_set-0-budget_year": 1,
            "item_set-0-coding_set-0-code": 1,
            "item_set-0-coding_set-1-financial_code_match_id": 2,
            "item_set-0-coding_set-1-budget_year": 3,
            "item_set-0-coding_set-1-code": 5,
            "item_set-1-id": 2,
            "item_set-1-transaction": 1,
            "item_set-1-date_item": "2017-06-02",
            "item_set-1-description": "Hotel Costs",
            "item_set-1-amount": 205.57,
            "item_set-1-gst": 10.72,
            "item_set-1-coding_set-0-financial_code_match_id": 3,
            "item_set-1-coding_set-0-budget_year": 1,
            "item_set-1-coding_set-0-code": 1,
            "item_set-1-coding_set-1-financial_code_match_id": 4,
            "item_set-1-coding_set-1-budget_year": 3,
            "item_set-1-coding_set-1-code": 5,
            "item_set-TOTAL_FORMS": 2,
            "item_set-INITIAL_FORMS": 2,
            "item_set-MIN_NUM_FORMS": 1,
            "item_set-MAX_NUM_FORMS": 1000,
            "attachmentmatch_set-0-transaction": 1,
            "attachmentmatch_set-0-id": 1,
            "attachmentmatch_set-0-attachment": 1,
            "attachmentmatch_set-0-DELETE": "",
            "attachmentmatch_set-TOTAL_FORMS": 1,
            "attachmentmatch_set-INITIAL_FORMS": 1,
            "attachmentmatch_set-MIN_NUM_FORMS": 0,
            "attachmentmatch_set-MAX_NUM_FORMS": 20,
        }

    def test_expense_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_expense_edit_url_exists_at_desired_location(self):
        """Checks that the edit expense page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/expense/edit/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_expense_edit_html404_on_invalid_url(self):
        """Checks that the edit expense page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/expense/edit/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_expense_edit_accessible_by_name(self):
        """Checks that edit expense page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            )
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_expense_edit_html404_on_invalid_name(self):
        """Checks that edit expense page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 999999999}
            )
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_expense_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            )
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "transactions/edit.html")
        
    def test_expense_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["date_submitted"] = "2017-12-01"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            ),
            edited_data,
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("transactions_dashboard"))

    def test_expense_edit_fails_on_invalid_transaction_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["date_submitted"] = "2017-12-01"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 999999999}
            ),
            edited_data,
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)
        
    def test_expense_edit_confirm_transaction_edit(self):
        """Confirms transaction is properly edited via the expense edit form"""
        # Setup edited data
        edited_data = self.correct_data
        edited_data["date_submitted"] = "2017-12-01"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            ),
            edited_data
        )

        # Confirm still only 2 transaction items
        self.assertEqual(2, Transaction.objects.count())

        # Confirm name has been updated properly
        self.assertEqual(
            str(Transaction.objects.get(id=1).date_submitted),
            "2017-12-01"
        )

    def test_expense_edit_confirm_item_edit(self):
        """Confirms that item can be edited in edit expense form"""
        edited_data = self.correct_data
        edited_data["item_set-0-description"] = "Fancy dinner"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            ),
            edited_data
        )

        # Confirm still only 2 transaction entries
        self.assertEqual(2, Transaction.objects.count())

        # Confirm still only 3 item entries
        self.assertEqual(3, Item.objects.count())

        # Confirm item description has been updated properly
        self.assertEqual(
            Item.objects.get(id=1).description,
            "Fancy dinner"
        )

    def test_expense_edit_fails_on_invalid_item_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Setup edited data
        edited_data = self.correct_data
        edited_data["item_set-0-id"] = "999999999"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            ),
            edited_data
        )

        # Check for the expected ValidationError
        self.assertEqual(
            response.context["forms"].forms.item_formsets[0].item_formset.errors["id"][0],
            "Select a valid choice. That choice is not one of the available choices."
        )
        
    def test_expense_edit_add_item(self):
        """Checks that a new item is added via the edit expense form"""
        added_data = self.correct_data
        added_data["item_set-2-id"] = ""
        added_data["item_set-2-date_item"] = "2017-06-03"
        added_data["item_set-2-description"] = "Fancy dinner"
        added_data["item_set-2-amount"] = 50.00
        added_data["item_set-2-gst"] = 2.50
        added_data["item_set-2-coding_set-0-financial_code_match_id"] = ""
        added_data["item_set-2-coding_set-0-budget_year"] = 1
        added_data["item_set-2-coding_set-0-code"] = 1
        added_data["item_set-2-coding_set-1-financial_code_match_id"] = ""
        added_data["item_set-2-coding_set-1-budget_year"] = 3
        added_data["item_set-2-coding_set-1-code"] = 5
        added_data["item_set-TOTAL_FORMS"] = 3

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            ),
            added_data
        )

        # Check that the number of items has increased
        self.assertEqual(
            Item.objects.count(),
            4
        )

        # Check that original items still exist
        self.assertEqual(
            str(Item.objects.get(id=1).description),
            "Taxi costs"
        )

        # Check that the new item is saved properly
        self.assertEqual(
            Item.objects.all().last().description,
            "Fancy dinner"
        )

    def test_expense_edit_delete_item(self):
        """Checks that item is deleted via the edit expense form"""
        # Setup the delete data
        delete_data = self.correct_data
        delete_data["item_set-0-DELETE"] = "on"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            ),
            delete_data
        )
        
        # Check that the number of items has decreased
        self.assertEqual(
            Item.objects.count(),
            2
        )

        # Check that the proper ID has been removed
        self.assertEqual(
            Item.objects.filter(id=1).count(),
            0
        )
        
    def test_expense_edit_delete_item_fails_on_zero_items(self):
        """Checks that a transaction cannot be edited below zero items"""
        # Setup the delete data
        delete_data = self.correct_data
        delete_data["item_set-0-DELETE"] = "on"
        delete_data["item_set-1-DELETE"] = "on"
        
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            ),
            delete_data
        )

        self.assertEqual(
            response.context["forms"].forms.item_formset.non_form_errors()[0],
            "Please submit 1 or more forms."
        )
        
    def test_expense_edit_fails_on_missing_financial_code(self):
        """Confirms expense edit fails without financial code"""
        edited_data = self.correct_data
        edited_data["item_set-0-coding_set-0-code"] = None
        
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            ),
            edited_data,
        )

        # Check for proper error message
        self.assertEqual(
            response.context["forms"].forms.item_formsets[0].financial_code_forms[0].form.errors["code"][0],
            "Select a valid choice. None is not one of the available choices."
        )

        # Check that no transaction was added/deleted
        self.assertEqual(2, Transaction.objects.count())

        # Check that no items were added/deleted
        self.assertEqual(3, Item.objects.count())
        
        # Check that no financial code matching was added/deleted
        self.assertEqual(6, FinancialCodeMatch.objects.count())

        # Check that the original financial code match code is unchanged
        self.assertEqual(1, FinancialCodeMatch.objects.get(id=1).financial_code.id)
        
    def test_expense_edit_fails_on_incorrect_financial_code(self):
        """Confirms expense edit fails with incorrect financial code"""
        edited_data = self.correct_data
        edited_data["item_set-0-coding_set-0-code"] = 999999999
        
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "expense", "transaction_id": 1}
            ),
            edited_data,
        )

        # Check for proper error message
        self.assertEqual(
            response.context["forms"].forms.item_formsets[0].financial_code_forms[0].form.errors["code"][0],
            "Select a valid choice. 999999999 is not one of the available choices."
        )
        
        # Check that no transaction was added/deleted
        self.assertEqual(2, Transaction.objects.count())

        # Check that no items were added/deleted
        self.assertEqual(3, Item.objects.count())
        
        # Check that no financial code matching was added/deleted
        self.assertEqual(6, FinancialCodeMatch.objects.count())

        # Check that the original financial code match code is unchanged
        self.assertEqual(1, FinancialCodeMatch.objects.get(id=1).financial_code.id)

    def test_expense_edit_add_attachment(self):
        """Confirms data & files added to database on successful submission"""
        # Get starting numbers for database objects
        transaction_total = Transaction.objects.count()

        with open("transactions/tests/files/test.pdf", "rb") as test_file:
            correct_data = self.correct_data
            correct_data["newattachment-attachment_files"] = InMemoryUploadedFile(test_file, None, "test.pdf", "application/pdf", None, None)

            self.client.login(username="user", password="abcd123456")
            response = self.client.post(
                reverse(
                    "transaction_edit", 
                    kwargs={"t_type": "expense", "transaction_id": 1}
                ),
                correct_data,
                format="multipart/form-data",
                follow=True,
            )

            # Get reference to the new attachment
            attachment_instance = Attachment.objects.first()

            # Check that user logged in
            self.assertEqual(str(response.context['user']), 'user')
        
            # Check that number of transactions is the same
            self.assertEqual(Transaction.objects.count(), transaction_total)

            # Check that one attachment match was added
            self.assertEqual(1, AttachmentMatch.objects.count())

            # Check that one attachment was added
            self.assertEqual(1, Attachment.objects.count())

            # Check that the attachment match used the right transaction
            self.assertEqual(
                AttachmentMatch.objects.first().transaction.id,
                Transaction.objects.first().id
            )

            self.assertEqual(
                AttachmentMatch.objects.first().attachment.id,
                attachment_instance.id
            )

            # Get the path to the new file
            attachment_path = Path(self.media_file_dir, Path(str(attachment_instance.location)))

            # Check that the file exists in the new directory
            self.assertTrue(attachment_path.exists())

            # Remove the new test file
            attachment_path.remove()
class RevenueEditTest(TestCase):
    """Tests covering revenue-specific edit views"""
    # pylint: disable=no-member,protected-access,duplicate-code
    fixtures = EDIT_FIXTURES
       
    def test_revenue_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "revenue", "transaction_id": 2}
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_revenue_edit_url_exists_at_desired_location(self):
        """Checks that the edit expense page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/revenue/edit/2")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_revenue_edit_accessible_by_name(self):
        """Checks that edit expense page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse(
                "transaction_edit",
                kwargs={"t_type": "revenue", "transaction_id": 2}
            )
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
       
class TransactionEditTest(TestCase):
    """Tests covering remaining edit transaction views"""
    # pylint: disable=no-member,protected-access,duplicate-code
    fixtures = EDIT_FIXTURES
       
    def test_transaction_edit_html404_on_invalid_url(self):
        """Checks that the transaction page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/abc/edit/1")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)
        
    def test_transaction_edit_html404_on_invalid_name(self):
        """Checks that the transaction page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")

        exception = False

        try:
            self.client.get(
                reverse(
                    "transaction_edit",
                    kwargs={"t_type": "abc", "transaction_id": 1}
                )
            )
        except NoReverseMatch:
            exception = True

        # Check that exception is raised
        self.assertTrue(exception)
