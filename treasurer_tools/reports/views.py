"""Views for the reports app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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

def account_summary_dashboard(request):
    """Dashboard to generate account summary views"""

    return render(
        request,
        "reports/account_summary.html",
        context={
            "financial_code_systems": FinancialCodeSystem.objects.all(),
        },
    )

def balance_sheet_dashboard(request):
    """Dashboard to generate balance sheet views"""
