"""Test cases for the payee_payer app"""

from django.urls import reverse
from django.test import TestCase

from payee_payers.models import PayeePayer

from .utils import create_user, create_country, create_demographics


class DashboardTest(TestCase):
    """Test functions for the Payee/Payer model"""

    def setUp(self):
        create_user()

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(reverse("payee_payers:dashboard"))

        self.assertRedirects(response, "/accounts/login/?next=/payee-payer/")

    def test_dashboard_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("payee_payers:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/payee-payer/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("payee_payers:dashboard"))

        # Check for proper template
        self.assertTemplateUsed(response, "payee_payers/index.html")

class RetrieveListTest(TestCase):
    """Test functions for the Payee/Payer model"""

    def setUp(self):
        create_user()
        create_demographics()

    def test_retrieve_list_redirect_if_not_logged_in(self):
        """Checks that request is redirected if user is not logged in"""
        response = self.client.get("/payee-payer/retrieve-payee-payer-list/")

        self.assertEqual(response.status_code, 302)

    def test_retrieve_list_no_redirect_if_logged_in(self):
        """Checks that request is redirected if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/payee-payer/retrieve-payee-payer-list/")

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that response is correct
        self.assertEqual(response.status_code, 200)

    def test_retrieve_list_all_entries(self):
        """Checks that all payee_payer entries are retrieved"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/payee-payer/retrieve-payee-payer-list/")

        # Check that the number of retrieved entries matches the DB
        db_count = PayeePayer.objects.all().count()
        context_count = len(response.context['payee_payer_list'])

        self.assertEqual(db_count, context_count)

    def test_retrieve_list_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/payee-payer/retrieve-payee-payer-list/")

        # Check for proper template
        self.assertTemplateUsed(response, "payee_payers/payee_payer_list.html")

class PayeePayerAddTest(TestCase):
    """Tests of the add payee/payer form page"""

    def setUp(self):
        create_user()

        country = create_country()

        self.valid_data = {
            "user": None,
            "name": "Another Test User",
            "address": "111-222 Fake Street",
            "city": "Edmonton",
            "province": "Alberta",
            "country": country.id,
            "postal_code": "T1T 1T1",
            "phone": "111-222-3333",
            "fax": "444-555-6666",
            "email": "test@email.com",
            "status": "a"
        }

    def test_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("payee_payers:add"))

        self.assertEqual(response.status_code, 302)

    def test_add_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("payee_payers:add"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_add_url_exists_at_desired_location(self):
        """Checks that the add page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/payee-payer/add/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("payee_payers:add"))

        # Check for proper template
        self.assertTemplateUsed(response, "payee_payers/add_edit.html")

    def test_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("payee_payers:add"), self.valid_data, follow=True
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("payee_payers:dashboard"))

    def test_add_saves_to_database(self):
        """Checks that form can properly save to database"""
        # Get current total of payee_payers
        payee_payer_total = PayeePayer.objects.count()

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("payee_payers:add"), self.valid_data, follow=True,
        )

        # Check that one entry is added
        self.assertEqual(PayeePayer.objects.count(), payee_payer_total + 1)

class PayeePayerEditTest(TestCase):
    """Tests of the edit payee/payer form page"""

    def setUp(self):
        create_user()

        country = create_country()
        payee_payer = create_demographics()

        self.current_data = {
            "user": payee_payer.user,
            "name": payee_payer.name,
            "address": payee_payer.address,
            "city": payee_payer.city,
            "province": payee_payer.province,
            "country": payee_payer.country.id,
            "postal_code": payee_payer.postal_code,
            "phone": payee_payer.phone,
            "fax": payee_payer.fax,
            "email": payee_payer.email,
            "status": payee_payer.status,
        }
        self.new_data = {
            "user": None,
            "name": "Another Test User",
            "address": "New Address",
            "city": "Edmonton",
            "province": "Alberta",
            "country": country.id,
            "postal_code": "T1T 1T1",
            "phone": "111-222-3333",
            "fax": "444-555-6666",
            "email": "test@email.com",
            "status": "a"
        }
        self.valid_args = {"payee_payer_id": payee_payer.id}
        self.valid_url = "/payee-payer/edit/{}".format(payee_payer.id)

    def test_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("payee_payers:edit", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_edit_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("payee_payers:edit", kwargs=self.valid_args)
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
        """Checks that edit payee/payer page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("payee_payers:edit", kwargs={"payee_payer_id": 999999999})
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("payee_payers:edit", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "payee_payers/add_edit.html")

    def test_payee_payer_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("payee_payers:edit", kwargs=self.valid_args),
            self.current_data,
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("payee_payers:dashboard"))

    def test_edit_confirm_edit(self):
        """Confirms deletion form works properly"""
        # Get current number of entries
        payee_payer_total = PayeePayer.objects.count()

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("payee_payers:edit", kwargs=self.valid_args),
            self.new_data
        )

        # Confirm still only 1 entry
        self.assertEqual(PayeePayer.objects.count(), payee_payer_total)

        # Confirm name has been updated properly
        self.assertEqual(
            PayeePayer.objects.last().name,
            self.new_data["name"]
        )

class PayeePayerDeleteTest(TestCase):
    """Tests of the delete payee/payer form page"""

    def setUp(self):
        create_user()
        payee_payer = create_demographics()

        self.valid_args = {"payee_payer_id": payee_payer.id}
        self.valid_url = "/payee-payer/delete/{}".format(payee_payer.id)

    def test_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("payee_payers:delete", kwargs={"payee_payer_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_delete_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("payee_payers:delete", kwargs=self.valid_args)
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

    def test_delete_html404_on_invalid_name(self):
        """Checks that delete page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("payee_payers:delete", kwargs={"payee_payer_id": 999999999})
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("payee_payers:delete", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "payee_payers/delete.html")

    def test_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("payee_payers:delete", kwargs=self.valid_args),
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("payee_payers:dashboard"))

    def test_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Get current totals
        payee_payer_total = PayeePayer.objects.count()

        # Delete entry
        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("payee_payers:delete", kwargs=self.valid_args)
        )

        # Checks that payee/payer was deleted
        self.assertEqual(PayeePayer.objects.count(), payee_payer_total - 1)
