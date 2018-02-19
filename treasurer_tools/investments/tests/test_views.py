"""Test cases for the investments app views"""

from django.core.urlresolvers import reverse
from django.test import TestCase

from investments.models import Investment

from .utils import create_user, create_investment


class InvestmentsDashboard(TestCase):
    """Tests for the investments dashboard view"""

    def setUp(self):
        create_user()

    def test_dashboard_redirect_if_not_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        response = self.client.get(reverse("investments:dashboard"))

        self.assertRedirects(response, "/accounts/login/?next=/investments/")

    def test_dashboard_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("investments:dashboard"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_url_exists_at_desired_location(self):
        """Checks that the dashboard uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/investments/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_dashboard_template(self):
        """Checks that the dashboard uses the correct template"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("investments:dashboard"))

        # Check for proper template
        self.assertTemplateUsed(response, "investments/index.html")

class InvestmentAddTest(TestCase):
    """Tests for the add investment view"""

    def setUp(self):
        create_user()

        self.valid_data = {
            "name": "Mutual Funds",
            "date_invested": "2017-03-01",
            "amount": 1000.00,
            "rate": "0.05% per month"
        }

    def test_add_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(reverse("investments:add"))

        self.assertEqual(response.status_code, 302)

    def test_add_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("investments:add"))

        # Check that user logged in
        self.assertEqual(str(response.context['user']), 'user')

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_add_url_exists_at_desired_location(self):
        """Checks that the add investment page uses the correct URL"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get("/investments/add/")

        # Check that page is accessible
        self.assertEqual(response.status_code, 200)

    def test_investment_add_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(reverse("investments:add"))

        # Check for proper template
        self.assertTemplateUsed(response, "investments/add.html")

    def test_add_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("investments:add"), self.valid_data, follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("investments:dashboard"))

    def test_add_no_redirect_on_invalid_data(self):
        """Confirms data is added to database on successful form submission"""
        # Setup invalid data
        invalid_data = self.valid_data
        invalid_data["name"] = None

        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("investments:add"), invalid_data, follow=True,
        )

        # Check that there was no redirect
        self.assertEqual(response.status_code, 200)

    def test_add_saves_to_database(self):
        """Checks that form can properly save to database"""
        # Get current total of investments
        investment_total = Investment.objects.count()

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("investments:add"), self.valid_data, follow=True,
        )

        # Check that one entry is added
        self.assertEqual(Investment.objects.count(), investment_total + 1)

class InvestmentEditTest(TestCase):
    """Tests for the edit investment view"""

    def setUp(self):
        create_user()
        investment = create_investment()

        self.current_data = {
            "name": investment.name,
            "date_invested": investment.date_invested,
            "amount": investment.amount,
            "rate": investment.rate
        }
        self.new_data = {
            "name": "Mutual Funds",
            "date_invested": "2017-03-01",
            "amount": 1000.00,
            "rate": "0.05% per month"
        }
        self.valid_args = {"investment_id": investment.id}
        self.valid_url = "/investments/edit/{}".format(investment.id)

    def test_edit_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("investments:edit", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_edit_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investments:edit", kwargs=self.valid_args)
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
        """Checks that edit page URL name failed on invalid ID"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investments:edit", kwargs={"investment_id": 999999999})
        )

        # Check that a 404 response is generated
        self.assertEqual(response.status_code, 404)

    def test_edit_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investments:edit", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "investments/edit.html")

    def test_edit_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("investments:edit", kwargs=self.valid_args),
            self.current_data,
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("investments:dashboard"))

    def test_edit_confirm_edit(self):
        """Confirms that the edit functionality work properly"""
        # Get current number of investments
        investment_total = Investment.objects.count()

        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("investments:edit", kwargs=self.valid_args),
            self.new_data
        )

        # Confirm still only 1 entry
        self.assertEqual(Investment.objects.count(), investment_total)

        # Confirm name has been updated properly
        self.assertEqual(
            Investment.objects.last().name,
            self.new_data["name"]
        )

class InvestmentDeleteTest(TestCase):
    """Tests for the delete investment view"""

    def setUp(self):
        create_user()
        investment = create_investment()

        self.valid_args = {"investment_id": investment.id}
        self.valid_url = "/investments/delete/{}".format(investment.id)

    def test_investment_delete_redirect_if_not_logged_in(self):
        """Checks user is redirected if not logged in"""
        response = self.client.get(
            reverse("investments:delete", kwargs=self.valid_args)
        )

        self.assertEqual(response.status_code, 302)

    def test_delete_no_redirect_if_logged_in(self):
        """Checks redirect to login page if user is not logged in"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investments:delete", kwargs=self.valid_args)
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
            reverse("investments:delete", kwargs={"investment_id": 999999999})
        )

        # Check that page is accessible
        self.assertEqual(response.status_code, 404)

    def test_delete_template(self):
        """Checks that correct template is being used"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.get(
            reverse("investments:delete", kwargs=self.valid_args)
        )

        # Check for proper template
        self.assertTemplateUsed(response, "investments/delete.html")

    def test_delete_redirect_to_dashboard(self):
        """Checks that form redirects to the dashboard on success"""
        self.client.login(username="user", password="abcd123456")
        response = self.client.post(
            reverse("investments:delete", kwargs=self.valid_args),
            follow=True,
        )

        # Check that redirection was successful
        self.assertRedirects(response, reverse("investments:dashboard"))

    def test_delete_confirm_deletion(self):
        """Confirms deletion form works properly"""
        # Get current totals
        investment_total = Investment.objects.count()

        # Delete entry
        self.client.login(username="user", password="abcd123456")
        self.client.post(
            reverse("investments:delete", kwargs=self.valid_args)
        )

        # Checks that investment was deleted
        self.assertEqual(Investment.objects.count(), investment_total - 1)
