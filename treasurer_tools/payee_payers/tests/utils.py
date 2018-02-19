"""Functions to assist with unit and integration testing"""

from django.contrib.auth import get_user_model

from payee_payers.models import Country, PayeePayer

def create_user():
    # Create regular user
    regular_user = get_user_model().objects.create(
        username="user",
        email="user@email.com"
    )
    regular_user.set_password("abcd123456")
    regular_user.is_superuser = False
    regular_user.is_staff = False
    regular_user.is_active = True
    regular_user.save()

def create_country():
    country_reference = Country.objects.create(
        country_code="CA",
        country_name="Canada",
    )

    return country_reference

def create_demographics():
    country_reference = create_country()

    demographic_reference = PayeePayer.objects.create(
        user=None,
        name="Test User",
        address="111-222 Fake Street",
        city="Edmonton",
        province="Alberta",
        country=country_reference,
        postal_code="T1T 1T1",
        phone="111-222-3333",
        fax="444-555-6666",
        email="test@email.com",
        status="a"
    )

    return demographic_reference
