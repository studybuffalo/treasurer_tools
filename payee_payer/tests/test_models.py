"""Test cases for the payee_payer app"""

from django.test import TestCase

from payee_payer.models import Country, Demographics

class DemographicsModelTest(TestCase):
    """Test functions for the Demographics model"""
    
    @classmethod
    def setUpTestData(cls):
        # Setup country data for testing
        Country.objects.create(country_code="CA", country_name="Canada")
        Demographics.objects.create(
            name="Joshua Torrance",
            address="111-2222 Test Street",
            city="Vancouver",
            province="British Columbia",
            country=Country.objects.create(id=0),
            postal_code="V1V 1V1",
            phone="111-222-3333",
            fax="444-555-6666",
            email="test@email.com",
            status="a",
        )

    def test_labels(self):
        """Tests a series of fields for proper label generation"""
        test_list = [
            {"field_name": "name", "label_name": "name"},
            {"field_name": "address", "label_name": "address"},
            {"field_name": "city", "label_name": "city"},
            {"field_name": "province", "label_name": "province"},
            {"field_name": "country", "label_name": "country"},
            {"field_name": "postal_code", "label_name": "postal code"},
            {"field_name": "phone", "label_name": "phone number"},
            {"field_name": "fax", "label_name": "fax number"},
            {"field_name": "email", "label_name": "email"},
            {"field_name": "status", "label_name": "status"},
        ]

        for test_item in test_list:
            payee_payer = Demographics.objects.get(id=1)
            field_label = payee_payer._meta.get_field(test_item["field_name"]).verbose_name
            self.assertEquals(field_label, test_item["label_name"])

    def test_max_length(self):
        """Tests a series of fields for proper max length"""
        test_list = [
            {"field_name": "name", "max_length": 256},
            {"field_name": "address", "max_length": 1000},
            {"field_name": "city", "max_length": 1000},
            {"field_name": "province", "max_length": 100},
            {"field_name": "postal_code", "max_length": 10},
            {"field_name": "phone", "max_length": 20},
            {"field_name": "fax", "max_length": 20},
        ]

        for test_item in test_list:
            payee_payer = Demographics.objects.get(id=1)
            max_length = payee_payer._meta.get_field(test_item["field_name"]).max_length
            self.assertEquals(max_length, test_item["max_length"])

    def test_string_representation(self):
        payee_payer = Demographics.objects.get(id=1)
        self.assertEqual(str(payee_payer), payee_payer.name)

class CountryModelTest(TestCase):
    """Test functions for the Demographics model"""
    
    @classmethod
    def setUpTestData(cls):
        # Setup country data for testing
        Country.objects.create(country_code="CA", country_name="Canada")
        
    def test_country_verbose_name_plural(self):
        country = Country.objects.get(id=1)
        
        self.assertEquals(
            country._meta.verbose_name_plural, 
            "countries"
        )

    def test_country_code_label(self):
        country = Country.objects.get(id=1)
        
        self.assertEquals(
            country._meta.get_field("country_code").verbose_name, 
            "country code"
        )

    def test_country_name_label(self):
        country = Country.objects.get(id=1)
        
        self.assertEquals(
            country._meta.get_field("country_name").verbose_name, 
            "country name"
        )