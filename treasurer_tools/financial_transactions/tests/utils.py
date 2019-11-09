"""Functions to assist with unit and integration testing"""

from django.contrib.auth import get_user_model

from financial_codes.models import FinancialCodeSystem, BudgetYear, FinancialCodeGroup, FinancialCode
from financial_transactions.models import FinancialTransaction, Item, FinancialCodeMatch
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

def create_financial_code_systems():
    system_references = [
        FinancialCodeSystem.objects.create(
            title="National",
            date_start="2010-01-01",
            date_end=None,
            submission_code=True
        ),
        FinancialCodeSystem.objects.create(
            title="Regional",
            date_start="2000-01-01",
            date_end="2020-12-31",
            submission_code=False,
        ),
    ]

    return system_references

def create_budget_years():
    systems = create_financial_code_systems()

    year_references = [
        BudgetYear.objects.create(
            financial_code_system=systems[0],
            date_start="2017-01-01",
            date_end="2017-12-31",
        ),
        BudgetYear.objects.create(
            financial_code_system=systems[1],
            date_start="2017-01-01",
            date_end="2017-12-31",
        ),
    ]

    return year_references

def create_financial_code_groups():
    years = create_budget_years()

    group_references = [
        FinancialCodeGroup.objects.create(
            budget_year=years[0],
            title="National Awards & Grants",
            description="Expenses for awards & grants",
            type="e",
            status="a",
        ),
        FinancialCodeGroup.objects.create(
            budget_year=years[0],
            title="National Awards & Grants",
            description="Revenue for awards & grants",
            type="r",
            status="a",
        ),
        FinancialCodeGroup.objects.create(
            budget_year=years[1],
            title="Regional Awards & Grants",
            description="Expenses for awards & grants",
            type="e",
            status="a",
        ),
        FinancialCodeGroup.objects.create(
            budget_year=years[1],
            title="Regional Awards & Grants",
            description="Revenue for awards & grants",
            type="r",
            status="a",
        )
    ]

    return group_references

def create_financial_codes():
    groups = create_financial_code_groups()

    code_references = [
        FinancialCode.objects.create(
            financial_code_group=groups[0],
            code="1000",
            description="Travel Grant"
        ),
        FinancialCode.objects.create(
            financial_code_group=groups[1],
            code="6000",
            description="Travel Grant Sponsorship"
        ),
        FinancialCode.objects.create(
            financial_code_group=groups[2],
            code="2000",
            description="Travel Grant"
        ),
        FinancialCode.objects.create(
            financial_code_group=groups[3],
            code="8000",
            description="Travel Grant Sponsorship"
        ),
    ]

    return code_references

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

def create_financial_transactions():
    demographic_reference = create_demographics()
    codes = create_financial_codes()

    # Create Transaction 1
    transaction_reference_1 = FinancialTransaction.objects.create(
        payee_payer=demographic_reference,
        transaction_type="e",
        memo="Test Expense Transaction 1",
        date_submitted="2017-06-01",
    )

    # Create associated items for transaction 1
    transaction_1_item_1 = Item.objects.create(
        transaction=transaction_reference_1,
        date_item="2017-06-01",
        description="Taxi costs (to hotel)",
        amount=100.00,
        gst=5.00,
    )

    transaction_1_item_2 = Item.objects.create(
        transaction=transaction_reference_1,
        date_item="2017-06-01",
        description="Taxi costs (from hotel)",
        amount=100.00,
        gst=5.00,
    )

    # Create financial code matches for transaction 1
    FinancialCodeMatch.objects.create(
        item=transaction_1_item_1,
        financial_code=codes[0]
    )

    FinancialCodeMatch.objects.create(
        item=transaction_1_item_1,
        financial_code=codes[2]
    )

    FinancialCodeMatch.objects.create(
        item=transaction_1_item_2,
        financial_code=codes[0]
    )

    FinancialCodeMatch.objects.create(
        item=transaction_1_item_2,
        financial_code=codes[2]
    )

    # Create Transaction 2
    transaction_reference_2 = FinancialTransaction.objects.create(
        payee_payer=demographic_reference,
        transaction_type="r",
        memo="Test Revenue Transaction 1",
        date_submitted="2017-01-01",
    )

    # Create associated items for transaction 2
    transaction_2_item = Item.objects.create(
        transaction=transaction_reference_2,
        date_item="2017-01-01",
        description="Sponsorship",
        amount=950.00,
        gst=50.00,
    )

    # Create financial code matches for transaction 2
    FinancialCodeMatch.objects.create(
        item=transaction_2_item,
        financial_code=codes[1]
    )

    FinancialCodeMatch.objects.create(
        item=transaction_2_item,
        financial_code=codes[3]
    )

    # Create Transaction 3
    transaction_reference_3 = FinancialTransaction.objects.create(
        payee_payer=demographic_reference,
        transaction_type="r",
        memo="Test Revenue Transaction 2",
        date_submitted="2017-01-05",
    )

    # Create associated items for transaction 3
    transaction_3_item = Item.objects.create(
        transaction=transaction_reference_3,
        date_item="2017-01-05",
        description="Funding",
        amount=500.00,
        gst=0.00,
    )

    # Create financial code matches for transaction 3
    FinancialCodeMatch.objects.create(
        item=transaction_3_item,
        financial_code=codes[1]
    )

    FinancialCodeMatch.objects.create(
        item=transaction_3_item,
        financial_code=codes[3]
    )

    # Create Transaction 4
    transaction_reference_4 = FinancialTransaction.objects.create(
        payee_payer=demographic_reference,
        transaction_type="e",
        memo="Test Expense Transaction 2",
        date_submitted="2017-06-05",
    )

    # Create associated items for transaction 4
    transaction_4_item = Item.objects.create(
        transaction=transaction_reference_4,
        date_item="2017-06-04",
        description="Hotel",
        amount=129.99,
        gst=7.30,
    )

    # Create financial code matches for transaction 4
    FinancialCodeMatch.objects.create(
        item=transaction_4_item,
        financial_code=codes[0]
    )

    FinancialCodeMatch.objects.create(
        item=transaction_4_item,
        financial_code=codes[2]
    )

    return [
        transaction_reference_1,
        transaction_reference_2,
        transaction_reference_3,
        transaction_reference_4,
    ]
