"""Test cases for the bank_transaction app"""

from django.test import TestCase

from financial_transactions.models import FinancialTransaction, Item, FinancialCodeMatch

from .utils import create_financial_transactions


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

        self.assertEqual(self.transactions[0].total, "$210.00")

#class ItemModelTest(TestCase):
#    """Test functions for the Item model"""
#    # pylint: disable=no-member,protected-access
#    fixtures = [
#        "transactions/tests/fixtures/country.json",
#        "transactions/tests/fixtures/demographics.json",
#        "transactions/tests/fixtures/transaction.json",
#        "transactions/tests/fixtures/item.json",
#    ]

#    def test_labels(self):
#        """tests a series of fields for proper label generation"""
#        test_list = [
#            {"field_name": "transaction", "label_name": "transaction"},
#            {"field_name": "date_item", "label_name": "date"},
#            {"field_name": "description", "label_name": "description"},
#            {"field_name": "amount", "label_name": "amount"},
#            {"field_name": "gst", "label_name": "gst"},
#        ]

#        for test_item in test_list:
#            item = Item.objects.get(id=1)
#            field_label = item._meta.get_field(test_item["field_name"]).verbose_name
#            self.assertEqual(field_label, test_item["label_name"])

#    def test_description_max_length(self):
#        """Tests the memo field for proper max length"""
#        item = Item.objects.get(id=1)
#        max_length = item._meta.get_field("description").max_length
#        self.assertEqual(max_length, 500)
        
#    def test_total_function(self):
#        """Tests the total function for propery string generation"""
#        # Create a test item with known details
#        item = Item.objects.create(
#            transaction=FinancialTransaction.objects.get(id=1),
#            date_item="2017-01-02",
#            description="Test item",
#            amount=2.00,
#            gst=0.1,
#        )

#        # Tests that total matches desired total and format
#        self.assertEqual(item.total, "$2.10")

#    def test_string_representation(self):
#        """Tests that the model string representaton returns as expected"""
#        item = Item.objects.get(id=1)

#        self.assertEqual(
#            str(item),
#            "{} - {} - {}".format(item.date_item, item.description, item.total)
#        )

#class FinancialCodeMatchModelTest(TestCase):
#    """Tests for the FinancialCodeMatch model"""
#    fixtures = [
#        "transactions/tests/fixtures/country.json",
#        "transactions/tests/fixtures/demographics.json",
#        "transactions/tests/fixtures/financial_code_system.json",
#        "transactions/tests/fixtures/budget_year.json",
#        "transactions/tests/fixtures/financial_code_group.json",
#        "transactions/tests/fixtures/financial_code.json",
#        "transactions/tests/fixtures/transaction.json",
#        "transactions/tests/fixtures/item.json",
#        "transactions/tests/fixtures/financial_code_match.json",
#    ]

#    def test_string_representation(self):
#        """Tests that the model string representaton returns as expected"""
#        # pylint: disable=no-member
#        financial_code_match = FinancialCodeMatch.objects.get(id=1)

#        self.assertEqual(
#            str(financial_code_match),
#            "2017-06-01 - Taxi costs - $105.00 - 1000 - FK Travel Grant"
#        )

#class AttachmentMatchModelTest(TestCase):
#    """Test functions for the Attachment match model"""
#    # pylint: disable=no-member,protected-access
#    fixtures = [
#        "transactions/tests/fixtures/country.json",
#        "transactions/tests/fixtures/demographics.json",
#        "transactions/tests/fixtures/transaction.json",
#        "transactions/tests/fixtures/attachment.json",
#        "transactions/tests/fixtures/attachment_match.json",
#    ]

#    def test_labels(self):
#        """tests a series of fields for proper label generation"""
#        test_list = [
#            {"field_name": "transaction", "label_name": "transaction"},
#            {"field_name": "attachment", "label_name": "attachment"},
#        ]

#        for test_item in test_list:
#            attachment_match = AttachmentMatch.objects.get(id=1)
#            field_label = attachment_match._meta.get_field(test_item["field_name"]).verbose_name
#            self.assertEqual(field_label, test_item["label_name"])

#    def test_string_representation(self):
#        """Tests that the model string representaton returns as expected"""
#        attachment_match = AttachmentMatch.objects.get(id=1)

#        self.assertEqual(
#            str(attachment_match),
#            "2017-06-01 - Expense - Joshua Torrance - Travel Grant award 2017 - test.pdf"
#        )
