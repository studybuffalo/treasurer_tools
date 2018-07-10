"""Views for the transactions app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import CompiledForms
from .models import FinancialTransaction

@login_required
def dashboard(request):
    """Main dashboard to expenses and revenue"""
    return render(request, "transactions/index.html")


@login_required
def request_transactions_list(request):
    """Retrieves list of transactions"""
    # Get all transactions
    transactions = FinancialTransaction.objects.all().order_by("-date_submitted")

    # Filter by type
    transaction_type = request.GET.get("transaction_type", "a")

    if transaction_type == "e":
        transactions = transactions.filter(transaction_type="e")
    elif transaction_type == "r":
        transactions = transactions.filter(transaction_type="r")

    # Filter by date
    date_start = request.GET.get("date_start", None)
    date_end = request.GET.get("date_end", None)

    if date_start:
        transactions = transactions.filter(date_submitted__gte=date_start)

    if date_end:
        transactions = transactions.filter(date_submitted__lte=date_end)

    return render(
        request,
        "transactions/transactions.html",
        context={
            "transactions": transactions
        }
    )

@login_required
def transaction_add(request, t_type):
    """Generates and processes form to add a transaction"""
    # POST request - try and save data
    if request.method == "POST":
        compiled_forms = CompiledForms(t_type, "POST", request.POST, request.FILES)

        if compiled_forms.is_valid():
            compiled_forms.save()

            # Redirect to a new URL:
            messages.success(request, "Transaction successfully added")

            return HttpResponseRedirect(reverse("financial_transactions:dashboard"))
    # GET request - generate blank form and formset
    else:
        compiled_forms = CompiledForms(
            t_type, "GET", request.POST, request.FILES,
        )

    return render(
        request,
        "transactions/add_edit.html",
        {
            "forms": compiled_forms,
            "page_name": "Add new {}".format(t_type),
            "type": "add",
        },
    )

@login_required
def transaction_edit(request, t_type, transaction_id):
    """Generate and processes form to edit transactions"""
    # POST request - try and save data
    if request.method == "POST":
        compiled_forms = CompiledForms(
            t_type, "POST", request.POST, request.FILES, transaction_id=transaction_id
        )

        if compiled_forms.is_valid():
            compiled_forms.save()

            # Redirect to a new URL:
            messages.success(request, "Transaction successfully edited")

            return HttpResponseRedirect(reverse("financial_transactions:dashboard"))
    # GET request - generate blank form and formset
    else:
        compiled_forms = CompiledForms(
            t_type, "GET", request.POST, request.FILES, transaction_id=transaction_id,
        )

    return render(
        request,
        "transactions/add_edit.html",
        {
            "forms": compiled_forms,
            "page_name": "Edit {}".format(t_type),
            "type": "edit",
        },
    )

@login_required
def transaction_delete(request, t_type, transaction_id):
    """Generates and handles delete requests of a transaction"""

    # Get the Transaction instance
    transaction = get_object_or_404(FinancialTransaction, id=transaction_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        transaction.delete()

        # Redirect back to main list
        messages.success(request, "Transaction deleted")

        return HttpResponseRedirect(reverse("financial_transactions:dashboard"))

    return render(
        request,
        "transactions/delete.html",
        {
            "page_name": t_type,
            "delete_message": t_type,
            "item_to_delete": transaction,
        },
    )
