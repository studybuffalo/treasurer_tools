"""Views for the reports app"""

import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.urls import reverse

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
def account_summary_dashboard(request):
    """Dashboard to generate account summary views"""

    return render(
        request,
        "reports/account_summary.html",
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
    
    try:
        system_id = request.GET.get("financial_code_system", None)
        print(system_id)
        system = FinancialCodeSystem.objects.get(id=system_id)
    except ValueError as e:
        system = None

    if system:
        budget_years = system.budgetyear_set.all()

        # Get all years

        # Get all budget years

        # Get all months

        json_dates = {
            "error": False,
            "test": "test"
        }
    else:
        json_dates = {
            "error": True
        }

    return HttpResponse(
        json.dumps(json_dates, cls=DjangoJSONEncoder), 
        content_type="application/json"
    )

@login_required
def retrieve_account_summary(request):
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
        "reports/account_summary_report.html",
        context={}
    )
@login_required
def balance_sheet_dashboard(request):
    """Dashboard to generate balance sheet views"""
