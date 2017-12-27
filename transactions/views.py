"""Views for the transactions app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import TransactionForm
from .models import Transaction, Item

@login_required
def dashboard(request):
    """Main dashboard to expenses and revenue"""
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
    
    # Setup the inline formset for the Item model
    ItemInlineFormSet = inlineformset_factory(
        Transaction,
        Item,
        fields=("date_item", "description", "amount", "gst",),
        extra=5,
        min_num=1,
        validate_min=True,
        can_delete=False,
    )

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a Transaction object
        transaction_data = Transaction()

        # Create a form instance and populate it with data from the request (binding):
        form = TransactionForm(request.POST, instance=transaction_data)

        # Check if the form is valid:
        if form.is_valid():
            # Create a item form instance and provide it the transaction object
            item_formset = ItemInlineFormSet(request.POST, instance=transaction_data)

            if item_formset.is_valid():
                # Collect the cleaned form fields
                payee_payer = form.cleaned_data["payee_payer"]
                memo = form.cleaned_data["memo"]
                date_submitted = form.cleaned_data["date_submitted"]
                transaction_type = "e" if t_type == "expense" else "r"

                # Set the model data and save the instance
                transaction_data.payee_payer = payee_payer
                transaction_data.memo = memo
                transaction_data.date_submitted = date_submitted
                transaction_data.transaction_type = transaction_type

                transaction_data.save()
                
                # Cycle through each item_formset and save model data
                for formset in item_formset:
                    # Only save non-empty forms
                    if formset.cleaned_data:
                        # Create an Item object
                        item_data = Item()

                        # Collect the cleaned formset data
                        date_item = formset.cleaned_data["date_item"]
                        description = formset.cleaned_data["description"]
                        amount = formset.cleaned_data["amount"]
                        gst = formset.cleaned_data["gst"]

                        # Set the model data and save the instance
                        item_data.transaction = transaction_data
                        item_data.date_item = date_item
                        item_data.description = description
                        item_data.amount = amount
                        item_data.gst = gst

                        item_data.save()

                # redirect to a new URL:
                messages.success(request, "Expense successfully added")

                return HttpResponseRedirect(reverse("transactions_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = TransactionForm(initial={})
        item_formset = ItemInlineFormSet()
    
    return render(
        request,
        "transactions/add.html",
        {
            "page_name": t_type,
            "form": form,
            "formset": item_formset,
        },
    )

@login_required
def transaction_edit(request, t_type, transaction_id):
    """Generate and processes form to edit a financial system"""
    
    # Setup the inline formset for the Item model
    ItemInlineFormSet = inlineformset_factory(
        Transaction,
        Item,
        form=TransactionForm,
        fields=("date_item", "description", "amount", "gst"),
        min_num=1,
        validate_min=True,
        can_delete=True,
    )

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Get the transaction object
        transaction_data = get_object_or_404(Transaction, id=transaction_id)

        # Create a form instance and populate it with data from the request (binding):
        form = TransactionForm(request.POST, instance=transaction_data)

        # Check if the form is valid:
        if form.is_valid():
            # Create a item form instance and provide it the transaction object
            item_formset = ItemInlineFormSet(request.POST, instance=transaction_data)

            if item_formset.is_valid():
                # Collect the cleaned form fields
                payee_payer = form.cleaned_data["payee_payer"]
                memo = form.cleaned_data["memo"]
                date_submitted = form.cleaned_data["date_submitted"]
                transaction_type = "e" if t_type == "expense" else "r"

                # Set the model data and save the instance
                transaction_data.payee_payer = payee_payer
                transaction_data.memo = memo
                transaction_data.date_submitted = date_submitted
                transaction_data.transaction_type = transaction_type

                transaction_data.save()
                
                # Cycle through each item_formset and save model data
                for formset in item_formset:
                    # Only save non-empty forms
                    if formset.cleaned_data:
                        # Check if this item is marked for deletion
                        can_delete = formset.cleaned_data["DELETE"]

                        # Get this item ID
                        if formset.cleaned_data["id"]:
                            item_exists = True

                            # Retrieve item reference
                            item_data = Item.objects.get(
                                id=formset.cleaned_data["id"].id
                            )
                        else:
                            item_exists = False
                            item_data = Item()

                        if can_delete and item_exists:
                            # Delete the retrieved item
                            item_data.delete()
                        else:
                            # Collect the cleaned formset data
                            date_item = formset.cleaned_data["date_item"]
                            description = formset.cleaned_data["description"]
                            amount = formset.cleaned_data["amount"]
                            gst = formset.cleaned_data["gst"]

                            # Set the model data and save the instance
                            item_data.transaction = transaction_data
                            item_data.date_item = date_item
                            item_data.description = description
                            item_data.amount = amount
                            item_data.gst = gst

                            item_data.save()
                            
                # redirect to a new URL:
                messages.success(request, "Expense successfully edited")

                return HttpResponseRedirect(reverse("transactions_dashboard"))

    # If this is a GET (or any other method) create populated forms
    else:
        # Populate the initial transaction data
        transaction_data = get_object_or_404(Transaction, id=transaction_id)
        form = TransactionForm(initial={
            "payee_payer": transaction_data.payee_payer,
            "memo": transaction_data.memo,
            "date_submitted": transaction_data.date_submitted
        })

        # Create dictionary of item data
        items = transaction_data.item_set.all()
        initial_item_data = []

        for item in items:
            initial_item_data.append({
                "id": item.id,
                "date_item": item.date_item,
                "description": item.description,
                "amount": item.amount,
                "gst": item.gst
            })
        print(len(items))
        # Populate the initial formset with the item data
        ItemInlineFormSet.extra = len(items) - 1
        item_formset = ItemInlineFormSet(initial=initial_item_data)

    return render(
        request,
        "transactions/edit.html",
        {
            "page_name": t_type,
            "form": form,
            "formset": item_formset,
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
            "title": transaction
        },
    )
