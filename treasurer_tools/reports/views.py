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

"""
@login_required
def retrieve_dates(request):
    # Retrieves a list of dates for code system
    # Get reference to the provided system ID
    system_id = request.GET.get("financial_code_system", None)
    system = get_object_or_404(FinancialCodeSystem, id=system_id)

    # Get all years
    system_year_start = system.date_start
    system_year_end = system.date_end if system.date_end else timezone.now()

    # Get all budget years
    budget_years = system.budgetyear_set.all().order_by("date_start")
    budget_year_dictionary = []

    for budget_year in budget_years:
        budget_year_dictionary.append({
            "start": budget_year.date_start,
            "end": budget_year.date_end
        })

    json_dates = {
        "system_year_start": system_year_start.strftime("%Y-%m-%d"),
        "system_year_end": system_year_end.strftime("%Y-%m-%d"),
        "budget_years": budget_year_dictionary,
    }

    return HttpResponse(
        json.dumps(json_dates, cls=DjangoJSONEncoder),
        content_type="application/json"
    )
"""

@login_required
def balance_sheet_dashboard(request):
    """Dashboard to generate balance sheet views"""
