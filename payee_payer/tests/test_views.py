"""Test cases for the bank_transactions app views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from bank_transactions.models import Institution, Account

# from bank_transactions.models import Demographics

class BankSettingsTest(TestCase):
    """Test functions for the BankSettings dashboard"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "bank_transactions/tests/fixtures/authentication.json",
        "bank_transactions/tests/fixtures/institution.json",
        "bank_transactions/tests/fixtures/account.json",
        "bank_transactions/tests/fixtures/statement.json",
        "bank_transactions/tests/fixtures/bank_transaction.json",
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
            reverse("institution_add"),
            {
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
            },
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("bank_settings"))

    def test_institution_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("institution_add"),
            {
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
            },
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one institution was added
        self.assertEqual(2, Institution.objects.count())

        # Check that one account was added
        self.assertEqual(2, Account.objects.count())

#class PayeePayerEditTest(TestCase):
#    """Tests of the edit payee/payer form page"""
#    # pylint: disable=no-member,protected-access

#    fixtures = [
#        "payee_payer/tests/fixtures/authentication.json",
#        "payee_payer/tests/fixtures/country.json",
#        "payee_payer/tests/fixtures/demographics.json",
#    ]

#    def test_payee_payer_edit_redirect_if_not_logged_in(self):
#        """Checks user is redirected if not logged in"""
#        response = self.client.get(
#            reverse("payee_payer_edit", kwargs={"payee_payer_id": 1})
#        )

#        self.assertEqual(response.status_code, 302)

#    def test_payee_payer_edit_url_exists_at_desired_location(self):
#        """Checks that the edit payee/payer page uses the correct URL"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.get("/payee-payer/edit/1")
        
#        # Check that user logged in
#        self.assertEqual(str(response.context['user']), 'user')

#        # Check that page is accessible
#        self.assertEqual(response.status_code, 200)

#    def test_payee_payer_edit_html404_on_invalid_url(self):
#        """Checks that the edit payee/payer page URL fails on invalid ID"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.get("/payee-payer/edit/999999999")
        
#        # Check that page is accessible
#        self.assertEqual(response.status_code, 404)

#    def test_payee_payer_edit_accessible_by_name(self):
#        """Checks that edit payee/payer page URL name works properly"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.get(
#            reverse("payee_payer_edit", kwargs={"payee_payer_id": 1})
#        )
        
#        # Check that user logged in
#        self.assertEqual(str(response.context['user']), 'user')

#        # Check that page is accessible
#        self.assertEqual(response.status_code, 200)
        
#    def test_payee_payer_edit_html404_on_invalid_name(self):
#        """Checks that edit payee/payer page URL name failed on invalid ID"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.get(
#            reverse("payee_payer_edit", kwargs={"payee_payer_id": 999999999})
#        )
        
#        # Check that page is accessible
#        self.assertEqual(response.status_code, 404)

#    def test_payee_payer_edit_template(self):
#        """Checks that correct template is being used"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.get(
#            reverse("payee_payer_edit", kwargs={"payee_payer_id": 1})
#        )
        
#        # Check that user logged in
#        self.assertEqual(str(response.context['user']), 'user')
        
#        # Check for proper template
#        self.assertTemplateUsed(response, "payee_payer/edit.html")
        
#    def test_payee_payer_edit_redirect_to_dashboard(self):
#        """Checks that form redirects to the dashboard on success"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.post(
#            reverse("payee_payer_edit", kwargs={"payee_payer_id": 1}),
#            {
#                "name": "Test Case Company - 2",
#                "address": "444 Test Boulevard",
#                "country": 1,
#                "province": "British Columbia",
#                "city": "Vancouver",
#                "postal_code": "V1V 1V12",
#                "phone": "111-111-1111",
#                "fax": "222-222-2222",
#                "email": "testcase@email.com",
#                "status": "a",
#            },
#            follow=True,
#        )

#        # Check that user logged in
#        self.assertEqual(str(response.context['user']), 'user')
        
#        # Check that redirection was successful
#        self.assertRedirects(response, reverse("payee_payer_dashboard"))

#    def test_payee_payer_edit_post_failed_on_invalid_id(self):
#        """Checks that a POST fails when an invalid ID is provided"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.post(
#            reverse("payee_payer_edit", kwargs={"payee_payer_id": 999999999}),
#            {
#                "name": "Test Case Company - 3",
#                "address": "444 Test Boulevard",
#                "country": 1,
#                "province": "British Columbia",
#                "city": "Vancouver",
#                "postal_code": "V1V 1V12",
#                "phone": "111-111-1111",
#                "fax": "222-222-2222",
#                "email": "testcase@email.com",
#                "status": "a",
#            },
#            follow=True,
#        )

#        # Check that page is accessible
#        self.assertEqual(response.status_code, 404)
        
#    def test_payee_payer_edit_confirm_edit(self):
#        """Confirms deletion form works properly"""
#        self.client.login(username="user", password="abcd123456")
#        self.client.post(
#            reverse("payee_payer_edit", kwargs={"payee_payer_id": 1}),
#            {
#                "name": "Test Case Company - 2",
#                "address": "444 Test Boulevard",
#                "country": 1,
#                "province": "British Columbia",
#                "city": "Vancouver",
#                "postal_code": "V1V 1V12",
#                "phone": "111-111-1111",
#                "fax": "222-222-2222",
#                "email": "testcase@email.com",
#                "status": "a",
#            },
#        )

#        # Confirm still only 1 entry
#        self.assertEqual(1, Demographics.objects.count())

#        # Confirm name has been updated properly
#        self.assertEqual(
#            Demographics.objects.get(id=1).name,
#            "Test Case Company - 2"
#        )

#class PayeePayerDeleteTest(TestCase):
#    """Tests of the delete payee/payer form page"""
#    # pylint: disable=no-member,protected-access

#    fixtures = [
#        "payee_payer/tests/fixtures/authentication.json",
#        "payee_payer/tests/fixtures/country.json",
#        "payee_payer/tests/fixtures/demographics.json",
#    ]

#    def test_payee_payer_delete_redirect_if_not_logged_in(self):
#        """Checks user is redirected if not logged in"""
#        response = self.client.get(
#            reverse("payee_payer_delete", kwargs={"payee_payer_id": 1})
#        )

#        self.assertEqual(response.status_code, 302)

#    def test_payee_payer_delete_url_exists_at_desired_location(self):
#        """Checks that the delete payee/payer page uses the correct URL"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.get("/payee-payer/delete/1")
        
#        # Check that user logged in
#        self.assertEqual(str(response.context['user']), 'user')

#        # Check that page is accessible
#        self.assertEqual(response.status_code, 200)

#    def test_payee_payer_delete_html404_on_invalid_url(self):
#        """Checks that the delete payee/payer page URL fails on invalid ID"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.get("/payee-payer/delete/999999999")
        
#        # Check that page is accessible
#        self.assertEqual(response.status_code, 404)

#    def test_payee_payer_delete_accessible_by_name(self):
#        """Checks that delete payee/payer page URL name works properly"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.get(
#            reverse("payee_payer_delete", kwargs={"payee_payer_id": 1})
#        )
        
#        # Check that user logged in
#        self.assertEqual(str(response.context['user']), 'user')

#        # Check that page is accessible
#        self.assertEqual(response.status_code, 200)
        
#    def test_payee_payer_delete_html404_on_invalid_name(self):
#        """Checks that delete payee/payer page URL name failed on invalid ID"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.get(
#            reverse("payee_payer_delete", kwargs={"payee_payer_id": 999999999})
#        )
        
#        # Check that page is accessible
#        self.assertEqual(response.status_code, 404)

#    def test_payee_payer_delete_template(self):
#        """Checks that correct template is being used"""
#        self.client.login(username="user", password="abcd123456")
#        response = self.client.get(
#            reverse("payee_payer_delete", kwargs={"payee_payer_id": 1})
#        )
        
#        # Check that user logged in
#        self.assertEqual(str(response.context['user']), 'user')
        
#        # Check for proper template
#        self.assertTemplateUsed(response, "payee_payer/delete.html")
        
#    def test_payee_payer_delete_redirect_to_dashboard(self):
#        """Checks that form redirects to the dashboard on success"""
#        # Login
#        self.client.login(username="user", password="abcd123456")

#        # Delete entry
#        response = self.client.post(
#            reverse("payee_payer_delete", kwargs={"payee_payer_id": 1}),
#            follow=True,
#        )

#        # Check that user logged in
#        self.assertEqual(str(response.context['user']), 'user')
        
#        # Check that redirection was successful
#        self.assertRedirects(response, reverse("payee_payer_dashboard"))

#    def test_payee_payer_edit_post_failed_on_invalid_id(self):
#        """Checks that a POST fails when an invalid ID is provided"""
#        # Login
#        self.client.login(username="user", password="abcd123456")

#        # Delete entry
#        response = self.client.post(
#            reverse("payee_payer_delete", kwargs={"payee_payer_id": 999999999}),
#            follow=True,
#        )

#        # Check that page is accessible
#        self.assertEqual(response.status_code, 404)

#    def test_payee_payer_delete_confirm_deletion(self):
#        """Confirms deletion form works properly"""
#        # Login
#        self.client.login(username="user", password="abcd123456")

#        # Delete entry
#        self.client.post(
#            reverse("payee_payer_delete", kwargs={"payee_payer_id": 1})
#        )

#        self.assertEqual(0, Demographics.objects.filter(id=1).count())
