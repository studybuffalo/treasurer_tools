"""Views for the transactions app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

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
    def __assemble_forms(self, formsets, post_data):
        """Assemble the item formsets and financial code forms"""
        # Cycle through each item's inline formset
        forms = []
        item_id = 0

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

            for system in financial_code_systems:
                # Setup the proper prefix for the form fields
                prefix = "item_set-{}-coding_set-{}".format(item_id, form_id)
                    
                financial_code_form = FinancialCodeAssignmentForm(
                    post_data,
                    prefix=prefix,
                    system=system,
                )
                print("Prefix = {}".format(prefix))
                print("Data = {}".format(post_data))
                print("Code = {}".format(financial_code_form["code"].value()))
                print("Bound = {}".format(financial_code_form.is_bound))
                print("Valid = {}".format(financial_code_form.is_valid()))
                    
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
            item_id = item_id + 1

        return forms

    def is_valid(self):
        """Checks if all item formsets & financial code forms are valid"""
        valid = True

        for group in self.forms:
            if group["item_formset"].is_valid() == False:
                valid = False

            for financial_code_form in group["financial_code_forms"]:
                if financial_code_form["form"].is_valid() == False:
                    valid = False

        return valid
            
    def __init__(self, formsets, post_data={}):
        self.forms = self.__assemble_forms(formsets, post_data)
            
@login_required
def transaction_add(request, t_type):
    """Generates and processes form to add a transaction"""
    def save_financial_code_match(item_id, financial_code_id):
        """Saves an item-financial code match"""
        # Get reference to each model
        match_item = Item.objects.get(id=item_id)
        match_code = FinancialCode.objects.get(id=financial_code_id)

        # Saves the financial code meatch
        match = FinancialCodeMatch(
            item=match_item,
            financial_code=match_code
        )
        match.save()
                    
    # POST request - try and save data
    if request.method == "POST":
        # Create form with POST data
        transaction_form = TransactionForm(request.POST)

        # Check if the form is valid:
        if transaction_form.is_valid():
            # Get a reference to the future saved form
            saved_transaction = transaction_form.save(commit=False)

            # Use POST data & form reference to populate formset
            item_formsets = ItemFormSet(request.POST, instance=saved_transaction)

            # Check if the formsets are valid
            if item_formsets.is_valid():
                # Assemble a compiled item & financial code forms object
                compiled_forms = CompiledItemForms(item_formsets, request.POST)

                if compiled_forms.is_valid():
                    # All forms are valid, may start saving entries
                    saved_transaction.save()
                    
                    # Cycle through & save each item + financial code matches
                    for form in compiled_forms.forms:
                        saved_item = form["item_formset"].save(commit=False)
                        saved_item.transaction = Transaction.objects.get(id=saved_transaction.id)
                        saved_item.save()

                        for code_form in form["financial_code_forms"]:
                            save_financial_code_match(
                                saved_item.id,
                                code_form["form"].cleaned_data["code"]
                            )
                    # Redirect to a new URL:
                    messages.success(request, "Expense successfully added")

                    return HttpResponseRedirect(reverse("transactions_dashboard"))
            else:
                # Form is not valid, so can generate formset without instance
                compiled_forms = CompiledItemForms(item_formsets, request.POST)
        else:
            # Form is not valid, so can generate formset without instance
            item_formsets = ItemFormSet(request.POST)
            item_formsets.can_delete = False
            compiled_forms = CompiledItemForms(item_formsets, request.POST)

    # GET request - generate blank form and formset
    else:
        transaction_form = TransactionForm()

        item_formsets = ItemFormSet()
        item_formsets.can_delete = False

        compiled_forms = CompiledItemForms(item_formsets)
        
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
