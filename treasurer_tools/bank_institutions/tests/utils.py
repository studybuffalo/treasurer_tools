"""Functions to assist with unit and integration testing"""

from django.contrib.auth import get_user_model

from bank_institutions.models import Institution, Account

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

def create_bank_institution():
    institution_reference = Institution.objects.create(
        name="Test Institution",
        address="1234 Bank Street",
        phone="777-888-9999",
        fax="999-888-7777",
    )

    return institution_reference

def create_bank_account():
    institution_reference = create_bank_institution()
    
    account_reference = Account.objects.create(
        institution=institution_reference,
        account_number="123456789",
        name="Chequing Account",
        status="a",
    )
    
    return account_reference