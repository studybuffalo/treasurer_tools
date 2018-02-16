"""Functions to assist with unit and integration testing"""

from django.contrib.auth import get_user_model

from bank_institutions.models import Institution, Account
from bank_transactions.models import Statement, BankTransaction

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

def create_bank_statement():
    account_reference = create_bank_account()

    statement_reference = Statement.objects.create(
        account=account_reference,
        date_start="2017-01-01",
        date_end="2017-01-31"
    )

    return statement_reference


def create_bank_statement():
    account_reference = create_bank_account()

    statement_reference = Statement.objects.create(
        account=account_reference,
        date_start="2017-01-01",
        date_end="2017-01-31"
    )

    return statement_reference

def create_bank_transactions():
    statement_reference = create_bank_statement()

    bank_transaction_reference_1 = BankTransaction.objects.create(
        statement=statement_reference,
        date_transaction="2017-01-01",
        description_bank="CHQ#0001",
        description_user="Cheque #0001",
        amount_debit=100.00,
        amount_credit=0.00,
    )
    bank_transaction_reference_2 = BankTransaction.objects.create(
        statement=statement_reference,
        date_transaction="2017-01-02",
        description_bank="CHQ#0002",
        description_user="Cheque #0002",
        amount_debit=200.00,
        amount_credit=0.00,
    )
    bank_transaction_reference_3 = BankTransaction.objects.create(
        statement=statement_reference,
        date_transaction="2017-01-03",
        description_bank="DEP3333",
        description_user="",
        amount_debit=0.00,
        amount_credit=300.00,
    )
    bank_transaction_reference_4 = BankTransaction.objects.create(
        statement=statement_reference,
        date_transaction="2017-01-04",
        description_bank="DEP4444",
        description_user="Deposit from account #4444",
        amount_debit=0.00,
        amount_credit=400.00,
    )

    return [
        bank_transaction_reference_1,
        bank_transaction_reference_2,
        bank_transaction_reference_3,
        bank_transaction_reference_4,
    ]
