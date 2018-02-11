"""Functions to assist with unit and integration testing"""

#from django.contrib.auth import get_user_model

#from bank_transactions.models import Institution, Account, Statement, BankTransaction
#from payee_payers.models import Country, PayeePayer
#from financial_transactions.models import FinancialTransaction, Item

#def create_user():
#    # Create regular user
#    regular_user = get_user_model().objects.create(
#        username="user",
#        email="user@email.com"
#    )
#    regular_user.set_password("abcd123456")
#    regular_user.is_superuser = False
#    regular_user.is_staff = False
#    regular_user.is_active = True
#    regular_user.save()

#def create_bank_institution():
#    institution_reference = Institution.objects.create(
#        name="Test Institution",
#        address="1234 Bank Street",
#        phone="777-888-9999",
#        fax="999-888-7777",
#    )

#    return institution_reference

#def create_bank_account():
#    institution_reference = create_bank_institution()

#    account_reference = Account.objects.create(
#        institution=institution_reference,
#        account_number="123456789",
#        name="Chequing Account",
#        status="a",
#    )

#    return account_reference

#def create_bank_statement():
#    account_reference = create_bank_account()

#    statement_reference = Statement.objects.create(
#        account=account_reference,
#        date_start="2017-01-01",
#        date_end="2017-01-31"
#    )

#    return statement_reference

#def create_bank_transactions():
#    statement_reference = create_bank_statement()

#    bank_transaction_reference_1 = BankTransaction.objects.create(
#        statement=statement_reference,
#        date_transaction="2017-01-01",
#        description_bank="CHQ#0001",
#        description_user="Cheque #0001"
#    )
#    bank_transaction_reference_2 = BankTransaction.objects.create(
#        statement=statement_reference,
#        date_transaction="2017-01-02",
#        description_bank="CHQ#0002",
#        description_user="Cheque #0002"
#    )
#    bank_transaction_reference_3 = BankTransaction.objects.create(
#        statement=statement_reference,
#        date_transaction="2017-01-03",
#        description_bank="DEP3333",
#        description_user=""
#    )
#    bank_transaction_reference_4 = BankTransaction.objects.create(
#        statement=statement_reference,
#        date_transaction="2017-01-04",
#        description_bank="DEP4444",
#        description_user="Deposit from account #4444"
#    )

#    return [
#        bank_transaction_reference_1,
#        bank_transaction_reference_2,
#        bank_transaction_reference_3,
#        bank_transaction_reference_4,
#    ]

#def create_country():
#    country_reference = Country.objects.create(
#        country_code="CA",
#        country_name="Canada",
#    )

#    return country_reference

#def create_demographics():
#    country_reference = create_country()

#    demographic_reference = PayeePayer.objects.create(
#        user=None,
#        name="Test User",
#        address="111-222 Fake Street",
#        city="Edmonton",
#        province="Alberta",
#        country=country_reference,
#        postal_code="T1T 1T1",
#        phone="111-222-3333",
#        fax="444-555-6666",
#        email="test@email.com",
#        status="a"
#    )

#    return demographic_reference

#def create_financial_transactions():
#    demographic_reference = create_demographics()

#    transaction_reference_1 = FinancialTransaction.objects.create(
#        payee_payer=demographic_reference,
#        transaction_type="e",
#        memo="Test Expense Transaction 1",
#        date_submitted="2017-06-01",
#    )

#    # Create associated items for transaction 1
#    Item.objects.create(
#        transaction=transaction_reference_1,
#        date_item="2017-06-01",
#        description="Taxi costs",
#        amount=100.00,
#        gst=5.00,
#    )

#    transaction_reference_2 = FinancialTransaction.objects.create(
#        payee_payer=demographic_reference,
#        transaction_type="r",
#        memo="Test Revenue Transaction 1",
#        date_submitted="2017-01-01",
#    )

#    # Create associated items for transaction 2
#    Item.objects.create(
#        transaction=transaction_reference_2,
#        date_item="2017-01-01",
#        description="Sponsorship",
#        amount=950.00,
#        gst=50.00,
#    )

#    transaction_reference_3 = FinancialTransaction.objects.create(
#        payee_payer=demographic_reference,
#        transaction_type="r",
#        memo="Test Revenue Transaction 2",
#        date_submitted="2017-01-05",
#    )

#    # Create associated items for transaction 3
#    Item.objects.create(
#        transaction=transaction_reference_3,
#        date_item="2017-01-05",
#        description="Funding",
#        amount=500.00,
#        gst=0.00,
#    )

#    transaction_reference_4 = FinancialTransaction.objects.create(
#        payee_payer=demographic_reference,
#        transaction_type="e",
#        memo="Test Expense Transaction 2",
#        date_submitted="2017-06-05",
#    )

#    # Create associated items for transaction 4
#    Item.objects.create(
#        transaction=transaction_reference_4,
#        date_item="2017-06-04",
#        description="Hotel",
#        amount=129.99,
#        gst=7.30,
#    )

#    return [
#        transaction_reference_1,
#        transaction_reference_2,
#        transaction_reference_3,
#        transaction_reference_4,
#    ]
