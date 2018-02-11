"""View for the bank_transaction app"""

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .utils import return_transactions_as_json, BankReconciliation


@login_required
def dashboard(request):
    """Page to handle bank reconciliation"""
    # pylint: disable=no-member

    return render(
        request,
        "bank_reconciliation/index.html",
        context={},
    )

@login_required
def retrieve_transactions(request):
    """Retrieves and returns all transactions in provided date range"""
    # pylint: disable=no-member
    json_data = return_transactions_as_json(request)

    return JsonResponse(json_data)

@login_required
def match_transactions(request):
    """Matches financial and banking transactions (if valid)"""
    reconciliation = BankReconciliation(request.body, "match")

    # Check if provided data is valid
    if reconciliation.is_valid():
        # Make reconcilation matches
        reconciliation.create_matches()

    return JsonResponse({
        "success": reconciliation.success,
        "errors": reconciliation.errors,
    })

@login_required
def unmatch_transactions(request):
    """Unmatches financial and banking transactions (if valid)"""
    reconciliation = BankReconciliation(request.body, "unmatch")

    # Check if provided data is valid
    if reconciliation.is_valid():
        # Make reconcilation matches
        reconciliation.delete_matches()

    return JsonResponse({
        "success": reconciliation.success,
        "errors": reconciliation.errors,
    })
