"""View for the bank_reconciliation app"""
import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render

from .models import ReconciliationGroup
from .utils import return_transactions_as_json, return_matches_as_json, BankReconciliation


@login_required
def dashboard(request):
    """Page to handle bank reconciliation"""

    return render(
        request,
        "bank_reconciliation/index.html",
        context={},
    )

@login_required
def retrieve_transactions(request):
    """Retrieves and returns all transactions in provided date range"""

    json_data = return_transactions_as_json(request)

    return JsonResponse(json_data)

@login_required
def match_transactions(request):
    """Matches financial and banking transactions (if valid)"""
    reconciliation = BankReconciliation(request.body)

    # Check if provided data is valid
    if reconciliation.is_valid():
        # Make reconcilation matches
        reconciliation.create_matches()

    return JsonResponse({
        "success": reconciliation.success,
        "errors": reconciliation.errors,
    })

@login_required
def retrieve_matches(request):
    json_data = return_matches_as_json(request)

    return JsonResponse(json_data)

@login_required
def unmatch_transactions(request):
    """Unmatches financial and banking transactions (if valid)"""
    # Setup variable to handle errors
    errors = []

    # Attemps to convert data to a dictionary
    try:
        request_data = json.loads(request.body)
        ids = request_data['reconciliation_group_ids']
    except (ValueError, KeyError) as e:
        errors.append({"post_data": "Invalid data submitted to server: {}".format(e)})
        ids = []

    # Get each provided ID and delete the repesctive group
    for group_id in ids:
        try:
            group = ReconciliationGroup.objects.get(id=group_id)
            group.delete()
        except ReconciliationGroup.DoesNotExist:
            errors.append({"ids": "Provided ID ({}) does not exist".format(group_id)})
        except ValueError:
            errors.append({"ids": "Provided ID ({}) is on wrong format".format(group_id)})

    return JsonResponse({
        "errors": errors,
    })
