"""Test cases for the bank_reconcilation app models"""

from django.test import TestCase

from ..models import ReconciliationMatch
from bank_transactions.models import Institution, Account, Statement, BankTransaction

class ReconciliationMatchModelTest(TestCase):
    """Tests for the ReconciliationMatch model"""

    def setUp(self):
        institution_reference, _ = Institution.objects.get_or_create(
            name="Test Institution",
            address="1234 Bank Street",
            phone="777-888-9999",
            fax="999-888-7777",
        )
        account_reference, _ = Account.objects.get_or_create(
            institution=institution_reference,
            account_number="123456789",
            name="Chequing Account",
            status="a"
        )
        statement_reference, _ = Statement.objects.get_or_create(
            account=account_reference,
            date_start="2017-01-01",
            date_end="2017-01-31"
        )
        BankTransaction.objects.get_or_create(
            statement=statement_reference,
            date_transaction="2017-01-01",
            description_bank="CHQ#0001",
            description_user="Cheque #0001",
            amount_debit=100.00,
            amount_credit=0.00,
        )

    def test_string_representation(self):
        """Tests ReconciliationMatch string representation"""
        # pylint: disable=no-member
        reconciliation_match = ReconciliationMatch.objects.get(id=1)

        self.assertEqual(
            str(reconciliation_match),
            "2017-01-01 - Cheque #0001 - 2017-06-01 - Expense - Joshua Torrance - Travel Grant award 2017"
        )
