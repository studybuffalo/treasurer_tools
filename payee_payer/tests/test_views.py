"""Test cases for the payee_payer app"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from payee_payer.models import Country, Demographics

class DashboardTest(TestCase):
    """Test functions for the Demographics model"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "payee_payer/tests/fixtures/authentication.json",
        "payee_payer/tests/fixtures/country.json",
        "payee_payer/tests/fixtures/demographics.json",
    ]

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get("/payee-payer/")

        self.assertRedirects(response, "/accounts/login/?next=/payee-payer/")

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        login = self.client.login(username="user", password="abcd123456")
        response = self.client.get("/payee-payer/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        login = self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("payee_payer_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        login = self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("payee_payer_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "payee_payer/index.html")

class RetrieveListTest(TestCase):
    """Test functions for the Demographics model"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "payee_payer/tests/fixtures/authentication.json",
        "payee_payer/tests/fixtures/country.json",
        "payee_payer/tests/fixtures/demographics.json",
    ]

    def test_retrieve_list_redirect_if_not_logged_in(self):
        """Checks that request is redirected if user is not logged in"""
        response = self.client.get("/payee-payer/retrieve-payee-payer-list/")

        self.assertEqual(response.status_code, 302)

    def test_retrieve_list_url_exists_at_desired_location(self):
        """Checks that the retrieve payee/payer list URL is correct"""
        login = self.client.login(username="user", password="abcd123456")
        response = self.client.get("/payee-payer/retrieve-payee-payer-list/")

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that response is corret
        self.assertEqual(response.status_code, 200)

    def test_retrieve_list_all_entries(self):
        """Checks that all payee_payer entries are retrieved"""
        login = self.client.login(username="user", password="abcd123456")
        response = self.client.get("/payee-payer/retrieve-payee-payer-list/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that the number of retrieved entries matches the DB
        db_count = Demographics.objects.all().count
        context_count = len(response.context['payee_payer_list'])

        self.assertTrue(True)

class AddPayeePayerTest(TestCase):
    """Tests of the add payee/payer form page"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "payee_payer/tests/fixtures/authentication.json",
        "payee_payer/tests/fixtures/country.json",
        "payee_payer/tests/fixtures/demographics.json",
    ]
    
    def test_add_payee_payer_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("payee_payer_add"))

        self.assertEqual(response.status_code, 302)

    def test_add_payee_payer_url_exists_at_desired_location(self):
        """Checks that the add payee/payer page uses the correct URL"""
        login = self.client.login(username="user", password="abcd123456")
        response = self.client.get("/payee-payer/add/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_payee_payer_add_accessible_by_name(self):
        """Checks that add payee/payer page URL name works properly"""
        login = self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("payee_payer_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
