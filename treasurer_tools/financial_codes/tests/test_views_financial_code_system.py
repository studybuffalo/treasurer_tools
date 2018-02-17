"""Test cases for the financial_codes app financial code system views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from financial_codes.models import FinancialCodeSystem

from .utils import create_user, create_financial_code_systems

class FinancialCodeSystemAddTest(TestCase):
    """Tests for the add financial code system view"""

    def setUp(self):
        create_user()

        self.correct_data = {
            "title": "CSHP National",
            "date_start": "2017-01-01",
        }

    def test_system_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("financial_codes:system_add"))

        self.assertEqual(response.status_code, 302)

    def test_system_add_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:system_add"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that there was no redirect
        self.assertEqual(response.status_code, 200)

    def test_system_add_url_exists_at_desired_location(self):
        """Checks that the add financial code system page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/system/add/")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_system_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_codes:system_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/add.html")

    def test_system_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:system_add"), self.correct_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_system_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        # Get current count
        system_total = FinancialCodeSystem.objects.count()
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:system_add"), self.correct_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one financial code system was added
        self.assertEqual(FinancialCodeSystem.objects.count(), system_total + 1)
    
class FinancialCodeSystemEditTest(TestCase):
    """Tests for the edit financial code system view"""

    def setUp(self):
        create_user()
        systems = create_financial_code_systems()

        self.valid_data = {
            "title": systems[0].title,
            "date_start": systems[0].date_start,
            "date_end": systems[0].date_end if systems[0].date_end else "",
        }
        self.system_id = systems[0].id
        self.valid_url = "/settings/codes/system/edit/{}".format(systems[0].id)
        self.valid_args = {"system_id": systems[0].id}

    def test_system_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_codes:system_edit", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_system_edit_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:system_edit", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that there was no redirect
        self.assertEqual(response.status_code, 200)

    def test_system_edit_url_exists_at_desired_location(self):
        """Checks that the edit financial code system page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_system_edit_html404_on_invalid_url(self):
        """Checks that the edit financial code system page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/system/edit/999999999")

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_system_edit_accessible_by_name(self):
        """Checks that edit financial code system page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:system_edit", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_system_edit_html404_on_invalid_name(self):
        """Checks that edit financial code system page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:system_edit", kwargs={"system_id": 999999999})
        )
        
        # Check that a 404 response is generated
        self.assertEqual(response.status_code, 404)

    def test_system_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:system_edit", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/edit.html")
        
    def test_system_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:system_edit", kwargs=self.valid_args),
            self.valid_data,
            follow=True
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_system_edit_confirm_edit(self):
        """Confirms that the edit functionality work properly"""
        # Count number of entries
        system_total = FinancialCodeSystem.objects.count()

        # Setup the edited data
        edited_data = self.valid_data
        edited_data["title"] = "CSHP Alberta Branch"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_codes:system_edit", kwargs=self.valid_args),
            edited_data
        )

        # Confirm still only two entries
        self.assertEqual(FinancialCodeSystem.objects.count(), system_total)

        # Confirm title has been updated properly
        self.assertEqual(
            FinancialCodeSystem.objects.get(id=self.system_id).title,
            edited_data["title"]
        )

    def test_system_edit_no_redirect_on_invalid_data(self):
        """Tests that user returns to edit page on invalid data"""
        invalid_data = self.valid_data
        invalid_data["title"] = None

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_codes:system_edit", kwargs=self.valid_args),
            invalid_data,
            follow=True
        )

        # Check that user is not redirected
        self.assertEqual(response.status_code, 200)

class FinancialCodeSystemDeleteTest(TestCase):
    """Tests for the delete financial code system view"""

    def setUp(self):
        create_user()
        systems = create_financial_code_systems()

        self.system_id = systems[0].id
        self.valid_url = "/settings/codes/system/edit/{}".format(systems[0].id)
        self.valid_args = {"system_id": systems[0].id}

    def test_system_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_codes:system_delete", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_system_delete_no_redirect_if_logged_in(self):
        """Checks user is redirected if not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:system_delete", kwargs=self.valid_args)
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that there was no redirect
        self.assertEqual(response.status_code, 200)

    def test_system_delete_url_exists_at_desired_location(self):
        """Checks that the delete financial code system page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(self.valid_url)
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_system_delete_accessible_by_name(self):
        """Checks that delete financial code system page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:system_delete", kwargs=self.valid_args)
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_system_delete_html404_on_invalid_name(self):
        """Checks that delete financial code system page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:system_delete", kwargs={"system_id": 999999999})
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_system_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_codes:system_delete", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/delete.html")

    def test_system_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("financial_codes:system_delete", kwargs=self.valid_args),
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes:dashboard"))

    def test_system_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse("financial_codes:system_delete", kwargs={"system_id": 1})
        )

        # Checks that financial code system was deleted
        self.assertEqual(0, FinancialCodeSystem.objects.filter(id=1).count())
