"""Test cases for the transactions app views"""

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.urls.exceptions import NoReverseMatch

from transactions.models import Transaction, Item, FinancialCodeMatch

DELETE_FIXTURES = [
    "transactions/tests/fixtures/authentication.json",
    "transactions/tests/fixtures/country.json",
    "transactions/tests/fixtures/demographics.json",
    "transactions/tests/fixtures/financial_code_system.json",
    "transactions/tests/fixtures/financial_code_group.json",
    "transactions/tests/fixtures/budget_year.json",
    "transactions/tests/fixtures/financial_code.json",
    "transactions/tests/fixtures/transaction.json",
    "transactions/tests/fixtures/item.json",
    "transactions/tests/fixtures/financial_code_match.json",
]

class ExpenseDeleteTest(TestCase):
    """Tests for the delete expense view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = DELETE_FIXTURES

    def test_expense_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse(
                "transaction_delete",
                kwargs={"t_type": "expense", "transaction_id": 1}
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_expense_delete_url_exists_at_desired_location(self):
        """Checks that the delete expense page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/expense/delete/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_expense_delete_html404_on_invalid_url(self):
        """Checks that the delete expense page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/expense/delete/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_expense_delete_accessible_by_name(self):
        """Checks that delete expense page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse(
                "transaction_delete",
                kwargs={"t_type": "expense", "transaction_id": 1}
            )
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_expense_delete_html404_on_invalid_name(self):
        """Checks that delete expense page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse(
                "transaction_delete",
                kwargs={"t_type": "expense", "transaction_id": 999999999}
            )
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_expense_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse(
                "transaction_delete",
                kwargs={"t_type": "expense", "transaction_id": 1}
            )
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "transactions/delete.html")
        
    def test_expense_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse(
                "transaction_delete",
                kwargs={"t_type": "expense", "transaction_id": 1}
            ),
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("transactions_dashboard"))

    def test_expense_delete_post_failed_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse(
                "transaction_delete",
                kwargs={"t_type": "expense", "transaction_id": 999999999}
            ),
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_expense_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse(
                "transaction_delete",
                kwargs={"t_type": "expense", "transaction_id": 1}
            )
        )

        # Checks that Transaction was deleted
        self.assertEqual(0, Transaction.objects.filter(id=1).count())

        # Checks that Items were deleted
        self.assertEqual(0, Item.objects.filter(id=1).count())
        self.assertEqual(0, Item.objects.filter(id=2).count())
        
        # Checks that financial code matches were deleted
        self.assertEqual(0, FinancialCodeMatch.objects.filter(item_id=1).count())

        # Check that other expeneses and items not deleted
        self.assertNotEqual(0, Transaction.objects.count())
        self.assertNotEqual(0, Item.objects.count())
 
class RevenueDeleteTest(TestCase):
    """Tests covering revenue-specific delete views"""
    # pylint: disable=no-member,protected-access
    fixtures = DELETE_FIXTURES
       
    def test_revenue_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse(
                "transaction_delete",
                kwargs={"t_type": "revenue", "transaction_id": 2}
            )
        )

        self.assertEqual(response.status_code, 302)

    def test_revenue_delete_url_exists_at_desired_location(self):
        """Checks that the delete expense page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/revenue/delete/2")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_revenue_delete_accessible_by_name(self):
        """Checks that delete expense page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse(
                "transaction_delete",
                kwargs={"t_type": "revenue", "transaction_id": 2}
            )
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
       
class TransactionDeleteTest(TestCase):
    """Tests covering remaining delete transaction views"""
    # pylint: disable=no-member,protected-access,duplicate-code
    fixtures = DELETE_FIXTURES
       
    def test_transaction_delete_html404_on_invalid_url(self):
        """Checks that the transaction page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/abc/delete/2")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)
        
    def test_transaction_delete_html404_on_invalid_name(self):
        """Checks that the transaction page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")

        exception = False

        try:
            self.client.get(
                reverse(
                    "transaction_delete",
                    kwargs={"t_type": "abc", "transaction_id": 1}
                )
            )
        except NoReverseMatch:
            exception = True

        # Check that exception is raised
        self.assertTrue(exception)
 