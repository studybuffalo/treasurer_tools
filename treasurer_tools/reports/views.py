"""Views for the reports app"""

from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum
from django.shortcuts import render

from financial_codes.models import FinancialCodeSystem, FinancialCode


@login_required
def dashboard(request):
    """Main dashboard to view reports"""
    return render(
        request,
        "reports/index.html",
        context={},
    )

@login_required
def income_statement_dashboard(request):
    """Dashboard to generate account summary views"""

    return render(
        request,
        "reports/income_statement.html",
        context={
            "financial_code_systems": FinancialCodeSystem.objects.all(),
            "date_years": [1],
            "date_budget_years": [2],
            "date_months": [3],
        },
    )

@login_required
def retrieve_income_statement(request):
    """Retrieves data for account summary report"""

    financial_code_system = request.GET.get("financial_code_system", None)
    date_start = request.GET.get("date_start", None)
    date_end = request.GET.get("date_end", None)

    if all([financial_code_system, date_start, date_end]):
        revenue_code_totals = FinancialCode.objects.values("code", "description").filter(
            Q(financial_code_group__budget_year__financial_code_system__id=financial_code_system)
            & Q(financial_code_group__type="r")
            & Q(financialcodematch__item__transaction__date_submitted__gte=date_start)
            & Q(financialcodematch__item__transaction__date_submitted__lte=date_end)
        ).annotate(
            total=Sum("financialcodematch__item__amount") + Sum("financialcodematch__item__gst")
        )

        expense_code_totals = FinancialCode.objects.values("code", "description").filter(
            Q(financial_code_group__budget_year__financial_code_system__id=financial_code_system)
            & Q(financial_code_group__type="e")
            & Q(financialcodematch__item__transaction__date_submitted__gte=date_start)
            & Q(financialcodematch__item__transaction__date_submitted__lte=date_end)
        ).annotate(
            total=Sum("financialcodematch__item__amount") + Sum("financialcodematch__item__gst")
        )
    else:
        revenue_code_totals = None
        expense_code_totals = None

    return render(
        request,
        "reports/income_statement_report.html",
        context={
            "revenue_codes": revenue_code_totals,
            "expense_codes": expense_code_totals,
        }
    )

@login_required
def retrieve_balance_sheet(request):
    """Retrieves data for the balance sheet report"""

    return render(
        request,
        "reports/balance_sheet_report.html",
        context={
        }
    )

@login_required
def balance_sheet_dashboard(request):
    """Dashboard to generate balance sheet views"""

    return render(
        request,
        "reports/balance_sheet.html",
        context={
        },
    )
