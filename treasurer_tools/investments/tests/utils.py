"""Functions to assist with unit and integration testing"""

from django.contrib.auth import get_user_model

from investments.models import Investment

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

def create_investment():
    investment_reference = Investment.objects.create(
        name="Term Deposit #1",
        rate="1% per anum"
    )

    return investment_reference
