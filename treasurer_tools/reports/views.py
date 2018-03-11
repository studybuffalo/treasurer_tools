"""Views for the reports app"""

import json
from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.urls import reverse
from django.utils import timezone

from financial_codes.models import FinancialCodeSystem


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
def retrieve_dates(request):
    """Retrieves a list of dates for code system"""
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

@login_required
def retrieve_income_statement(request):
    """Retrieves data for account summary report"""

    financial_code_system = request.GET.get("financial_code_system", None)
    grouping = request.GET.get("grouping", None)
    date_start = request.GET.get("date_start", None)
    date_end = request.GET.get("date_end", None)

    if all([financial_code_system, grouping, date_start, date_end]):
        print("All valid")
    else:
        print("Not all valid")

    return render(
        request,
        "reports/income_statement_report.html",
        context={}
    )
@login_required
def balance_sheet_dashboard(request):
    """Dashboard to generate balance sheet views"""
