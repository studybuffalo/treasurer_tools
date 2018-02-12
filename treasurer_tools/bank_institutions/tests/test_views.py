"""Test cases for the bank_institution app views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from bank_institutions.models import Institution, Account

from .utils import create_user, create_bank_account


class BankDashboardTest(TestCase):
    """Test functions for the BankSettings dashboard"""
    def setUp(self):
        create_user()

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
        response = self.client.get(reverse("bank_institutions:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_institutions:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "bank_institutions/index.html")

class InstitutionAddTest(TestCase):
    """Tests for the institution_add view"""

    def setUp(self):
        create_user()

        self.valid_data = {
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
        response = self.client.get(reverse("bank_institutions:add"))

        self.assertEqual(response.status_code, 302)

    def test_institution_add_noredirect_if_logged_in(self):
        """Checks that user is not redirected if logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_institutions:add"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that 200 status code returned (i.e. no redirect)
        self.assertEqual(response.status_code, 200)

    def test_institution_add_url_exists_at_desired_location(self):
        """Checks that the add institution page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/banking/institution/add/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_institution_add_accessible_by_name(self):
        """Checks that add institution page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_institutions:add"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_institution_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_institutions:add"))

        # Check for proper template
        self.assertTemplateUsed(response, "bank_institutions/add.html")

    def test_institution_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_institutions:add"),
            self.valid_data,
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_institutions:dashboard"))

    def test_institution_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        # Get current count of institutions and accounts
        institution_total = Institution.objects.count()
        account_total = Account.objects.count()

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_institutions:add"),
            self.valid_data,
            follow=True,
        )

        # Check that one institution was added
        self.assertEqual(
            Institution.objects.count(),
            institution_total + 1
        )

        # Check that one account was added
        self.assertEqual(
            Account.objects.count(),
            account_total + 1
        )

    def test_institution_add_invalid_institution_data(self):
        """Confirms form data returned on invalid institution data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["name"] = ""
        
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_institutions:add"),
            invalid_data,
            follow=True,
        )

        # Check that institution data returned
        institution_form = response.context["form"]

        self.assertEqual(
            institution_form["name"].value(),
            invalid_data["name"]
        )

        self.assertEqual(
            institution_form["address"].value(),
            invalid_data["address"]
        )

        # Check that account data returned
        account_formset = response.context["formsets"]

        self.assertEqual(
            account_formset[0]["account_number"].value(),
            invalid_data["account_set-0-account_number"]
        )

    def test_institution_add_invalid_account_data(self):
        """Confirms form data returned on invalid account data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["account_set-0-name"] = ""
        
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_institutions:add"),
            invalid_data,
            follow=True,
        )

        # Check that institution data returned
        institution_form = response.context["form"]

        self.assertEqual(
            institution_form["name"].value(),
            invalid_data["name"]
        )

        # Check that account data returned
        account_formset = response.context["formsets"]

        self.assertEqual(
            account_formset[0]["account_number"].value(),
            invalid_data["account_set-0-account_number"]
        )
        
        self.assertEqual(
            account_formset[0]["name"].value(),
            invalid_data["account_set-0-name"]
        )

class InstitutionEditTest(TestCase):
    """Tests of the edit Institution form page"""

    def setUp(self):
        # Create a user
        create_user()

        # Create entries for both models
        account = create_bank_account()
        institution = account.institution

        # Populate the valid data
        self.valid_data = {
            "name": institution.name,
            "address": institution.address,
            "phone": institution.phone,
            "fax": institution.fax,
            "account_set-0-account_number": account.account_number,
            "account_set-0-name": account.name,
            "account_set-0-status": account.status,
            "account_set-0-id": account.id,
            "account_set-TOTAL_FORMS": 1,
            "account_set-INITIAL_FORMS": 1,
            "account_set-MIN_NUM_FORMS": 1,
            "account_set-MAX_NUM_FORMS": 1000,
        }
        self.account = account
        self.institution = institution
        self.url = "/settings/banking/institution/edit/{}".format(institution.id)
        self.url_args = {"institution_id": institution.id}

    def test_institution_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("bank_institutions:edit", kwargs=self.url_args))

        self.assertEqual(response.status_code, 302)

    def test_institution_edit_noredirect_if_logged_in(self):
        """Checks that user is not redirected if logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_institutions:edit", kwargs=self.url_args))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that 200 status code returned (i.e. no redirect)
        self.assertEqual(response.status_code, 200)

    def test_institution_edit_url_exists_at_desired_location(self):
        """Checks that the edit institution page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_institution_edit_html404_on_invalid_url(self):
        """Checks that the edit institution page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/banking/institution/edit/999999999")

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_institution_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("bank_institutions:edit", kwargs=self.url_args))

        # Check for proper template
        self.assertTemplateUsed(response, "bank_institutions/edit.html")

    def test_institution_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_institutions:edit", kwargs=self.url_args),
            self.valid_data,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_institutions:dashboard"))

    def test_institution_edit_post_failed_on_invalid_institution_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_institutions:edit", kwargs={"institution_id": 999999999}),
            self.valid_data,
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_institution_edit_post_account_addition(self):
        """Confirms an account can be added"""
        # Count current accounts
        accounts_total = Account.objects.count()

        # Setup form data
        edited_data = self.valid_data
        edited_data["account_set-1-account_number"] = "222222222"
        edited_data["account_set-1-name"] = "TFSA Account"
        edited_data["account_set-1-status"] = "a"
        edited_data["account_set-TOTAL_FORMS"] = 2

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("bank_institutions:edit", kwargs=self.url_args),
            edited_data,
            follow=True,
        )

        # Confirm addition of account
        self.assertEqual(
            Account.objects.count(),
            accounts_total + 1
        )

    def test_institution_edit_post_delete_account(self):
        """Checks that account is deleted via the edit institution form"""
        # Add an extra entry to Account
        new_account = Account.objects.create(
            institution=self.institution,
            account_number="222222222",
            name="TFSA Account",
            status="a",
        )

        # Count current accounts
        accounts_total = Account.objects.count()

        # Setup form data
        delete_data = self.valid_data
        delete_data["account_set-0-DELETE"] = "on"
        delete_data["account_set-1-account_number"] = "222222222"
        delete_data["account_set-1-name"] = "TFSA Account"
        delete_data["account_set-1-status"] = "a"
        delete_data["account_set-1-id"] = new_account.id
        delete_data["account_set-TOTAL_FORMS"] = 2
        delete_data["account_set-INITIAL_FORMS"] = 2

        # Make the post request
        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("bank_institutions:edit", kwargs=self.url_args),
            delete_data,
            follow=True,
        )
        
        # Confirm deletion of account
        self.assertEqual(
            Account.objects.count(),
            accounts_total - 1
        )

        # Confirm proper account was deleted
        self.assertFalse(Account.objects.filter(id=self.account.id).count())

    def test_institution_edit_post_no_account(self):
        """Checks that edit fails if no accounts saved"""
        # Count current accounts
        accounts_total = Account.objects.count()

        # Setup form data
        delete_data = self.valid_data
        delete_data["account_set-0-DELETE"] = "on"
        
        # Make the post request
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_institutions:edit", kwargs=self.url_args),
            delete_data,
        )

        # Confirm 200 status code (rather than 302)
        self.assertEqual(response.status_code, 200)

        # Confirm no change in account number
        self.assertEqual(Account.objects.count(), accounts_total)

    def test_institution_edit_invalid_institution_data(self):
        """Tests that updates fail on invalid institution data"""
        
        # Setup form data
        invalid_data = self.valid_data
        invalid_data["name"] = ""
        
        # Make the post request
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("bank_institutions:edit", kwargs=self.url_args),
            invalid_data,
        )

        # Confirm 200 status code (rather than 302)
        self.assertEqual(response.status_code, 200)

class InstitutionDeleteTest(TestCase):
    """Tests the delete institution view"""

    def setUp(self):
        # Create a user
        create_user()

        # Create entries for the institution and accounts
        account = create_bank_account()
        institution = account.institution

        self.institution = institution
        self.url = "/settings/banking/institution/delete/{}".format(institution.id)
        self.url_args = {"institution_id": institution.id}

    def test_institution_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("bank_institutions:delete", kwargs=self.url_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_institution_delete_url_exists_at_desired_location(self):
        """Checks that the delete institution page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.url)

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
            reverse("bank_institutions:delete", kwargs=self.url_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_institution_delete_html404_on_invalid_name(self):
        """Checks that delete institution page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("bank_institutions:delete", kwargs={"institution_id": 999999999})
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_institution_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("bank_institutions:delete", kwargs=self.url_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "bank_institutions/delete.html")

    def test_institution_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("bank_institutions:delete", kwargs=self.url_args)
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_institutions:dashboard"))

    def test_institution_delete_post_failed_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("bank_institutions:delete", kwargs={"institution_id": 999999999}),
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_institution_delete_confirm_delete(self):
        """Confirms deletion form works properly"""
        institution_total = Institution.objects.count()
        account_total = Account.objects.count()

        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse("bank_institutions:delete", kwargs=self.url_args)
        )

        # Checks that institution was deleted
        self.assertEqual(
            Institution.objects.count(),
            institution_total - 1
        )

        # Checks that accounts were deleted
        self.assertEqual(
            Account.objects.count(),
            account_total -1
        )
