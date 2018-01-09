"""Views for the transactions app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from .forms import TransactionForm, ItemFormSet, FinancialCodeAssignmentForm
from .models import Transaction, Item, FinancialCodeMatch
from financial_codes.models import FinancialCodeSystem, FinancialCode

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

class CompiledItemForms(object):
    """Object holding item & related financial code forms & functions"""
    def __assemble_forms(self, transaction_type, formsets, post_data):
        """Assemble the item formsets and financial code forms"""
        # Cycle through each item's inline formset
        forms = []
        item_form_id = 0

        for item_formset in formsets:
            # Get the date assigned to this formset
            date_item = item_formset["date_item"].value()
        
            # Find all the systems encompassing the provided date
            financial_code_systems = FinancialCodeSystem.objects.filter(
                Q(date_start__lte=date_item),
                (Q(date_end=None) | Q(date_end__gte=date_item))
            )

            # Create a FinancialCodeAssignmentForm for each system
            financial_code_forms = []
            form_id = 0

            item_id = item_formset["id"].value()
            
            for system in financial_code_systems:
                # Setup the proper prefix for the form fields
                prefix = "item_set-{}-coding_set-{}".format(item_form_id, form_id)
                
                # Check for no post data and an item ID (i.e. an edit GET request)
                match_instance = None

                if not post_data and item_id:
                    match_instances = FinancialCodeMatch.objects.filter(item=Item.objects.get(id=item_id))
                    
                    if match_instances:
                        for match in match_instances:
                            budget_year = match.financial_code.financial_code_group.budget_year

                            if budget_year.financial_code_system.id == system.id:
                                match_instance = {
                                    "financial_code_match": match.id,
                                    "budget_year": budget_year.id,
                                    "code": match.financial_code.id,
                                }
                               
                    # Add the matched data into the initializing data
                    if match_instance:
                        data = {
                            "{}-financial_code_match_id".format(prefix): match_instance["financial_code_match"],
                            "{}-budget_year".format(prefix): match_instance["budget_year"],
                            "{}-code".format(prefix): match_instance["code"],
                        }
                else:
                    data = post_data

                financial_code_form = FinancialCodeAssignmentForm(
                    data,
                    prefix=prefix,
                    transaction_type=transaction_type,
                    system=system,
                )

                # Add the form and a system title to the list
                financial_code_forms.append({
                    "name": str(system),
                    "form": financial_code_form,
                })

                # Increment the form_id for the prefix
                form_id = form_id + 1

            # Add item formset & associated financial code forms to list
            forms.append({
                "item_formset": item_formset,
                "financial_code_forms": financial_code_forms,
            })

            # Increment the item_id for the prefix
            item_form_id = item_form_id + 1

        return forms

    def __assemble_empty_financial_code_form(self, transaction_type):
        """Assembles empty set of financial code forms (like .empty_form())"""
        # Set the item date as today
        date_item = timezone.now()

        # Find all the systems encompassing the provided date
        financial_code_systems = FinancialCodeSystem.objects.filter(
            Q(date_start__lte=date_item),
            (Q(date_end=None) | Q(date_end__gte=date_item))
        )

        # Create a FinancialCodeAssignmentForm for each system
        financial_code_forms = []
        form_id = 0

        for system in financial_code_systems:
            # Setup the proper prefix for the form fields
            prefix = "item_set-__prefix__-coding_set-{}".format(form_id)
            
            financial_code_forms.append({
                "name": str(system),
                "form": FinancialCodeAssignmentForm(
                    {},
                    prefix=prefix,
                    transaction_type=transaction_type,
                    system=system,
                ),
            })

            form_id = form_id + 1

        return financial_code_forms

    def is_valid(self):
        """Checks if all item formsets & financial code forms are valid"""
        valid = True
        item_formset_num = len(self.forms)

        for group in self.forms:
            # Check that each item formset is valid
            if group["item_formset"].is_valid() == False:
                valid = False
            else:
                # Check if marked for deletion
                if group["item_formset"].cleaned_data["DELETE"]:
                    item_formset_num = item_formset_num - 1

            # Check that each financial code form is valid
            for financial_code_form in group["financial_code_forms"]:
                if financial_code_form["form"].is_valid() == False:
                    valid = False

        if item_formset_num <= 0:
            valid = False

        return valid
            
    def save(self, transaction_id):
        # Cycle through & save each item + financial code matches
        for form in self.forms:
            item_formset = form["item_formset"]

            # Delete any form marked for deletion
            if item_formset.cleaned_data["DELETE"]:
                item_formset.cleaned_data["id"].delete()
            else:
                # Save the item formset
                saved_item = item_formset.save(commit=False)
                saved_item.transaction = Transaction.objects.get(id=transaction_id)
                saved_item.save()

                for code_form in form["financial_code_forms"]:
                    # Get any ID for an exisiting match ID
                    match_id = code_form["form"].cleaned_data["financial_code_match_id"]

                    # Get the item ID from the recently saved item
                    match_item = Item.objects.get(id=saved_item.id)

                    # If provided, get the financial code ID
                    match_code_id = code_form["form"].cleaned_data["code"]

                    if match_code_id:
                        match_code = FinancialCode.objects.get(id=match_code_id)
                    else:
                        match_code = None
                
                    # If an ID is present, get the original object
                    if match_id:
                        match = get_object_or_404(FinancialCodeMatch, id=match_id)
                    else:
                        match = FinancialCodeMatch()

                    # Saves the financial code match
                    match.item = match_item
                    match.financial_code = match_code
                    match.save()
                
    def __init__(self, transaction_type, formsets, post_data={}):
        self.forms = self.__assemble_forms(transaction_type, formsets, post_data)
        self.empty_financial_code_form = self.__assemble_empty_financial_code_form(transaction_type)
            
@login_required
def transaction_add(request, t_type):
    """Generates and processes form to add a transaction"""
    # POST request - try and save data
    if request.method == "POST":
        # Create form with POST data
        transaction_form = TransactionForm(request.POST)

        # Check if the form is valid:
        if transaction_form.is_valid():
            # Get a reference to the future saved form
            saved_transaction = transaction_form.save(commit=False)
            
            # Update the transaction_type
            saved_transaction.transaction_type = "e" if t_type == "expense" else "r"

            # Use POST data & form reference to populate formset
            item_formsets = ItemFormSet(request.POST, instance=saved_transaction)

            # Check if the formsets are valid
            if item_formsets.is_valid():
                # Assemble a compiled item & financial code forms object
                compiled_forms = CompiledItemForms(t_type, item_formsets, request.POST)

                if compiled_forms.is_valid():
                    # All forms are valid, save all three levels of forms
                    saved_transaction.save()
                    compiled_forms.save(saved_transaction.id)

                    # Redirect to a new URL:
                    messages.success(request, "Transaction successfully added")

                    return HttpResponseRedirect(reverse("transactions_dashboard"))
            else:
                # Form is not valid, so can generate formset without instance
                compiled_forms = CompiledItemForms(t_type, item_formsets, request.POST)
        else:
            # Form is not valid, so can generate formset without instance
            item_formsets = ItemFormSet(request.POST)
            item_formsets.can_delete = False
            compiled_forms = CompiledItemForms(t_type, item_formsets, request.POST)

    # GET request - generate blank form and formset
    else:
        transaction_form = TransactionForm()

        item_formsets = ItemFormSet()
        item_formsets.can_delete = False

        compiled_forms = CompiledItemForms(t_type, item_formsets)
        
    return render(
        request,
        "transactions/add.html",
        {
            "form": transaction_form,
            "formsets": item_formsets,
            "formsets_group": compiled_forms,
            "page_name": t_type,
            "formset_button": "Add item",
        },
    )

@login_required
def transaction_edit(request, t_type, transaction_id):
    """Generate and processes form to edit transactions"""
    # POST request - try and save data
    if request.method == "POST":
        # Get the Transaction object by the provided ID
        transaction_data = get_object_or_404(Transaction, id=transaction_id)

        # Create form with POST data
        transaction_form = TransactionForm(request.POST, instance=transaction_data)

        # Check if the form is valid:
        if transaction_form.is_valid():
            # Get a reference to the future saved form
            saved_transaction = transaction_form.save(commit=False)

            # Use POST data & form reference to populate formset
            item_formsets = ItemFormSet(request.POST, instance=saved_transaction)
            
            #if item_formsets.is_valid() or not item_formsets.has_changed()
            # Assemble a compiled item & financial code forms object
            compiled_forms = CompiledItemForms(t_type, item_formsets, request.POST)
            
            if compiled_forms.is_valid():
                # All forms are valid, save all three levels of forms
                saved_transaction.save()
                compiled_forms.save(saved_transaction.id)

                # Redirect to a new URL:
                messages.success(request, "Transaction successfully updated")

                return HttpResponseRedirect(reverse("transactions_dashboard"))
        else:
            # Form is not valid, so can generate formset without instance
            item_formsets = ItemFormSet(request.POST, instance=transaction_data)
            compiled_forms = CompiledItemForms(t_type, item_formsets, request.POST)

    # GET request - generate blank form and formset
    else:
        transaction_data = get_object_or_404(Transaction, id=transaction_id)

        transaction_form = TransactionForm(instance=transaction_data)
        item_formsets = ItemFormSet(instance=transaction_data)
        compiled_forms = CompiledItemForms(t_type, item_formsets)

    return render(
        request,
        "transactions/edit.html",
        {
            "form": transaction_form,
            "formsets": item_formsets,
            "formsets_group": compiled_forms,
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
