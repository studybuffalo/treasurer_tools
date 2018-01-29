"""Test cases for the transactions app views"""
from unipath import Path

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls.exceptions import NoReverseMatch

from transactions.models import Transaction, Item, FinancialCodeMatch, AttachmentMatch
from documents.models import Attachment

class ExpenseAddTest(TestCase):
    """Tests for the add expense view"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "transactions/tests/fixtures/authentication.json",
        "transactions/tests/fixtures/country.json",
        "transactions/tests/fixtures/demographics.json",
        "transactions/tests/fixtures/financial_code_system.json",
        "transactions/tests/fixtures/budget_year.json",
        "transactions/tests/fixtures/financial_code_group.json",
        "transactions/tests/fixtures/financial_code.json",
    ]

    def setUp(self):
        self.correct_data = {
            "payee_payer": 1,
            "memo": "Travel Grant award 2017",
            "date_submitted": "2017-06-01",
            "item_set-0-date_item": "2017-06-01",
            "item_set-0-description": "Taxi costs",
            "item_set-0-amount": 100.00,
            "item_set-0-gst": 5.00,
            "item_set-0-id": "",
            "item_set-0-transaction": "",
            "item_set-0-coding_set-0-financial_code_match_id": "",
            "item_set-0-coding_set-0-budget_year": 1,
            "item_set-0-coding_set-0-code": 1,
            "item_set-0-coding_set-1-financial_code_match_id": "",
            "item_set-0-coding_set-1-budget_year": 3,
            "item_set-0-coding_set-1-code": 5,
            "item_set-TOTAL_FORMS": 1,
            "item_set-INITIAL_FORMS": 0,
            "item_set-MIN_NUM_FORMS": 1,
            "item_set-MAX_NUM_FORMS": 1000,
            "attachmentmatch_set-TOTAL_FORMS": 0,
            "attachmentmatch_set-INITIAL_FORMS": 0,
            "attachmentmatch_set-MIN_NUM_FORMS": 0,
            "attachmentmatch_set-MAX_NUM_FORMS": 20,
        }

        self.cwd = Path().cwd()
        self.test_file_dir = self.cwd.child("transactions", "tools", "files")
        self.media_file_dir = self.cwd.child("media")

    def test_expense_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("transaction_add", kwargs={"t_type": "expense"})
        )

        self.assertEqual(response.status_code, 302)

    def test_expense_add_url_exists_at_desired_location(self):
        """Checks that the add expense page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/expense/add/")

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_expense_add_accessible_by_name(self):
        """Checks that add expense page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("transaction_add", kwargs={"t_type": "expense"})
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_expense_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("transaction_add", kwargs={"t_type": "expense"})
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "transactions/add.html")

    def test_expense_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("transaction_add", kwargs={"t_type": "expense"}),
            self.correct_data,
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("transactions_dashboard"))

    def test_expense_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("transaction_add", kwargs={"t_type": "expense"}),
            self.correct_data,
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one transaction was added
        self.assertEqual(1, Transaction.objects.count())

        # Check that one item was added
        self.assertEqual(1, Item.objects.count())
        
        # Check that item was associated with the transaction
        self.assertEqual(1, Transaction.objects.first().item_set.count())

        # Check that financial code matches were added
        self.assertEqual(2, FinancialCodeMatch.objects.count())

        # Check that financial code match entries are associated with item
        self.assertEqual(2, Item.objects.first().financialcodematch_set.count())

    def test_expense_fail_on_missing_financial_code(self):
        """Confirms expense addition fails without financial code"""
        edited_data = self.correct_data
        edited_data["item_set-0-coding_set-0-code"] = None
        
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("transaction_add", kwargs={"t_type": "expense"}),
            edited_data,
        )

        # Check for proper error message
        self.assertEqual(
            response.context["forms"].forms.item_formsets[0].financial_code_forms[0].form.errors["code"][0],
            "Select a valid choice. None is not one of the available choices."
        )

        # Check that no transaction was added
        self.assertEqual(0, Transaction.objects.count())

        # Check that no items were added
        self.assertEqual(0, Item.objects.count())
        
        # Check that no financial code matching was added
        self.assertEqual(0, FinancialCodeMatch.objects.count())
        
    def test_expense_fail_on_incorrect_financial_code(self):
        """Confirms expense addition fails without financial code"""
        edited_data = self.correct_data
        edited_data["item_set-0-coding_set-0-code"] = 999999999
        
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("transaction_add", kwargs={"t_type": "expense"}),
            edited_data,
        )

        # Check for proper error message
        self.assertEqual(
            response.context["forms"].forms.item_formsets[0].financial_code_forms[0].form.errors["code"][0],
            "Select a valid choice. 999999999 is not one of the available choices."
        )

        # Check that no transaction was added
        self.assertEqual(0, Transaction.objects.count())

        # Check that no items were added
        self.assertEqual(0, Item.objects.count())
        
        # Check that no financial code matching was added
        self.assertEqual(0, FinancialCodeMatch.objects.count())

    def test_expense_add_attachment(self):
        """Confirms data & files added to database on successful submission"""
        with open("transactions/tests/files/test.pdf", "rb") as test_file:
            correct_data = self.correct_data
            correct_data["newattachment-attachment_files"] = InMemoryUploadedFile(
                test_file, None, "test.pdf", "application/pdf", None, None
            )

            self.client.login(username="user", password="abcd123456")
            response = self.client.post(
                reverse("transaction_add", kwargs={"t_type": "expense"}),
                correct_data,
                format="multipart/form-data",
                follow=True,
            )

            # Get reference to the new attachment
            attachment_instance = Attachment.objects.first()

            # Check that user logged in
            self.assertEqual(str(response.context['user']), 'user')
            
            # Check that one transaction was added
            self.assertEqual(1, Transaction.objects.count())

            # Check that one attachment match was added
            self.assertEqual(1, AttachmentMatch.objects.count())

            # Check that one attachment was added
            self.assertEqual(1, Attachment.objects.count())

            # Check that attachment match used right transaction & attachment
            self.assertEqual(
                AttachmentMatch.objects.first().attachment.id,
                attachment_instance.id
            )

            self.assertEqual(
                AttachmentMatch.objects.first().transaction.id,
                Transaction.objects.first().id
            )

            # Get the path to the new file
            attachment_path = Path(self.media_file_dir, Path(str(attachment_instance.location)))

            # Check that the file exists in the new directory
            self.assertTrue(attachment_path.exists())

            # Remove the new test file
            attachment_path.remove()

class RevenueAddTest(TestCase):
    """Tests covering revenue-specific add views"""
    fixtures = [
        "transactions/tests/fixtures/authentication.json",
        "transactions/tests/fixtures/country.json",
        "transactions/tests/fixtures/demographics.json",
    ]
    
    def test_revenue_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("transaction_add", kwargs={"t_type": "revenue"})
        )

        self.assertEqual(response.status_code, 302)

    def test_revenue_add_url_exists_at_desired_location(self):
        """Checks that the add revenue page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/revenue/add/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_revenue_add_accessible_by_name(self):
        """Checks that add revenue page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("transaction_add", kwargs={"t_type": "revenue"})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

class TransactionAddTest(TestCase):
    """Tests covering remaining add transaction views"""

    def test_transaction_add_html404_on_invalid_url(self):
        """Checks that the transaction page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/abc/add/")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)
        
    def test_transaction_add_html404_on_invalid_name(self):
        """Checks that the transaction page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")

        exception = False

        try:
            self.client.get(
                reverse("transaction_add", kwargs={"t_type": "abc"})
            )
        except NoReverseMatch:
            exception = True

        # Check that exception is raised
        self.assertTrue(exception)
