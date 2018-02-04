"""View for the bank_transaction app"""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from bank_transactions.models import BankTransaction
from transactions.models import Transaction

from .utils import BankReconciliation


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
    transaction_type = request.GET.get("transaction_type", None)
    date_start = request.GET.get("date_start", None)
    date_end = request.GET.get("date_end", None)

    if date_start and date_end and transaction_type == "financial":
        try:
            transactions = Transaction.objects.filter(
                Q(date_submitted__gte=date_start) & Q(date_submitted__lte=date_end)
            )

            transaction_list = []
        
            for transaction in transactions:
                transaction_list.append({
                    "transaction": str(transaction),
                    "id": transaction.id,
                    "total": transaction.total,
                    "reconciled": transaction.rm_financial_transaction.all().exists()
                })

            json_data = {
                "data": transaction_list,
                "type": "financial"
            }
        except ValidationError:
            json_data = {}

    elif date_start and date_end and transaction_type == "bank":
        try:
            transactions = BankTransaction.objects.filter(
                Q(date_transaction__gte=date_start) & Q(date_transaction__lte=date_end)
            )

            transaction_list = []
        
            for transaction in transactions:
                transaction_list.append({
                    "transaction": str(transaction),
                    "id": transaction.id,
                    "debit": transaction.amount_debit,
                    "credit": transaction.amount_credit,
                    "reconciled": transaction.rm_bank_transaction.all().exists()
                })

            json_data = {
                "data": transaction_list,
                "type": "bank"
            }
        except ValidationError:
            json_data = {}
    else:
        json_data = {}
    
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
