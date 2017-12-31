"""Test cases for the financial_codes app financial code group views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from financial_codes.models import FinancialCodeGroup

class FinancialCodeGroupAddTest(TestCase):
    """Tests for the add financial code group view"""
    # pylint: disable=no-member,protected-access

    fixtures = [
        "financial_codes/tests/fixtures/authentication.json",
        "financial_codes/tests/fixtures/financial_code_system.json",
    ]
    
    def setUp(self):
        self.correct_data = {
            "financial_code_system":  1,
            "title": "Awards & Grants",
            "description": "Revenue for branch awards and grants",
            "type": "r",
            "status": "a",
        }
        
    def test_financial_code_group_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("group_add"))

        self.assertEqual(response.status_code, 302)

    def test_financial_code_group_add_url_exists_at_desired_location(self):
        """Checks that the add financial code group page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/group/add/")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_financial_code_group_add_accessible_by_name(self):
        """Checks that add financial code group page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("group_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_financial_code_group_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("group_add"))
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/add.html")

    def test_financial_code_group_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("group_add"), self.correct_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes_dashboard"))

    def test_financial_code_group_add_confirm_add(self):
        """Confirms data is added to database on successful form submission"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("group_add"), self.correct_data, follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that one financial code group was added
        self.assertEqual(1, FinancialCodeGroup.objects.count())
      
class FinancialCodeGroupEditTest(TestCase):
    """Tests for the edit financial code group view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/authentication.json",
        "financial_codes/tests/fixtures/financial_code_system.json",
        "financial_codes/tests/fixtures/financial_code_group.json",
    ]

    def setUp(self):
        # Add standard test data
        self.correct_data = {
            "financial_code_system":  1,
            "title": "Awards & Grants",
            "description": "Revenue for branch awards and grants",
            "type": "r",
            "status": "a"
        }

    def test_financial_code_group_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("group_edit", kwargs={"group_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_financial_code_group_edit_url_exists_at_desired_location(self):
        """Checks that the edit financial code group page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/group/edit/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_financial_code_group_edit_html404_on_invalid_url(self):
        """Checks that the edit financial code group page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/group/edit/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_financial_code_group_edit_accessible_by_name(self):
        """Checks that edit financial coe group page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("group_edit", kwargs={"group_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_financial_code_group_edit_html404_on_invalid_name(self):
        """Checks that edit financial code group page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("group_edit", kwargs={"group_id": 999999999})
        )
        
        # Check that a 404 response is generated
        self.assertEqual(response.status_code, 404)

    def test_financial_code_group_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("group_edit", kwargs={"group_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/edit.html")
        
    def test_financial_code_group_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["title"] = "Awards, Grants, and Sponsorship"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("group_edit", kwargs={"group_id": 1}),
            edited_data,
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes_dashboard"))

    def test_financial_code_group_edit_fail_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["title"] = "Awards, Grants, and Sponsorship"

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("group_edit", kwargs={"group_id": 999999999}),
            edited_data,
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)
        
    def test_financial_code_group_edit_confirm_edit(self):
        """Confirms that the edit functionality work properly"""
        # Setup the edited data
        edited_data = self.correct_data
        edited_data["title"] = "Awards, Grants, and Sponsorship"

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("group_edit", kwargs={"group_id": 1}),
            edited_data
        )

        # Confirm still only 2 entries
        self.assertEqual(2, FinancialCodeGroup.objects.count())

        # Confirm title has been updated properly
        self.assertEqual(
            FinancialCodeGroup.objects.get(id=1).title,
            "Awards, Grants, and Sponsorship"
        )

class FinancialCodeGroupDeleteTest(TestCase):
    """Tests for the delete financial code group view"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "financial_codes/tests/fixtures/authentication.json",
        "financial_codes/tests/fixtures/financial_code_system.json",
        "financial_codes/tests/fixtures/financial_code_group.json",
    ]

    def test_financial_code_group_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("group_delete", kwargs={"group_id": 1})
        )

        self.assertEqual(response.status_code, 302)

    def test_financial_code_group_delete_url_exists_at_desired_location(self):
        """Checks that the delete financial code group page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/group/delete/1")
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_financial_code_group_delete_html404_on_invalid_url(self):
        """Checks that the delete financial code group page URL fails on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/settings/codes/group/delete/999999999")
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_financial_code_group_delete_accessible_by_name(self):
        """Checks that delete financial code group page URL name works properly"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("group_delete", kwargs={"group_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)
        
    def test_financial_code_group_delete_html404_on_invalid_name(self):
        """Checks that delete financial code group page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("group_delete", kwargs={"group_id": 999999999})
        )
        
        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_financial_code_group_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("group_delete", kwargs={"group_id": 1})
        )
        
        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check for proper template
        self.assertTemplateUsed(response, "financial_codes/delete.html")
        
    def test_financial_code_group_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("group_delete", kwargs={"group_id": 1}),
            follow=True,
        )

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')
        
        # Check that redirection was successful
        self.assertRedirects(response, reverse("financial_codes_dashboard"))

    def test_financial_code_group_delete_fails_on_invalid_id(self):
        """Checks that a POST fails when an invalid ID is provided"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        response = self.client.post(
            reverse("group_delete", kwargs={"group_id": 999999999}),
            follow=True,
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_financial_code_group_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Login
        self.client.login(username="user", password="abcd123456")

        # Delete entry
        self.client.post(
            reverse("group_delete", kwargs={"group_id": 1})
        )

        # Checks that financial code group was deleted
        self.assertEqual(0, FinancialCodeGroup.objects.filter(id=1).count())
