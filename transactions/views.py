"""Views for the transactions app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import CompiledForms
from .models import Transaction

@login_required
def dashboard(request):
    """Main dashboard to expenses and revenue"""
    # pylint: disable=no-member
    transactions = Transaction.objects.all()

    return render(
        request,
        "transactions/index.html",
        context={
            "transactions": transactions,
        },
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

            return HttpResponseRedirect(reverse("transactions_dashboard"))
    # GET request - generate blank form and formset
    else:
        compiled_forms = CompiledForms(
            t_type, "GET", request.POST, request.FILES,
        )

    return render(
        request,
        "transactions/add.html",
        {
            "forms": compiled_forms,
            "page_name": t_type,
            "formset_button": "Add item",
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

            return HttpResponseRedirect(reverse("transactions_dashboard"))
    # GET request - generate blank form and formset
    else:
        compiled_forms = CompiledForms(
            t_type, "GET", request.POST, request.FILES, transaction_id=transaction_id,
        )

    return render(
        request,
        "transactions/edit.html",
        {
            "forms": compiled_forms,
            "page_name": t_type,
        },
    )

@login_required
def transaction_delete(request, t_type, transaction_id):
    """Generates and handles delete requests of a transaction"""

    # Get the Transaction instance
    transaction = get_object_or_404(Transaction, id=transaction_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        transaction.delete()

        # Redirect back to main list
        messages.success(request, "Transaction deleted")

        return HttpResponseRedirect(reverse("transactions_dashboard"))

    return render(
        request,
        "transactions/delete.html",
        {
            "page_name": t_type,
            "delete_message": t_type,
            "item_to_delete": transaction,
        },
    )

@login_required
def retrieve_financial_code_systems(request):
    """Retrieves all financial code systems active on provided date"""
    form_object = CompiledForms()
    transaction_date = request.GET.get("item_date", None)
    item_form_id = request.GET.get("item_form_id", None)

    return render(
        request,
        "transactions/financial_code_systems.html",
        context={
            "financial_code_forms" : form_object.create_financial_code_forms(
                item_form_id, None, transaction_date=transaction_date
            ),
        },
    )
    