"""Test cases for the financial_codes app budget year views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from financial_codes.models import BudgetYear

class BudgetYearAddTest(TestCase):
    """Tests for the add financial code group view"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "financial_codes/tests/fixtures/authentication.json",
        "financial_codes/tests/fixtures/financial_code_system.json",
    ]
    
    def setUp(self):
        self.correct_data = {
            "financial_code_system":  1,
            "date_start": "2017-04-01",
            "date_end": "2018-03-31"
        }
        
    def test_budget_year_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("year_add"))

        self.assertEqual(response.status_code, 302)

    def test_budget_year_add_url_exists_at_desired_location(self):
        """Checks that the add budget year page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/year/add/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_budget_year_add_accessible_by_name(self):
        """Checks that add year page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("year_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_budget_year_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("year_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/add.html")

    def test_budget_year_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("year_add"), self.correct_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes_dashboard"))

    def test_budget_year_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("year_add"), self.correct_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one budget year was added
        self.assertEqual(1, BudgetYear.objects.count())
  
class BudgetYearEditTest(TestCase):
    """Tests for the edit budget year view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/authentication.json",
        "financial_codes/tests/fixtures/financial_code_system.json",
        "financial_codes/tests/fixtures/budget_year.json",
    ]

    def setUp(self):
        # Add standard test data
        self.correct_data = {
            "financial_code_system":  1,
            "date_start": "2017-04-01",
            "date_end": "2018-03-31"
        }

    def test_budget_year_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("year_edit", kwargs={"year_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_budget_year_edit_url_exists_at_desired_location(self):
        """Checks that the edit budget year page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/year/delete/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_budget_year_edit_html404_on_invalid_url(self):
        """Checks that the edit budget year page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/year/edit/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_budget_year_edit_accessible_by_name(self):
        """Checks that edit budget year page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("year_edit", kwargs={"year_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_budget_year_edit_html404_on_invalid_name(self):
        """Checks that edit budget year page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("year_edit", kwargs={"year_id": 999999999})
        )
        
        # Check that a 404 response is generated
        self.assertEqual(response.status_code, 404)

    def test_budget_year_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("year_edit", kwargs={"year_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/edit.html")
        
    def test_budget_year_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["date_start"] = "2017-01-01"
        edited_data["date_end"] = "2017-12-31"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("year_edit", kwargs={"year_id": 1}),
            edited_data,
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes_dashboard"))

    def test_budget_year_edit_fail_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["date_start"] = "2017-01-01"
        edited_data["date_end"] = "2017-12-31"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("year_edit", kwargs={"year_id": 999999999}),
            edited_data,
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)
        
    def test_budget_year_edit_confirm_edit(self):
        """Confirms that the edit functionality work properly"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["date_start"] = "2017-01-01"
        edited_data["date_end"] = "2017-12-31"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("year_edit", kwargs={"year_id": 1}),
            edited_data
        )

        # Confirm still only 1 entry
        self.assertEqual(1, BudgetYear.objects.count())

        # Confirm date_start has been updated properly
        self.assertEqual(
            str(BudgetYear.objects.get(id=1).date_start),
            "2017-01-01"
        )
        
        # Confirm date_end has been updated properly
        self.assertEqual(
            str(BudgetYear.objects.get(id=1).date_end),
            "2017-12-31"
        )

class BudgetYearDeleteTest(TestCase):
    """Tests for the delete budget year view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/authentication.json",
        "financial_codes/tests/fixtures/financial_code_system.json",
        "financial_codes/tests/fixtures/budget_year.json",
    ]

    def test_budget_year_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("year_delete", kwargs={"year_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_budget_year_delete_url_exists_at_desired_location(self):
        """Checks that the delete budget year page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/year/delete/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_budget_year_delete_html404_on_invalid_url(self):
        """Checks that the delete budget year page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/year/delete/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_budget_year_delete_accessible_by_name(self):
        """Checks that delete budget year page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("year_delete", kwargs={"year_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_budget_year_delete_html404_on_invalid_name(self):
        """Checks that delete budget year page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("year_delete", kwargs={"year_id": 999999999})
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_budget_year_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("year_delete", kwargs={"year_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/delete.html")
        
    def test_budget_year_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("year_delete", kwargs={"year_id": 1}),
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes_dashboard"))

    def test_budget_year_delete_fails_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("year_delete", kwargs={"year_id": 999999999}),
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_budget_year_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse("year_delete", kwargs={"year_id": 1})
        )

        # Checks that budget year was deleted
        self.assertEqual(0, BudgetYear.objects.filter(id=1).count())
