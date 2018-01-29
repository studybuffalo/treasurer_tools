"""Test cases for the financial_codes app financial code system views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from financial_codes.models import FinancialCodeSystem

class FinancialCodeSystemAddTest(TestCase):
    """Tests for the add financial code system view"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "financial_codes/tests/fixtures/authentication.json",
    ]
    
    def setUp(self):
        self.correct_data = {
            "title": "CSHP National",
            "date_start": "2017-01-01",
        }
        
    def test_financial_code_system_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("financial_code_system_add"))

        self.assertEqual(response.status_code, 302)

    def test_financial_code_system_add_url_exists_at_desired_location(self):
        """Checks that the add financial code system page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/system/add/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_financial_code_system_add_accessible_by_name(self):
        """Checks that add financial code system page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_code_system_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_financial_code_system_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("financial_code_system_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/add.html")

    def test_financial_code_system_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_code_system_add"), self.correct_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes_dashboard"))

    def test_financial_code_system_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_code_system_add"), self.correct_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one financial code system was added
        self.assertEqual(1, FinancialCodeSystem.objects.count())
    
class FinancialCodeSystemEditTest(TestCase):
    """Tests for the edit financial code system view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/authentication.json",
        "financial_codes/tests/fixtures/financial_code_system.json",
    ]

    def setUp(self):
        # Add standard test data
        self.correct_data = {
            "title": "CSHP National",
            "date_start": "2017-01-01",

        }

    def test_financial_code_system_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_code_system_edit", kwargs={"system_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_financial_code_system_edit_url_exists_at_desired_location(self):
        """Checks that the edit financial code system page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/system/edit/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_financial_code_system_edit_html404_on_invalid_url(self):
        """Checks that the edit financial code system page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/system/edit/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_financial_code_system_edit_accessible_by_name(self):
        """Checks that edit financial code system page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_code_system_edit", kwargs={"system_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_financial_code_system_edit_html404_on_invalid_name(self):
        """Checks that edit financial code system page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_code_system_edit", kwargs={"system_id": 999999999})
        )
        
        # Check that a 404 response is generated
        self.assertEqual(response.status_code, 404)

    def test_financial_code_system_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_code_system_edit", kwargs={"system_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/edit.html")
        
    def test_financial_code_system_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["title"] = "CSHP Alberta Branch"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_code_system_edit", kwargs={"system_id": 1}),
            edited_data,
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes_dashboard"))

    def test_financial_code_system_edit_fail_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["title"] = "CSHP Alberta Branch"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("financial_code_system_edit", kwargs={"system_id": 999999999}),
            edited_data,
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)
        
    def test_financial_code_system_edit_confirm_edit(self):
        """Confirms that the edit functionality work properly"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["title"] = "CSHP Alberta Branch"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("financial_code_system_edit", kwargs={"system_id": 1}),
            edited_data
        )

        # Confirm still only two entries
        self.assertEqual(2, FinancialCodeSystem.objects.count())

        # Confirm title has been updated properly
        self.assertEqual(
            FinancialCodeSystem.objects.get(id=1).title,
            "CSHP Alberta Branch"
        )

class FinancialCodeSystemDeleteTest(TestCase):
    """Tests for the delete financial code system view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/authentication.json",
        "financial_codes/tests/fixtures/financial_code_system.json",
    ]

    def test_financial_code_system_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("financial_code_system_delete", kwargs={"system_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_financial_code_system_delete_url_exists_at_desired_location(self):
        """Checks that the delete financial code system page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/system/delete/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_financial_code_system_delete_html404_on_invalid_url(self):
        """Checks that the delete financial code system page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/system/delete/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_financial_code_system_delete_accessible_by_name(self):
        """Checks that delete financial code system page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_code_system_delete", kwargs={"system_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_financial_code_system_delete_html404_on_invalid_name(self):
        """Checks that delete financial code system page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_code_system_delete", kwargs={"system_id": 999999999})
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_financial_code_system_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("financial_code_system_delete", kwargs={"system_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/delete.html")
        
    def test_financial_code_system_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("financial_code_system_delete", kwargs={"system_id": 1}),
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes_dashboard"))

    def test_financial_code_system_delete_fails_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("financial_code_system_delete", kwargs={"system_id": 999999999}),
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_financial_code_system_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse("financial_code_system_delete", kwargs={"system_id": 1})
        )

        # Checks that financial code system was deleted
        self.assertEqual(0, FinancialCodeSystem.objects.filter(id=1).count())
