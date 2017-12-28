"""Test cases for the bank_transaction app"""

from django.test import TestCase

from bank_transactions.models import Institution

class DemographicsModelTest(TestCase):
    """Test functions for the Demographics model"""
    # pylint: disable=no-member,protected-access

    @classmethod
    def setUpTestData(cls):
        Institution.objects.create(
            name="Test Financial Institution",
            address="1234 Financial Avenue",
            phone="1-800-123-4569",
            fax="1-877-123-1234",
        )
