"""Views for the transactions app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import TransactionForm, ItemFormSet
from .models import Transaction, Item
from financial_codes.models import FinancialCodeSystem

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
    def retrieve_financial_code_systems():
        return FinancialCodeSystem.objects.return_json_data()

    # POST request - try and save data
    if request.method == "POST":
        # Create form with POST data
        form = TransactionForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # Get a reference to the future saved form
            saved_form = form.save(commit=False)

            # Use POST data & form reference to populate formset
            formsets = ItemFormSet(request.POST, instance=saved_form)

            # If formsets are valid, save transaction and items
            if formsets.is_valid():
                saved_form.save()
                formsets.save()
                
                # Redirect to a new URL:
                messages.success(request, "Expense successfully added")

                return HttpResponseRedirect(reverse("transactions_dashboard"))
        else:
            # Form is not valid, so can generate formset without instance
            formsets = ItemFormSet(request.POST)

            # Set up the financial code systems dictionary
            financial_code_systems = retrieve_financial_code_systems()

    # GET request - generate blank form and formset
    else:
        form = TransactionForm()
        formsets = ItemFormSet()

        # Disable delete function
        formsets.can_delete = False
        
        # Set up the financial code systems dictionary
        financial_code_systems = retrieve_financial_code_systems()

    return render(
        request,
        "transactions/add.html",
        {
            "form": form,
            "formsets": formsets,
            "financial_code_systems": financial_code_systems,
            "page_name": t_type,
            "legend_title": "Transaction items",
            "formset_button": "Add item",
        },
    )

@login_required
def transaction_edit(request, t_type, transaction_id):
    """Generate and processes form to edit a financial system"""

     # POST request - try and save data
    if request.method == "POST":
        # Get the Transaction object by the provided ID
        transaction_data = get_object_or_404(Transaction, id=transaction_id)

        # Create form with POST data
        form = TransactionForm(request.POST, instance=transaction_data)

        # Check if the form is valid:
        if form.is_valid():
            # Get a reference to the future saved form
            saved_form = form.save(commit=False)

            # Use POST data & form reference to populate formset
            formsets = ItemFormSet(request.POST, instance=saved_form)

            # If formsets are valid, save transaction and items
            if formsets.is_valid():
                saved_form.save()
                formsets.save()
                
                # Redirect to a new URL:
                messages.success(request, "Expense successfully added")

                return HttpResponseRedirect(reverse("transactions_dashboard"))
        else:
            # Form is not valid, so can generate formset without instance
            formsets = ItemFormSet(request.POST)

    # GET request - generate blank form and formset
    else:
        # Get the Transaction object by the provided ID
        transaction_data = get_object_or_404(Transaction, id=transaction_id)

        # Create the form and formsets with the transaction object
        form = TransactionForm(instance=transaction_data)
        formsets = ItemFormSet(instance=transaction_data)

    return render(
        request,
        "transactions/edit.html",
        {
            "form": form,
            "formsets": formsets,
            "page_name": t_type,
            "legend_title": "Transaction items",
            "formset_button": "Add item",
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
