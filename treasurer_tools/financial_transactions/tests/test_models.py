"""Test cases for the bank_transaction app"""

from decimal import Decimal

from django.test import TestCase

from financial_transactions.models import FinancialCodeMatch

from .utils import create_financial_transactions, create_financial_codes


class TransactionModelTest(TestCase):
    """Test functions for the Transaction model"""

    def setUp(self):
        self.transactions = create_financial_transactions()

    def test_labels(self):
        """tests a series of fields for proper label generation"""

        # Test payee_payer label
        self.assertEqual(
            self.transactions[0]._meta.get_field("payee_payer").verbose_name,
            "payee or payer"
        )

        # Test transaction_type label
        self.assertEqual(
            self.transactions[0]._meta.get_field("transaction_type").verbose_name,
            "transaction type"
        )

        # Test memo label
        self.assertEqual(
            self.transactions[0]._meta.get_field("memo").verbose_name,
            "memo"
        )

        # Test date_submitted label
        self.assertEqual(
            self.transactions[0]._meta.get_field("date_submitted").verbose_name,
            "submission date"
        )

    def test_memo_max_length(self):
        """Tests the memo field for proper max length"""
        self.assertEqual(
            self.transactions[0]._meta.get_field("memo").max_length,
            1000
        )

    def test_string_representation_expense(self):
        """Tests that the model string representaton returns as expected"""

        test_string = "{} - Expense - {} - {}".format(
            self.transactions[0].date_submitted,
            self.transactions[0].payee_payer,
            self.transactions[0].memo[:100]
        )

        self.assertEqual(
            str(self.transactions[0]),
            test_string
        )

    def test_string_representation_revenue(self):
        """Tests that the model string representaton returns as expected"""

        test_string = "{} - Revenue - {} - {}".format(
            self.transactions[1].date_submitted,
            self.transactions[1].payee_payer,
            self.transactions[1].memo[:100]
        )

        self.assertEqual(
            str(self.transactions[1]),
            test_string
        )

    def test_total_property(self):
        """Tests that total property returns proper value"""

        self.assertEqual(self.transactions[0].total, Decimal(210.00))

class ItemModelTest(TestCase):
    """Test functions for the Item model"""

    def setUp(self):
        transactions = create_financial_transactions()
        self.items = transactions[0].item_set.all().order_by("id")

    def test_labels(self):
        """tests a series of fields for proper label generation"""

        # Test transaction label
        self.assertEqual(
            self.items[0]._meta.get_field("transaction").verbose_name,
            "transaction"
        )

        # Test date_item label
        self.assertEqual(
            self.items[0]._meta.get_field("date_item").verbose_name,
            "date"
        )

        # Test description label
        self.assertEqual(
            self.items[0]._meta.get_field("description").verbose_name,
            "description"
        )

        # Test amount label
        self.assertEqual(
            self.items[0]._meta.get_field("amount").verbose_name,
            "amount"
        )

        # Test gst label
        self.assertEqual(
            self.items[0]._meta.get_field("gst").verbose_name,
            "GST/HST"
        )

    def test_description_max_length(self):
        """Tests the memo field for proper max length"""

        self.assertEqual(
            self.items[0]._meta.get_field("description").max_length,
            500
        )

    def test_total_function(self):
        """Tests the total function for propery string generation"""

        # Tests that total matches desired total and format
        self.assertEqual(self.items[0].total, Decimal(105.00))

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""

        self.assertEqual(
            str(self.items[0]),
            "2017-06-01 - Taxi costs (to hotel) - $105.00"
        )

class FinancialCodeMatchModelTest(TestCase):
    """Tests for the FinancialCodeMatch model"""

    def setUp(self):
        codes = create_financial_codes()
        transactions = create_financial_transactions()

        self.match = FinancialCodeMatch.objects.create(
            item=transactions[0].item_set.all()[0],
            financial_code=codes[0]
        )

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""

        self.assertEqual(
            str(self.match),
            "2017-06-01 - Taxi costs (from hotel) - $105.00 - 1000 - Travel Grant"
        )
