"""Test cases for the financial_codes app financial code views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from financial_codes.models import FinancialCode

from .utils import create_user, create_financial_code_groups, create_financial_codes

class FinancialCodeAddTest(TestCase):
    """Tests for the add financial code group view"""

    def setUp(self):
        create_user()
        groups = create_financial_code_groups()

        self.valid_data = {
            "financial_code_group": groups[0].id,
            "code": "1000",
            "description": "FK Travel Grant"
        }

    def test_code_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("financial_codes:code_add"))

        self.assertEqual(response.status_code, 302)

    def test_code_add_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:code_add"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that status is 200
        self.assertEqual(response.status_code, 200)

    def test_code_add_url_exists_at_desired_location(self):
        """Checks that the add financial code page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/code/add/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_code_add_accessible_by_name(self):
        """Checks that add year page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:code_add"))

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_code_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:code_add"))

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/code_add.html")

    def test_code_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:code_add"), self.valid_data, follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_code_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_codes:code_add"), self.valid_data, follow=True,
        )

        # Check that one financial code was added
        self.assertEqual(1, FinancialCode.objects.count())

    def test_code_add_no_redirect_on_invalid_data(self):
        """Confirms user ends up on add page on invalid data"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["code"] = None

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:code_add"), invalid_data, follow=True,
        )

        # Check for proper status code
        self.assertEqual(response.status_code, 200)

class FinancialCodeEditTest(TestCase):
    """Tests for the edit financial code view"""

    def setUp(self):
        create_user()
        codes = create_financial_codes()

        self.valid_data = {
            "financial_code_group": codes[0].financial_code_group.id,
            "code": codes[0].code,
            "description": codes[0].description
        }
        self.code_id = codes[0].id
        self.valid_args = {"code_id": codes[0].id}
        self.valid_url = "/settings/codes/code/edit/{}".format(codes[0].id)

    def test_code_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_codes:code_edit", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_code_edit_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:code_edit", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that status is 200
        self.assertEqual(response.status_code, 200)

    def test_code_edit_url_exists_at_desired_location(self):
        """Checks that the edit financial code page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_code_edit_accessible_by_name(self):
        """Checks that edit financial code page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:code_edit", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_code_edit_html404_on_invalid_name(self):
        """Checks that edit financial code page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:code_edit", kwargs={"code_id": 999999999})
        )

        # Check that a 404 response is generated
        self.assertEqual(response.status_code, 404)

    def test_code_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:code_edit", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/code_edit.html")

    def test_code_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:code_edit", kwargs=self.valid_args),
            self.valid_data,
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_code_edit_confirm_edit(self):
        """Confirms that the edit functionality work properly"""
        # Count current entries
        code_total = FinancialCode.objects.count()
        # Setup the edited data
        edited_data = self.valid_data
        edited_data["code"] = "1005"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_codes:code_edit", kwargs=self.valid_args),
            edited_data
        )

        # Confirm no new entries added
        self.assertEqual(FinancialCode.objects.count(), code_total)

        # Confirm code has been updated properly
        self.assertEqual(
            FinancialCode.objects.get(id=self.code_id).code,
            edited_data["code"]
        )

class FinancialCodeDeleteTest(TestCase):
    """Tests for the delete financial code view"""

    def setUp(self):
        create_user()
        codes = create_financial_codes()

        self.code_id = codes[0].id
        self.valid_args = {"code_id": codes[0].id}
        self.valid_url = "/settings/codes/code/delete/{}".format(codes[0].id)

    def test_code_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_codes:code_delete", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_code_edit_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:code_delete", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that status is 200
        self.assertEqual(response.status_code, 200)

    def test_code_delete_url_exists_at_desired_location(self):
        """Checks that the delete financial code page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_code_delete_accessible_by_name(self):
        """Checks that delete financial code page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:code_delete", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_code_delete_html404_on_invalid_name(self):
        """Checks that delete financial code page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:code_delete", kwargs={"code_id": 999999999})
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_code_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:code_delete", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/delete.html")

    def test_code_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:code_delete", kwargs=self.valid_args),
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_code_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Count current entries
        code_total = FinancialCode.objects.count()

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_codes:code_delete", kwargs=self.valid_args)
        )

        # Check that entry was removed
        self.assertEqual(FinancialCode.objects.count(), code_total - 1)
