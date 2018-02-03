"""Test cases for the bank_reconcilation app models"""

from django.test import TestCase

from ..models import ReconciliationMatch
from utils.utils_tests import create_reconciliation_matches

class ReconciliationMatchModelTest(TestCase):
    """Tests for the ReconciliationMatch model"""

    def setUp(self):
        create_reconciliation_matches()
        
    def test_string_representation(self):
        """Tests ReconciliationMatch string representation"""
        # pylint: disable=no-member
        reconciliation_match = ReconciliationMatch.objects.first()

        self.assertEqual(
            str(reconciliation_match),
            "2017-01-01 - Cheque #0001 - 2017-06-01 - Expense - Test User - Test Expense Transaction 1"
        )
