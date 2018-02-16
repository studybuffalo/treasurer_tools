"""Functions to assist with unit and integration testing"""

from django.contrib.auth import get_user_model

from bank_institutions.models import Institution, Account
from bank_transactions.models import Statement

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

def create_bank_statement():
    account_reference = create_bank_account()

    statement_reference = Statement.objects.create(
        account=account_reference,
        date_start="2017-01-01",
        date_end="2017-01-31"
    )

    return statement_reference
