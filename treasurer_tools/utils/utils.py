"""Functions to assist with unit and integration testing"""

from django.contrib.auth.models import User
from bank_reconciliation.models import ReconciliationMatch
from bank_transactions.models import Institution, Account, Statement, BankTransaction
from payee_payer.models import Country, Demographics
from transactions.models import Transaction, Item

def create_authentication_entries():
    # Create superuser
    superuser = User.objects.create(
        username="superuser",
        email="superuser@email.com"
    )
    superuser.set_password("abcd123456")
    superuser.is_superuser = True
    superuser.is_staff = True
    superuser.is_active = True
    superuser.save()

    # Create staff
    staff = User.objects.create(
        username="staff",
        email="staff@email.com"
    )
    staff.set_password("abcd123456")
    staff.is_superuser = False
    staff.is_staff = True
    staff.is_active = True
    staff.save()

    # Create regular user
    regular_user = User.objects.create(
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

def create_bank_transactions():
    statement_reference = create_bank_statement()

    bank_transaction_reference_1 = BankTransaction.objects.create(
        statement=statement_reference,
        date_transaction="2017-01-01",
        description_bank="CHQ#0001",
        description_user="Cheque #0001"
    )
    bank_transaction_reference_2 = BankTransaction.objects.create(
        statement=statement_reference,
        date_transaction="2017-01-02",
        description_bank="CHQ#0002",
        description_user="Cheque #0002"
    )
    bank_transaction_reference_3 = BankTransaction.objects.create(
        statement=statement_reference,
        date_transaction="2017-01-03",
        description_bank="DEP3333",
        description_user=""
    )
    bank_transaction_reference_4 = BankTransaction.objects.create(
        statement=statement_reference,
        date_transaction="2017-01-04",
        description_bank="DEP4444",
        description_user="Deposit from account #4444"
    )

    return [
        bank_transaction_reference_1,
        bank_transaction_reference_2,
        bank_transaction_reference_3,
        bank_transaction_reference_4,
    ]

def create_countries():
    country_reference_1 = Country.objects.create(
        country_code="CA",
        country_name="Canada",
    )
    country_reference_2 = Country.objects.create(
        country_code="US",
        country_name="United States",
    )
    country_reference_3 = Country.objects.create(
        country_code="AU",
        country_name="Australia",
    )

    return [
        country_reference_1,
        country_reference_2,
        country_reference_3,
    ]

def create_demographics():
    country_references = create_countries()

    demographic_reference = Demographics.objects.create(
        user=None,
        name="Test User",
        address="111-222 Fake Street",
        city="Edmonton",
        province="Alberta",
        country=country_references[0],
        postal_code="T1T 1T1",
        phone="111-222-3333",
        fax="444-555-6666",
        email="test@email.com",
        status="a"
    )

    return demographic_reference

def create_financial_transactions_and_items():
    demographic_reference = create_demographics()

    transaction_reference_1 = Transaction.objects.create(
        payee_payer=demographic_reference,
        transaction_type="e",
        memo="Test Expense Transaction 1",
        date_submitted="2017-06-01",
    )

    # Create associated items for transaction 1
    Item.objects.create(
        transaction=transaction_reference_1,
        date_item="2017-06-01",
        description="Taxi costs",
        amount=100.00,
        gst=5.00,
    )

    transaction_reference_2 = Transaction.objects.create(
        payee_payer=demographic_reference,
        transaction_type="r",
        memo="Test Revenue Transaction 1",
        date_submitted="2017-01-01",
    )

    # Create associated items for transaction 2
    Item.objects.create(
        transaction=transaction_reference_2,
        date_item="2017-01-01",
        description="Sponsorship",
        amount=950.00,
        gst=50.00,
    )

    transaction_reference_3 = Transaction.objects.create(
        payee_payer=demographic_reference,
        transaction_type="r",
        memo="Test Revenue Transaction 2",
        date_submitted="2017-01-05",
    )

    # Create associated items for transaction 3
    Item.objects.create(
        transaction=transaction_reference_3,
        date_item="2017-01-05",
        description="Funding",
        amount=500.00,
        gst=0.00,
    )

    transaction_reference_4 = Transaction.objects.create(
        payee_payer=demographic_reference,
        transaction_type="e",
        memo="Test Expense Transaction 2",
        date_submitted="2017-06-05",
    )

    # Create associated items for transaction 4
    Item.objects.create(
        transaction=transaction_reference_4,
        date_item="2017-06-04",
        description="Hotel",
        amount=129.99,
        gst=7.30,
    )

    return [
        transaction_reference_1,
        transaction_reference_2,
        transaction_reference_3,
        transaction_reference_4,
    ]

def create_reconciliation_matches():
    bank_transactions = create_bank_transactions()
    financial_transactions = create_financial_transactions_and_items()

    # create 1:1 match
    reconciliation_match_reference_1 = ReconciliationMatch.objects.create(
        bank_transaction=bank_transactions[0],
        financial_transaction=financial_transactions[0]
    )

    # create 2:1 match
    reconciliation_match_reference_2 = ReconciliationMatch.objects.create(
        bank_transaction=bank_transactions[1],
        financial_transaction=financial_transactions[1],
    )
    reconciliation_match_reference_3 = ReconciliationMatch.objects.create(
        bank_transaction=bank_transactions[2],
        financial_transaction=financial_transactions[1],
    )

    # create 1:2 match
    reconciliation_match_reference_4 = ReconciliationMatch.objects.create(
        bank_transaction=bank_transactions[3],
        financial_transaction=financial_transactions[2],
    )

    reconciliation_match_reference_5 = ReconciliationMatch.objects.create(
        bank_transaction=bank_transactions[3],
        financial_transaction=financial_transactions[3],
    )

    return [
        reconciliation_match_reference_1,
        reconciliation_match_reference_2,
        reconciliation_match_reference_3,
        reconciliation_match_reference_4,
        reconciliation_match_reference_5,
    ]