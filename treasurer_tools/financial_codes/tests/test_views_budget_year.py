"""Test cases for the financial_codes app budget year views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from financial_codes.models import BudgetYear

from .utils import create_user, create_financial_code_systems, create_budget_year

class BudgetYearAddTest(TestCase):
    """Tests for the add financial code group view"""

    def setUp(self):
        create_user()
        systems = create_financial_code_systems()

        self.valid_data = {
            "financial_code_system": systems[0].id,
            "date_start": "2017-04-01",
            "date_end": "2018-03-31"
        }

    def test_year_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("financial_codes:year_add"))

        self.assertEqual(response.status_code, 302)

    def test_year_add_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:year_add"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that status is 200
        self.assertEqual(response.status_code, 200)

    def test_year_add_url_exists_at_desired_location(self):
        """Checks that the add budget year page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/year/add/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_year_add_accessible_by_name(self):
        """Checks that add year page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:year_add"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_year_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:year_add"))

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/add.html")

    def test_year_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:year_add"), self.valid_data, follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_year_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:year_add"), self.valid_data, follow=True,
        )

        # Check that one budget year was added
        self.assertEqual(1, BudgetYear.objects.count())

    def test_year_add_no_redirect_on_invalid_data(self):
        """Confirms user ends up on add page on invalid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["date_start"] = None

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:year_add"), invalid_data, follow=True,
        )

        # Check for proper status code
        self.assertEqual(response.status_code, 200)

class BudgetYearEditTest(TestCase):
    """Tests for the edit budget year view"""

    def setUp(self):
        create_user()
        year = create_budget_year()

        self.valid_data = {
            "financial_code_system":  year.financial_code_system.id,
            "date_start": year.date_start,
            "date_end": year.date_end,
        }
        self.year_id = year.id
        self.valid_url = "/settings/codes/year/delete/{}".format(year.id)
        self.valid_args = {"year_id": year.id}

    def test_year_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_codes:year_edit", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_year_edit_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:year_edit", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that status is 200
        self.assertEqual(response.status_code, 200)

    def test_year_edit_url_exists_at_desired_location(self):
        """Checks that the edit budget year page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_year_edit_accessible_by_name(self):
        """Checks that edit budget year page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:year_edit", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_year_edit_html404_on_invalid_name(self):
        """Checks that edit budget year page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:year_edit", kwargs={"year_id": 999999999})
        )

        # Check that a 404 response is generated
        self.assertEqual(response.status_code, 404)

    def test_year_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:year_edit", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/edit.html")

    def test_year_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:year_edit", kwargs=self.valid_args),
            self.valid_data,
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_year_edit_confirm_edit(self):
        """Confirms that the edit functionality work properly"""
        # Count number of entries
        years_total = BudgetYear.objects.count()

        # Setup the edited data
        edited_data = self.valid_data
        edited_data["date_start"] = "2017-01-01"
        edited_data["date_end"] = "2017-12-31"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_codes:year_edit", kwargs=self.valid_args),
            edited_data
        )

        # Confirm no new entries added
        self.assertEqual(BudgetYear.objects.count(), years_total)

        # Confirm date_start has been updated properly
        self.assertEqual(
            str(BudgetYear.objects.get(id=self.year_id).date_start),
            "2017-01-01"
        )

        # Confirm date_end has been updated properly
        self.assertEqual(
            str(BudgetYear.objects.get(id=self.year_id).date_end),
            "2017-12-31"
        )

    def test_year_edit_no_redirect_on_invalid_data(self):
        """Confirms user ends up on edit page on invalid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["date_start"] = None

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:year_edit", kwargs=self.valid_args),
            invalid_data,
            follow=True,
        )

        # Check for proper status code
        self.assertEqual(response.status_code, 200)

class BudgetYearDeleteTest(TestCase):
    """Tests for the delete budget year view"""

    def setUp(self):
        create_user()
        year = create_budget_year()

        self.year_id = year.id
        self.valid_args = {"year_id": year.id}
        self.valid_url = "/settings/codes/year/delete/{}".format(year.id)

    def test_year_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_codes:year_delete", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_year_delete_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:year_delete", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that status is 200
        self.assertEqual(response.status_code, 200)

    def test_year_delete_url_exists_at_desired_location(self):
        """Checks that the delete budget year page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_year_delete_accessible_by_name(self):
        """Checks that delete budget year page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:year_delete", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_year_delete_html404_on_invalid_name(self):
        """Checks that delete budget year page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:year_delete", kwargs={"year_id": 999999999})
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def tes_year_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:year_delete", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/delete.html")

    def test_year_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("financial_codes:year_delete", kwargs=self.valid_args),
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_year_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Get current number of budget years
        year_total = BudgetYear.objects.count()
        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_codes:year_delete", kwargs=self.valid_args)
        )

        # Checks that budget year was deleted
        self.assertEqual(BudgetYear.objects.count(), year_total - 1)
