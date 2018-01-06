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

@login_required
def transaction_add(request, t_type):
    """Generates and processes form to add a transaction"""
    def extract_financial_code_assignment_values(data, prefix):
        """"""
        if data:
            budget_year_key = "{}-budget_year".format(prefix)
            code_key = "{}-code".format(prefix)
            
            return {
                "budget_year": data[budget_year_key],
                "code": data[code_key],
            }
        else:
            return None

    def assemble_financial_code_forms(formsets, post_data=[]):
        """"""
        # Cycle through formsets and assemble financial code forms
        code_forms = []
        is_valid = True
        item_id = 0

        for formset in formsets:
            # Get the date assigned to this formset
            date_item = formset["date_item"].value()
        
            # Find all the systems encompassing the provided date
            systems = FinancialCodeSystem.objects.filter(
                Q(date_start__lte=date_item),
                (Q(date_end=None) | Q(date_end__gte=date_item))
            )

            # Assemble each required form
            code_forms_for_single_item = []
            form_id = 0

            for system in systems:
                prefix = "item_set-{}-coding_set-{}".format(item_id, form_id)
                post_dictionary = extract_financial_code_assignment_values(
                    post_data, prefix
                )
                
                code_form = FinancialCodeAssignmentForm(
                    post_dictionary,
                    prefix=prefix,
                    system=system,
                )
                
                if code_form.is_valid() == False:
                    is_valid = False

                code_forms_for_single_item.append({
                    "name": str(system),
                    "form": code_form,
                })

                form_id = form_id + 1


            code_forms.append({
                "formset": formset,
                "code_forms": code_forms_for_single_item,
            })

            item_id = item_id + 1

        return {
            "forms": code_forms,
            "is_valid": is_valid,
        }

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

            # Check if the formsets are valid
            if formsets.is_valid():
                financial_code_forms = assemble_financial_code_forms(formsets, request.POST)

                if financial_code_forms["is_valid"]:
                    saved_form.save()
                    
                    for code_forms in financial_code_forms["forms"]:
                        saved_formset = code_forms["formset"].save(commit=False)
                        saved_formset.transaction = Transaction.objects.get(id=saved_form.id)
                        saved_formset.save()

                        for code_form in code_forms["code_forms"]:
                            # Get reference to each model
                            match_item = Item.objects.get(id=saved_formset.id)
                            match_code = FinancialCode.objects.get(
                                id=int(code_form["form"].cleaned_data["code"])
                            )

                            # Saves each financial code match
                            match = FinancialCodeMatch(
                                item=match_item,
                                financial_code=match_code
                            )
                            match.save()
                    
                    # Redirect to a new URL:
                    messages.success(request, "Expense successfully added")

                    return HttpResponseRedirect(reverse("transactions_dashboard"))
            else:
                # Form is not valid, so can generate formset without instance
                financial_code_forms = assemble_financial_code_forms(formsets, request.POST)
        else:
            # Form is not valid, so can generate formset without instance
            formsets = ItemFormSet(request.POST)
            formsets.can_delete = False
            financial_code_forms = assemble_financial_code_forms(formsets, request.POST)

    # GET request - generate blank form and formset
    else:
        form = TransactionForm()

        formsets = ItemFormSet()
        formsets.can_delete = False

        financial_code_forms = assemble_financial_code_forms(formsets)
        

    return render(
        request,
        "transactions/add.html",
        {
            "form": form,
            "formsets": formsets,
            "formsets_group": financial_code_forms,
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
