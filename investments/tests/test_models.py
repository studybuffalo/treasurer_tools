"""Test cases for the bank_transaction app"""

from django.test import TestCase

from investments.models import Investment

class FinancialCodeSystemModelTest(TestCase):
    """Test functions for the Financial Code System model"""
    # pylint: disable=no-member,protected-access
    
    fixtures = [
        "investments/tests/fixtures/investment.json",
    ]

    def test_labels(self):
        """tests a series of fields for proper label generation"""
        test_list = [
            {"field_name": "name", "label_name": "name"},
            {"field_name": "date_invested", "label_name": "date invested"},
            {"field_name": "amount", "label_name": "amount"},
            {"field_name": "rate", "label_name": "rate"},
        ]

        for test_item in test_list:
            investment = Investment.objects.get(id=1)
            field_label = Investment._meta.get_field(test_item["field_name"]).verbose_name
            self.assertEqual(field_label, test_item["label_name"])

    def test_name_max_length(self):
        """Tests the name field for proper max length"""
        investment = Investment.objects.get(id=1)
        max_length = investment._meta.get_field("name").max_length
        self.assertEqual(max_length, 256)
        
    def test_rate_max_length(self):
        """Tests the rate field for proper max length"""
        investment = Investment.objects.get(id=1)
        max_length = investment._meta.get_field("rate").max_length
        self.assertEqual(max_length, 256)

    def test_string_representation(self):
        """Tests that the model string representaton returns as expected"""
        investment = Investment.objects.get(id=1)
        self.assertEqual(
            str(investment), 
            "{} - {}".format(investment.date_invested, investment.name)
        )
