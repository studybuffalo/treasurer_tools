"""Test cases for the bank_transactions app views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from bank_transactions.models import Statement, BankTransaction

class BankDashboardTest(TestCase):
    """Tests for the bank dashboard view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
    ]

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
        response = self.client.get(reverse("bank_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/index.html")

class StatementAddTest(TestCase):
    """Tests for the add statement view"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
    ]
    
    def setUp(self):
        self.correct_statement_data = {
            "account": 1,
            "date_start": "2017-01-01",
            "date_end": "2017-01-31",
            "banktransaction_set-TOTAL_FORMS": 0,
            "banktransaction_set-INITIAL_FORMS": 0,
            "banktransaction_set-MIN_NUM_FORMS": 0,
            "banktransaction_set-MAX_NUM_FORMS": 1000,
        }
        self.correct_transaction_data = {
            "account": 1,
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
        response = self.client.get(reverse("statement_add"))

        self.assertEqual(response.status_code, 302)

    def test_statement_add_url_exists_at_desired_location(self):
        """Checks that the add statement page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/statement/add/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_statement_add_accessible_by_name(self):
        """Checks that add statement page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("statement_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_statement_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("statement_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/add.html")

    def test_statement_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("statement_add"), self.correct_statement_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_dashboard"))

    def test_statement_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("statement_add"), self.correct_statement_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one statement was added
        self.assertEqual(1, Statement.objects.count())
    
    def test_statement_add_transaction_add(self):
        """Confirms that a transaction can be added along with statement"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("statement_add"),
            self.correct_transaction_data,
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one statement was added
        self.assertEqual(1, BankTransaction.objects.count())
    

class StatementEditTest(TestCase):
    """Tests for the edit statement view"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
        "bank_transactions/tests/fixtures/statement.json",
        "bank_transactions/tests/fixtures/bank_transaction.json",
    ]
       
    def setUp(self):
        # Add standard test data
        self.correct_data = {
            "account": 1,
            "date_start": "2017-01-01",
            "date_end": "2017-01-31",
            "banktransaction_set-0-id": 1,
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

    def test_statement_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("statement_edit", kwargs={"statement_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_statement_edit_url_exists_at_desired_location(self):
        """Checks that the edit statement page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/statement/edit/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

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
            reverse("statement_edit", kwargs={"statement_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_statement_edit_html404_on_invalid_name(self):
        """Checks that edit statement page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("statement_edit", kwargs={"statement_id": 999999999})
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_statement_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("statement_edit", kwargs={"statement_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/edit.html")
        
    def test_statement_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["end_date"] = "2017-12-31"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("statement_edit", kwargs={"statement_id": 1}),
            edited_data,
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_dashboard"))

    def test_statement_edit_post_failed_on_invalid_statement_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["end_date"] = "2017-12-31"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("statement_edit", kwargs={"statement_id": 999999999}),
            edited_data,
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)
        
    def test_statement_edit_post_confirm_statement_edit(self):
        """Confirms banktransaction is properly edited via the statement edit form"""
        # Setup edited data
        edited_data = self.correct_data
        edited_data["date_end"] = "2017-12-31"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("statement_edit", kwargs={"statement_id": 1}),
            edited_data
        )

        # Confirm still only 1 entry
        self.assertEqual(1, Statement.objects.count())

        # Confirm name has been updated properly
        self.assertEqual(
            str(Statement.objects.get(id=1).date_end),
            "2017-12-31"
        )

    def test_statement_edit_post_confirm_bank_transaction_edit(self):
        """Confirms that transaction can be edited in edit statement form"""
        edited_data = self.correct_data
        edited_data["banktransaction_set-0-description_bank"] = "4"
        edited_data["banktransaction_set-0-description_user"] = "5"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("statement_edit", kwargs={"statement_id": 1}),
            edited_data
        )

        # Confirm still only 4 entrries
        self.assertEqual(4, BankTransaction.objects.count())

        # Confirm banktransaction number has been updated properly
        self.assertEqual(
            BankTransaction.objects.get(id=1).description_bank,
            "4"
        )

        # Confirm name has been updated properly
        self.assertEqual(
            BankTransaction.objects.get(id=1).description_user,
            "5"
        )

    def test_statement_edit_post_fail_on_invalid_bank_transaction_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Setup edited data
        edited_data = self.correct_data
        edited_data["banktransaction_set-0-id"] = "999999999"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("statement_edit", kwargs={"statement_id": 1}),
            edited_data
        )

        # Check for the expected ValidationError
        self.assertEqual(
            response.context["formsets"][0].errors["id"][0],
            "Select a valid choice. That choice is not one of the available choices."
        )
        
    def test_statement_edit_post_add_bank_transaction(self):
        """Checks that a new banktransaction is added via the edit statement form"""
        added_data = self.correct_data
        added_data["banktransaction_set-1-id"] = ""
        added_data["banktransaction_set-1-date_transaction"] = "2017-01-05"
        added_data["banktransaction_set-1-description_bank"] = "DEP"
        added_data["banktransaction_set-1-description_user"] = "Deposit"
        added_data["banktransaction_set-1-amount_debit"] = 0.00
        added_data["banktransaction_set-1-amount_credit"] = 200.00
        added_data["banktransaction_set-TOTAL_FORMS"] = 2

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("statement_edit", kwargs={"statement_id": 1}),
            added_data
        )

        # Check that the number of banktransactions has increased
        self.assertEqual(
            BankTransaction.objects.count(),
            5
        )

        # Check that original banktransactions still exist
        self.assertEqual(
            str(BankTransaction.objects.get(id=1).date_transaction),
            "2017-01-01"
        )

        self.assertEqual(
            str(BankTransaction.objects.get(id=2).date_transaction),
            "2017-01-02"
        )

        self.assertEqual(
            str(BankTransaction.objects.get(id=3).date_transaction),
            "2017-01-03"
        )

        self.assertEqual(
            str(BankTransaction.objects.get(id=4).date_transaction),
            "2017-01-04"
        )

        # Check that the new banktransaction was saved properly
        self.assertEqual(
            str(BankTransaction.objects.get(id=5).date_transaction),
            "2017-01-05"
        )

    def test_statement_edit_post_delete_bank_transaction(self):
        """Checks that bank transaction is deleted via the edit statement form"""
        # Setup the delete data
        delete_data = self.correct_data
        delete_data["banktransaction_set-0-DELETE"] = "on"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("statement_edit", kwargs={"statement_id": 1}),
            delete_data
        )
        
        # Check that the number of banktransactions has decreased
        self.assertEqual(
            BankTransaction.objects.count(),
            3
        )

        # Check that the proper ID has been removed
        self.assertEqual(
            BankTransaction.objects.filter(id=1).count(),
            0
        )
        
class StatementDeleteTest(TestCase):
    """Tests for the delete statement view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
        "bank_transactions/tests/fixtures/statement.json",
    ]

    def test_statement_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("statement_delete", kwargs={"statement_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_statement_delete_url_exists_at_desired_location(self):
        """Checks that the delete statement page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/banking/statement/delete/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

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
            reverse("statement_delete", kwargs={"statement_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_statement_delete_html404_on_invalid_name(self):
        """Checks that delete statement page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("statement_delete", kwargs={"statement_id": 999999999})
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_statement_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("statement_delete", kwargs={"statement_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "bank_transactions/delete.html")
        
    def test_statement_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("statement_delete", kwargs={"statement_id": 1}),
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_dashboard"))

    def test_statement_delete_post_failed_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("statement_delete", kwargs={"statement_id": 999999999}),
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_statement_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse("statement_delete", kwargs={"statement_id": 1})
        )

        # Checks that statement was deleted
        self.assertEqual(0, Statement.objects.filter(id=1).count())

        # Checks that BankTransactions were deleted
        self.assertEqual(0, BankTransaction.objects.count())
