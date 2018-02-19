"""Functions to assist with unit and integration testing"""

from django.contrib.auth import get_user_model

from financial_codes.models import FinancialCodeSystem, BudgetYear, FinancialCodeGroup, FinancialCode


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
        ),
        FinancialCodeSystem.objects.create(
            title="Regional",
            date_start="2000-01-01",
            date_end="2015-12-31",
        ),
    ]

    return system_references

def create_budget_year():
    systems = create_financial_code_systems()

    year_reference = BudgetYear.objects.create(
        financial_code_system=systems[0],
        date_start="2017-01-01",
        date_end="2017-12-31",
    )

    return year_reference

def create_financial_code_groups():
    year = create_budget_year()

    group_references = [
        FinancialCodeGroup.objects.create(
            budget_year=year,
            title="Awards & Grants",
            description="Expenses for awards & grants",
            type="e",
            status="a",
        ),
        FinancialCodeGroup.objects.create(
            budget_year=year,
            title="Awards & Grants",
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
    ]

    return code_references
