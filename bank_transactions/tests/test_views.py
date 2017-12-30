"""Test cases for the bank_transactions app views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from bank_transactions.models import Institution, Account

class BankSettingsTest(TestCase):
    """Test functions for the BankSettings dashboard"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
    ]

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get("/settings/banking/")

        self.assertRedirects(response, "/accounts/login/?next=/settings/banking/")

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/banking/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_settings"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_settings"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "bank_settings/index.html")

class InstitutionAddTest(TestCase):
    """Tests for the institution_add view"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
    ]
    
    def setUp(self):
        self.CORRECT_FORM_DATA = {
            "name": "Another Financial Institution",
            "address": "444 Test Boulevard\nRich City $$ T1T 1T1",
            "phone": "111-222-1234",
            "fax": "222-111-1111",
            "account_set-0-account_number": "777888999",
            "account_set-0-name": "Savings Account",
            "account_set-0-status": "a",
            "account_set-TOTAL_FORMS": 1,
            "account_set-INITIAL_FORMS": 0,
            "account_set-MIN_NUM_FORMS": 1,
            "account_set-MAX_NUM_FORMS": 1000,
        }

    def test_institution_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("institution_add"))

        self.assertEqual(response.status_code, 302)

    def test_institution_add_url_exists_at_desired_location(self):
        """Checks that the add institution page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/banking/institution/add/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_institution_add_accessible_by_name(self):
        """Checks that add institution page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("institution_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_institution_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("institution_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "bank_settings/add.html")

    def test_institution_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("institution_add"), self.CORRECT_FORM_DATA, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_settings"))

    def test_institution_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("institution_add"), self.CORRECT_FORM_DATA, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one institution was added
        self.assertEqual(2, Institution.objects.count())

        # Check that one account was added
        self.assertEqual(3, Account.objects.count())
        
    def test_institution_add_invalid_account_status(self):
        """Confirms that incorrect statuses are properly converted to 'a'"""
        # Setup incorrect data
        incorrect_data = self.CORRECT_FORM_DATA
        incorrect_data["account_set-0-status"] = "z"

        # Submit form
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("institution_add"), incorrect_data, follow=True,
        )
        
        # Confirm that new entry has been added properly
        self.assertEqual(Account.objects.get(id=1).status, "a")

class InstitutionEditTest(TestCase):
    """Tests of the edit Institution form page"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
    ]
       
    def setUp(self):
        # Add standard test data
        self.CORRECT_FORM_DATA = {
            "name": "Another Financial Institution",
            "address": "444 Test Boulevard\nRich City $$ T1T 1T1",
            "phone": "111-222-1234",
            "fax": "222-111-1111",
            "account_set-0-account_number": "777888999",
            "account_set-0-name": "Savings Account",
            "account_set-0-status": "a",
            "account_set-0-id": 1,
            "account_set-1-account_number": "333333333",
            "account_set-1-name": "Embezzlement Account",
            "account_set-1-status": "a",
            "account_set-1-id": 2,
            "account_set-TOTAL_FORMS": 2,
            "account_set-INITIAL_FORMS": 0,
            "account_set-MIN_NUM_FORMS": 1,
            "account_set-MAX_NUM_FORMS": 1000,
        }

    def test_institution_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("institution_edit", kwargs={"institution_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_institution_edit_url_exists_at_desired_location(self):
        """Checks that the edit institution page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/banking/institution/edit/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_institution_edit_html404_on_invalid_url(self):
        """Checks that the edit institution page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/banking/institution/edit/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_institution_edit_accessible_by_name(self):
        """Checks that edit institution page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("institution_edit", kwargs={"institution_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_institution_edit_html404_on_invalid_name(self):
        """Checks that edit institution page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("institution_edit", kwargs={"institution_id": 999999999})
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_institution_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("institution_edit", kwargs={"institution_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "bank_settings/edit.html")
        
    def test_institution_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("institution_edit", kwargs={"institution_id": 1}),
            {
                "name": "Another Financial Institution 2",
                "address": "444 Test Boulevard\nRich City $$ T1T 1T1",
                "phone": "111-222-1234",
                "fax": "222-111-1111",
                "account_set-0-account_number": "777888999",
                "account_set-0-name": "Savings Account",
                "account_set-0-status": "a",
                "account_set-0-id": 1,
                "account_set-TOTAL_FORMS": 1,
                "account_set-INITIAL_FORMS": 0,
                "account_set-MIN_NUM_FORMS": 1,
                "account_set-MAX_NUM_FORMS": 1000,
            },
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_settings"))

    def test_institution_edit_post_failed_on_invalid_institution_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("institution_edit", kwargs={"institution_id": 999999999}),
            {
                "name": "Another Financial Institution 2",
                "address": "444 Test Boulevard\nRich City $$ T1T 1T1",
                "phone": "111-222-1234",
                "fax": "222-111-1111",
                "account_set-0-account_number": "777888999",
                "account_set-0-name": "Savings Account",
                "account_set-0-status": "a",
                "account_set-0-id": 1,
                "account_set-TOTAL_FORMS": 1,
                "account_set-INITIAL_FORMS": 0,
                "account_set-MIN_NUM_FORMS": 1,
                "account_set-MAX_NUM_FORMS": 1000,
            },
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)
        
    def test_institution_edit_post_confirm_institution_edit(self):
        """Confirms account is properly edited via the institution edit form"""
        # Setup edited data
        edited_data = self.CORRECT_FORM_DATA
        edited_data["name"] = "Another Financial Institution 2"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("institution_edit", kwargs={"institution_id": 1}),
            edited_data
        )

        # Confirm still only 1 entry
        self.assertEqual(1, Institution.objects.count())

        # Confirm name has been updated properly
        self.assertEqual(
            Institution.objects.get(id=1).name,
            "Another Financial Institution 2"
        )

    def test_institution_edit_post_confirm_account_edit(self):
        """Confirms deletion form works properly"""
        edited_data = self.CORRECT_FORM_DATA
        edited_data["account_set-0-account_number"] = "222222222"
        edited_data["account_set-0-name"] = "TFSA Account"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("institution_edit", kwargs={"institution_id": 1}),
            edited_data
        )

        # Confirm still only 2 entrries
        self.assertEqual(2, Account.objects.count())

        # Confirm account number has been updated properly
        self.assertEqual(
            Account.objects.get(id=1).account_number,
            "222222222"
        )

        # Confirm name has been updated properly
        self.assertEqual(
            Account.objects.get(id=1).name,
            "TFSA Account"
        )

    def test_institution_edit_post_fail_on_invalid_account_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Setup edited data
        edited_data = self.CORRECT_FORM_DATA
        edited_data["account_set-0-id"] = "999999999"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("institution_edit", kwargs={"institution_id": 1}),
            edited_data
        )

        # Check for the expected ValidationError
        self.assertEqual(
            response.context["formsets"][0].errors["id"][0],
            "Select a valid choice. That choice is not one of the available choices."
        )
        
    def test_institution_edit_post_add_account(self):
        """Checks that a new account is added via the edit institution form"""
        added_data = self.CORRECT_FORM_DATA
        added_data["account_set-2-account_number"] = "444444444"
        added_data["account_set-2-name"] = "Charity Account"
        added_data["account_set-2-status"] = "a"
        added_data["account_set-2-id"] = ""
        added_data["account_set-TOTAL_FORMS"] = 3

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("institution_edit", kwargs={"institution_id": 1}),
            added_data
        )

        # Check that the number of accounts has increased
        self.assertEqual(
            Account.objects.count(),
            3
        )

        # Check that original accounts still exist
        self.assertEqual(
            Account.objects.get(id=1).name,
            "Savings Account"
        )

        self.assertEqual(
            Account.objects.get(id=2).name,
            "Embezzlement Account"
        )

        # Check that the new account was saved properly
        self.assertEqual(
            Account.objects.get(id=3).name,
            "Charity Account"
        )

    def test_institution_edit_post_delete_account(self):
        """Checks that account is deleted via the edit institution form"""
        # Setup the delete data
        delete_data = self.CORRECT_FORM_DATA
        delete_data["account_set-1-DELETE"] = "on"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("institution_edit", kwargs={"institution_id": 1}),
            delete_data
        )
        
        # Check that the number of accounts has decreased
        self.assertEqual(
            Account.objects.count(),
            1
        )

        # Check that the proper ID has been removed
        self.assertEqual(
            Account.objects.filter(id=2).count(),
            0
        )
        
    def test_institution_add_invalid_account_status(self):
        """Confirms that incorrect statuses are properly converted to 'a'"""
        # Setup incorrect data
        incorrect_data = self.CORRECT_FORM_DATA
        incorrect_data["account_set-0-status"] = "z"

        # Submit form
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("institution_edit", kwargs={"institution_id": 1}),
            incorrect_data, follow=True,
        )
        
        # Confirm that new entry has been added properly
        self.assertEqual(Account.objects.get(id=1).status, "a")

class InstitutionDeleteTest(TestCase):
    """Tests the delete institution view"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
    ]
    
    def test_institution_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("institution_delete", kwargs={"institution_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_institution_delete_url_exists_at_desired_location(self):
        """Checks that the delete institution page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/banking/institution/delete/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_institution_delete_html404_on_invalid_url(self):
        """Checks that the delete institution page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/banking/institution/delete/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_institution_delete_accessible_by_name(self):
        """Checks that delete institution page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("institution_delete", kwargs={"institution_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_institution_delete_html404_on_invalid_name(self):
        """Checks that delete institution page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("institution_delete", kwargs={"institution_id": 999999999})
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_institution_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("institution_delete", kwargs={"institution_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "bank_settings/delete.html")
        
    def test_institution_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("institution_delete", kwargs={"institution_id": 1}),
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_settings"))

    def test_institution_delete_post_failed_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("institution_delete", kwargs={"institution_id": 999999999}),
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_institution_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse("institution_delete", kwargs={"institution_id": 1})
        )

        # Checks that institution was deleted
        self.assertEqual(0, Institution.objects.filter(id=1).count())

        # Checks that accounts were deleted
        self.assertEqual(0, Account.objects.count())

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

class StatementEditTest(TestCase):
    """Tests for the edit statement view"""

class StatementDeleteTest(TestCase):
    """Tests for the delete statement view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
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
