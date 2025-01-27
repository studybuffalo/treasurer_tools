"""Test cases for the financial_codes app financial code group views"""

from django.urls import reverse
from django.test import TestCase

from financial_codes.models import FinancialCodeGroup

from .utils import create_user, create_budget_year, create_financial_code_groups

class FinancialCodeGroupAddTest(TestCase):
    """Tests for the add financial code group view"""

    def setUp(self):
        create_user()
        year = create_budget_year()

        self.valid_data = {
            "budget_year": year.id,
            "title": "Awards & Grants",
            "description": "Expenses related to awards and grants",
            "type": "e",
            "status": "a"
        }

    def test_group_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("financial_codes:group_add"))

        self.assertEqual(response.status_code, 302)

    def test_group_add_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:group_add"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that status is 200
        self.assertEqual(response.status_code, 200)

    def test_group_add_url_exists_at_desired_location(self):
        """Checks that the add financial code group page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/group/add/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_group_add_accessible_by_name(self):
        """Checks that add financial code group page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:group_add"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_group_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:group_add"))

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/add_edit.html")

    def test_group_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:group_add"), self.valid_data, follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_group_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        # Get current total number of groups
        group_total = FinancialCodeGroup.objects.count()

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_codes:group_add"), self.valid_data, follow=True,
        )

        # Check that one financial code group was added
        self.assertEqual(FinancialCodeGroup.objects.count(), group_total + 1)

    def test_group_add_no_redirect_on_invalid_data(self):
        """Confirms user ends up on add page on invalid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["title"] = ''

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:group_add"), invalid_data, follow=True,
        )

        # Check for proper status code
        self.assertEqual(response.status_code, 200)

class FinancialCodeGroupEditTest(TestCase):
    """Tests for the edit financial code group view"""

    def setUp(self):
        create_user()
        groups = create_financial_code_groups()

        self.valid_data = {
            "budget_year": groups[0].budget_year.id,
            "title": groups[0].title,
            "description": groups[0].description,
            "type": groups[0].type,
            "status": groups[0].status,
        }
        self.group_id = groups[0].id
        self.valid_args = {"group_id": groups[0].id}
        self.valid_url = "/settings/codes/group/edit/{}/".format(groups[0].id)

    def test_group_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_codes:group_edit", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_group_edit_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:group_edit", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that status is 200
        self.assertEqual(response.status_code, 200)

    def test_group_edit_url_exists_at_desired_location(self):
        """Checks that the edit financial code group page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_group_edit_accessible_by_name(self):
        """Checks that edit financial coe group page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:group_edit", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_group_edit_html404_on_invalid_name(self):
        """Checks that edit financial code group page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:group_edit", kwargs={"group_id": 999999999})
        )

        # Check that a 404 response is generated
        self.assertEqual(response.status_code, 404)

    def test_group_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:group_edit", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/add_edit.html")

    def test_group_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:group_edit", kwargs=self.valid_args),
            self.valid_data,
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_group_edit_confirm_edit(self):
        """Confirms that the edit functionality work properly"""
        # Get current number of entries
        group_total = FinancialCodeGroup.objects.count()

        # Setup the edited data
        edited_data = self.valid_data
        edited_data["title"] = "Awards, Grants, and Sponsorship"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_codes:group_edit", kwargs=self.valid_args),
            edited_data
        )

        # Confirm still 8 entries
        self.assertEqual(FinancialCodeGroup.objects.count(), group_total)

        # Confirm title has been updated properly
        self.assertEqual(
            FinancialCodeGroup.objects.get(id=self.group_id).title,
            edited_data["title"]
        )

    def test_group_edit_no_redirect_on_invalid_data(self):
        """Confirms user ends up on edit page on invalid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["title"] = ''

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:group_edit", kwargs=self.valid_args),
            invalid_data,
            follow=True,
        )

        # Check for proper status code
        self.assertEqual(response.status_code, 200)

class FinancialCodeGroupDeleteTest(TestCase):
    """Tests for the delete financial code group view"""

    def setUp(self):
        create_user()
        groups = create_financial_code_groups()

        self.group_id = groups[0].id
        self.valid_args = {"group_id": groups[0].id}
        self.valid_url = "/settings/codes/group/delete/{}/".format(groups[0].id)

    def test_group_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_codes:group_delete", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_group_delete_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:group_delete", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that status is 200
        self.assertEqual(response.status_code, 200)

    def test_group_delete_url_exists_at_desired_location(self):
        """Checks that the delete financial code group page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_group_delete_accessible_by_name(self):
        """Checks that delete financial code group page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:group_delete", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_group_delete_html404_on_invalid_name(self):
        """Checks that delete financial code group page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:group_delete", kwargs={"group_id": 999999999})
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_group_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:group_delete", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/delete.html")

    def test_group_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("financial_codes:group_delete", kwargs=self.valid_args),
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_group_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Count current entries
        group_total = FinancialCodeGroup.objects.count()

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_codes:group_delete", kwargs=self.valid_args)
        )

        # Checks that financial code group was deleted
        self.assertEqual(FinancialCodeGroup.objects.count(), group_total - 1)
