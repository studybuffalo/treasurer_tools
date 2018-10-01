"""Test cases for other transactions app views"""

from django.urls import reverse
from django.test import TestCase

from financial_transactions.forms import FinancialCodeAssignmentForm
from financial_transactions.models import FinancialTransaction, Item, FinancialCodeMatch

from .utils import create_user, create_financial_codes, create_demographics, create_financial_transactions

class TransactionsDashboard(TestCase):
    """Tests for the transactions dashboard view"""

    def setUp(self):
        create_user()

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(reverse("financial_transactions:dashboard"))

        self.assertRedirects(response, "/accounts/login/?next=/transactions/")

    def test_dashboard_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_transactions:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible and there was no dedirection
        self.assertEqual(response.status_code, 200)

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/")

        # Check that page is accessible and there was no dedirection
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_transactions:dashboard"))

        # Check for proper template
        self.assertTemplateUsed(response, "transactions/index.html")

class RetrieveTransactionsTest(TestCase):
    """Checks that transactions are retrieved properly"""

    def setUp(self):
        create_user()
        create_financial_transactions()

        self.url = "/transactions/retrieve-transactions/"
        self.valid_args = {
            "transaction_type": "a",
            "date_start": "2016-04-01",
            "date_end": "2018-03-31"
        }

    def test_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(self.url, self.valid_args)

        self.assertRedirects(
            response,
            "/accounts/login/?next={}%3Ftransaction_type%3D{}%26date_start%3D{}%26date_end%3D{}".format(
                self.url, "a", "2016-04-01", "2018-03-31"
            )
        )

    def test_no_redirect_if_logged_in(self):
        """Checks no redirect if user is logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, self.valid_args)

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible and there was no dedirection
        self.assertEqual(response.status_code, 200)

    def test_retrieval_on_valid_data(self):
        """Checks that transactions are retrieved when provided with valid data"""
        # Count total number of transactions
        transaction_total = FinancialTransaction.objects.count()

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, self.valid_args)

        # Check number of transactions retrieved
        self.assertEqual(
            len(response.context["transactions"]),
            transaction_total
        )

    def test_expense_type_filter(self):
        """Checks that you can filter by expense transaction_type"""
        # Count total number of transactions
        expense_total = FinancialTransaction.objects.filter(transaction_type="e").count()

        # Create modified args
        new_args = self.valid_args
        new_args["transaction_type"] = "e"

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, new_args)

        # Check number of transactions retrieved
        self.assertEqual(
            len(response.context["transactions"]),
            expense_total
        )

    def test_revenue_type_filter(self):
        """Checks that you can filter by revenue transaction_type"""
        # Count total number of transactions
        expense_total = FinancialTransaction.objects.filter(transaction_type="r").count()

        # Create modified args
        new_args = self.valid_args
        new_args["transaction_type"] = "r"

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, new_args)

        # Check number of transactions retrieved
        self.assertEqual(
            len(response.context["transactions"]),
            expense_total
        )

    def test_date_start_filter(self):
        """Checks that you can filter by date_start"""
        # Count total number of transactions
        transaction_total = FinancialTransaction.objects.filter(date_submitted__gte="2017-04-01").count()

        # Create modified args
        new_args = self.valid_args
        new_args["date_start"] = "2017-04-01"

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, new_args)

        # Check number of transactions retrieved
        self.assertEqual(
            len(response.context["transactions"]),
            transaction_total
        )

    def test_date_end_filter(self):
        """Checks that you can filter by date_end"""
        # Count total number of transactions
        transaction_total = FinancialTransaction.objects.filter(date_submitted__lte="2017-03-31").count()

        # Create modified args
        new_args = self.valid_args
        new_args["date_end"] = "2017-03-31"

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, new_args)

        # Check number of transactions retrieved
        self.assertEqual(
            len(response.context["transactions"]),
            transaction_total
        )

    def test_no_filter_on_invalid_transaction_type(self):
        """Checks that no type filtering occurs on invalid type"""
        # Count total number of transactions
        transaction_total = FinancialTransaction.objects.count()

        # Generate incorrect parameters
        invalid_args = self.valid_args
        invalid_args["transaction_type"] = ""

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, invalid_args)

        # Check number of transactions retrieved
        self.assertEqual(
            len(response.context["transactions"]),
            transaction_total
        )

    def test_no_filter_on_invalid_date_start(self):
        """Checks that no type filtering occurs on invalid date_start"""
        # Count total number of transactions
        transaction_total = FinancialTransaction.objects.count()

        # Generate incorrect parameters
        invalid_args = self.valid_args
        invalid_args["date_start"] = ""

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, invalid_args)

        # Check number of transactions retrieved
        self.assertEqual(
            len(response.context["transactions"]),
            transaction_total
        )

    def test_no_filter_on_invalid_date_end(self):
        """Checks that no type filtering occurs on invalid date_end"""
        # Count total number of transactions
        transaction_total = FinancialTransaction.objects.count()

        # Generate incorrect parameters
        invalid_args = self.valid_args
        invalid_args["date_end"] = ""

        # Make request
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url, invalid_args)

        # Check number of transactions retrieved
        self.assertEqual(
            len(response.context["transactions"]),
            transaction_total
        )

class FinancialTransactionAddTest(TestCase):
    """Tests for the financial transaction add view"""

    def setUp(self):
        create_user()

        payee_payer = create_demographics()
        codes = create_financial_codes()

        self.valid_data = {
            "payee_payer": payee_payer.id,
            "memo": "Travel Grant award 2017",
            "date_submitted": "2017-06-01",
            "items-0-date_item": "2017-06-01",
            "items-0-description": "Taxi costs",
            "items-0-amount": "100.0",
            "items-0-gst": "5.0",
            "items-0-id": "",
            "items-0-transaction": "",
            "items-0-coding_set-0-financial_code_match_id": "",
            "items-0-coding_set-0-budget_year": codes[0].financial_code_group.budget_year.id,
            "items-0-coding_set-0-code": codes[0].id,
            "items-0-coding_set-1-financial_code_match_id": "",
            "items-0-coding_set-1-budget_year": codes[2].financial_code_group.budget_year.id,
            "items-0-coding_set-1-code": codes[2].id,
            "items-TOTAL_FORMS": "1",
            "items-INITIAL_FORMS": "0",
            "items-MIN_NUM_FORMS": "1",
            "items-MAX_NUM_FORMS": "1000",
            "financialtransactionmatch_set-TOTAL_FORMS": "0",
            "financialtransactionmatch_set-INITIAL_FORMS": "0",
            "financialtransactionmatch_set-MIN_NUM_FORMS": "0",
            "financialtransactionmatch_set-MAX_NUM_FORMS": "20",
        }
        self.valid_args = {"t_type": "expense"}

    def test_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_transactions:add", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_add_no_redirect_if_logged_in(self):
        """Checks user is not redirected if logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_transactions:add", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_add_url_exists_at_desired_location(self):
        """Checks that the add expense page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/transactions/expense/add/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_add_accessible_by_name(self):
        """Checks that add expense page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_transactions:add", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_transactions:add", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "transactions/add_edit.html")

    def test_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_transactions:add", kwargs=self.valid_args),
            self.valid_data,
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_transactions:dashboard"))

    def test_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_transactions:add", kwargs=self.valid_args),
            self.valid_data,
            follow=True,
        )

        # Check that one transaction was added
        self.assertEqual(1, FinancialTransaction.objects.count())

        # Check that one item was added
        self.assertEqual(1, Item.objects.count())

        # Check that item was associated with the transaction
        self.assertEqual(1, FinancialTransaction.objects.first().items.count())

        # Check that financial code matches were added
        self.assertEqual(2, FinancialCodeMatch.objects.count())

        # Check that financial code match entries are associated with item
        self.assertEqual(2, Item.objects.first().financialcodematch_set.count())

class FinancialTransactionEditTest(TestCase):
    """Tests for the edit view"""

    def setUp(self):
        create_user()

        transactions = create_financial_transactions()
        transaction = transactions[0]
        items = transaction.items.all().order_by("id")
        item_1_codes = items[0].financialcodematch_set.all().order_by("id")
        item_2_codes = items[1].financialcodematch_set.all().order_by("id")

        self.valid_data = {
            "payee_payer": transaction.payee_payer.id,
            "memo": transaction.memo,
            "date_submitted": transaction.date_submitted,
            "items-0-id": items[0].id,
            "items-0-transaction": transaction.id,
            "items-0-date_item": items[0].date_item,
            "items-0-description": items[0].description,
            "items-0-amount": items[0].amount,
            "items-0-gst": items[0].gst,
            "items-0-coding_set-0-financial_code_match_id": item_1_codes[0].id,
            "items-0-coding_set-0-budget_year": item_1_codes[0].financial_code.financial_code_group.budget_year.id,
            "items-0-coding_set-0-code": item_1_codes[0].financial_code.id,
            "items-0-coding_set-1-financial_code_match_id": item_1_codes[1].id,
            "items-0-coding_set-1-budget_year": item_1_codes[1].financial_code.financial_code_group.budget_year.id,
            "items-0-coding_set-1-code": item_1_codes[1].financial_code.id,
            "items-1-id": items[1].id,
            "items-1-transaction": transaction.id,
            "items-1-date_item": items[1].date_item,
            "items-1-description": items[1].description,
            "items-1-amount": items[1].amount,
            "items-1-gst": items[1].gst,
            "items-1-coding_set-0-financial_code_match_id": item_2_codes[0].id,
            "items-1-coding_set-0-budget_year": item_2_codes[0].financial_code.financial_code_group.budget_year.id,
            "items-1-coding_set-0-code": item_2_codes[0].financial_code.id,
            "items-1-coding_set-1-financial_code_match_id": item_2_codes[1].id,
            "items-1-coding_set-1-budget_year": item_2_codes[1].financial_code.financial_code_group.budget_year.id,
            "items-1-coding_set-1-code": item_2_codes[1].financial_code.id,
            "items-TOTAL_FORMS": 2,
            "items-INITIAL_FORMS": 2,
            "items-MIN_NUM_FORMS": 1,
            "items-MAX_NUM_FORMS": 1000,
            "financialtransactionmatch_set-TOTAL_FORMS": 0,
            "financialtransactionmatch_set-INITIAL_FORMS": 0,
            "financialtransactionmatch_set-MIN_NUM_FORMS": 0,
            "financialtransactionmatch_set-MAX_NUM_FORMS": 20,
        }
        self.valid_args = {"t_type": "expense", "transaction_id": transaction.id}
        self.valid_url = "/transactions/expense/edit/{}".format(transaction.id)

    def test_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_transactions:edit", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_edit_no_redirect_if_logged_in(self):
        """Checks user is not redirected if logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_transactions:edit", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_edit_url_exists_at_desired_location(self):
        """Checks that the edit page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_edit_html404_on_invalid_name(self):
        """Checks that edit page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse(
                "financial_transactions:edit",
                kwargs={"t_type": "expense", "transaction_id": 999999999}
            )
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_transactions:edit", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "transactions/add_edit.html")

    def test_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Setup the edited data
        edited_data = self.valid_data
        edited_data["date_submitted"] = "2017-12-01"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_transactions:edit", kwargs=self.valid_args),
            edited_data,
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_transactions:dashboard"))

class FinancialTransactionDeleteTest(TestCase):
    """Tests for the delete view"""

    def setUp(self):
        create_user()

        transactions = create_financial_transactions()
        transaction = transactions[0]

        self.valid_args = {"t_type": "expense", "transaction_id": transaction.id}
        self.valid_url = "/transactions/expense/delete/{}".format(transaction.id)

    def test_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_transactions:delete", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_delete_no_redirect_if_logged_in(self):
        """Checks user is not redirected if logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_transactions:delete", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_delete_url_exists_at_desired_location(self):
        """Checks that the delete page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_delete_accessible_by_name(self):
        """Checks that delete page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_transactions:delete", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_delete_html404_on_invalid_name(self):
        """Checks that delete page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse(
                "financial_transactions:delete",
                kwargs={"t_type": "expense", "transaction_id": 999999999}
            )
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_transactions:delete", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "transactions/delete.html")

    def test_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("financial_transactions:delete", kwargs=self.valid_args),
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_transactions:dashboard"))
