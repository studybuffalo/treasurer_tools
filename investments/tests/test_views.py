"""Test cases for the investments app views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from investments.models import Investment

class InvestmentsDashboard(TestCase):
    """Tests for the investments dashboard view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "investments/tests/fixtures/authentication.json",
    ]

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get("/investments/")

        self.assertRedirects(response, "/accounts/login/?next=/investments/")

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/investments/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_accessible_by_name(self):
        """Checks that the dashboard URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("investments_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("investments_dashboard"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check for proper template
        self.assertTemplateUsed(response, "investments/index.html")

class InvestmentAddTest(TestCase):
    """Tests for the add investment view"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "investments/tests/fixtures/authentication.json",
    ]
    
    def setUp(self):
        self.correct_data = {
            "name":  "Annual GIC",
            "date_invested": "2017-01-01",
            "amount": 100.00,
            "rate":  "1% annually"
        }
        
    def test_investment_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("investment_add"))

        self.assertEqual(response.status_code, 302)

    def test_investment_add_url_exists_at_desired_location(self):
        """Checks that the add investment page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/investments/add/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_investment_add_accessible_by_name(self):
        """Checks that add investment page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("investment_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_investment_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("investment_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "investments/add.html")

    def test_investment_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("investment_add"), self.correct_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("investments_dashboard"))

    def test_investment_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("investment_add"), self.correct_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one investment was added
        self.assertEqual(1, Investment.objects.count())
    
class InvestmentEditTest(TestCase):
    """Tests for the edit investment view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "investments/tests/fixtures/authentication.json",
        "investments/tests/fixtures/investment.json",
    ]

    def setUp(self):
        # Add standard test data
        self.correct_data = {
            "name":  "Annual GIC",
            "date_invested": "2017-01-01",
            "amount": 100.00,
            "rate":  "1% annually"
        }

    def test_investment_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("investment_edit", kwargs={"investment_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_investment_edit_url_exists_at_desired_location(self):
        """Checks that the edit investment page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/investments/edit/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_investment_edit_html404_on_invalid_url(self):
        """Checks that the edit investment page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/investments/edit/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_investment_edit_accessible_by_name(self):
        """Checks that edit investment page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investment_edit", kwargs={"investment_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_investment_edit_html404_on_invalid_name(self):
        """Checks that edit investment page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investment_edit", kwargs={"investment_id": 999999999})
        )
        
        # Check that a 404 response is generated
        self.assertEqual(response.status_code, 404)

    def test_investment_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investment_edit", kwargs={"investment_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "investments/edit.html")
        
    def test_investment_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["name"] = "GIC - 3 Month Term"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("investment_edit", kwargs={"investment_id": 1}),
            edited_data,
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("investments_dashboard"))

    def test_investment_edit_fail_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["name"] = "GIC - 3 Month Term"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("investment_edit", kwargs={"investment_id": 999999999}),
            edited_data,
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)
        
    def test_investment_edit_confirm_edit(self):
        """Confirms that the edit functionality work properly"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["name"] = "GIC - 3 Month Term"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("investment_edit", kwargs={"investment_id": 1}),
            edited_data
        )

        # Confirm still only 1 entry
        self.assertEqual(1, Investment.objects.count())

        # Confirm name has been updated properly
        self.assertEqual(
            Investment.objects.get(id=1).name,
            "GIC - 3 Month Term"
        )

class InvestmentDeleteTest(TestCase):
    """Tests for the delete investment view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "investments/tests/fixtures/authentication.json",
        "investments/tests/fixtures/investment.json",
    ]

    def test_investment_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("investment_delete", kwargs={"investment_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_investment_delete_url_exists_at_desired_location(self):
        """Checks that the delete investment page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/investments/delete/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_investment_delete_html404_on_invalid_url(self):
        """Checks that the delete investment page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/investments/delete/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_investment_delete_accessible_by_name(self):
        """Checks that delete investment page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investment_delete", kwargs={"investment_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_investment_delete_html404_on_invalid_name(self):
        """Checks that delete investment page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investment_delete", kwargs={"investment_id": 999999999})
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_investment_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investment_delete", kwargs={"investment_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "investments/delete.html")
        
    def test_investment_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("investment_delete", kwargs={"investment_id": 1}),
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("investments_dashboard"))

    def test_investment_delete_fails_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("investment_delete", kwargs={"investment_id": 999999999}),
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_investment_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse("investment_delete", kwargs={"investment_id": 1})
        )

        # Checks that investment was deleted
        self.assertEqual(0, Investment.objects.filter(id=1).count())
