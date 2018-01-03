"""View for the bank_transaction app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import StatementForm
from .models import Statement, BankTransaction

@login_required
def dashboard(request):
    """Main dashboard to display banking functions"""
    # pylint: disable=no-member
    statements = Statement.objects.all()

    return render(
        request,
        "bank_transactions/index.html",
        context={
            "statements": statements,
        },
    )

@login_required
def statement_add(request):
    """Generates and processes form to add new bank statement"""

    def save_statement_form(form, statement_data):
        """Saves Statement instance based on provided form data"""
        # Collect the cleaned form fields
        account = form.cleaned_data["account"]
        date_start = form.cleaned_data["date_start"]
        date_end = form.cleaned_data["date_end"]

        # Set the model data and save the instance
        statement_data.account = account
        statement_data.date_start = date_start
        statement_data.date_end = date_end

        statement_data.save()

    def save_transaction_formset(formset, statement_data):
        """Saves BankTransaction based on provided formset data"""
        # Only save non-empty forms
        if formset.cleaned_data:
            # Create an BankTransaction object
            transaction_data = BankTransaction()

            # Collect the cleaned formset data
            date_transaction = formset.cleaned_data["date_transaction"]
            description_bank = formset.cleaned_data["description_bank"]
            description_user = formset.cleaned_data["description_user"]
            amount_debit = formset.cleaned_data["amount_debit"]
            amount_credit = formset.cleaned_data["amount_credit"]

            # Set the model data and save the instance
            transaction_data.statement = statement_data
            transaction_data.date_transaction = date_transaction
            transaction_data.description_bank = description_bank
            transaction_data.description_user = description_user
            transaction_data.amount_debit = amount_debit
            transaction_data.amount_credit = amount_credit

            transaction_data.save()

    # Setup the inline formset for the Item model
    bank_transaction_formset = inlineformset_factory(
        Statement,
        BankTransaction,
        fields=(
            "date_transaction", "description_bank", "description_user",
            "amount_debit", "amount_credit"
        ),
        labels={
            "date_transaction": "Transaction date",
            "description_bank": "Bank description",
            "description_user": "Custom description",
            "amount_debit": "Debit amount",
            "amount_credit": "Credit amount",
        },
        extra=1,
        can_delete=False,
    )

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a Statement object
        statement_data = Statement()

        # Create a form instance and populate it with data from the request (binding):
        form = StatementForm(request.POST, instance=statement_data)

        # Check if the form is valid:
        if form.is_valid():
            # Create a item form instance and provide it the transaction object
            formsets = bank_transaction_formset(
                request.POST, instance=statement_data
            )

            if formsets.is_valid():
                save_statement_form(form, statement_data)

                # Cycle through each item_formset and save model data
                for formset in formsets:
                    save_transaction_formset(formset, statement_data)

                # redirect to a new URL:
                messages.success(request, "Statement successfully added")

                return HttpResponseRedirect(reverse("bank_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = StatementForm(initial={})
        formsets = bank_transaction_formset()

    return render(
        request,
        "bank_transactions/add.html",
        {
            "form": form,
            "formsets": formsets,
            "page_name": "bank statement",
            "legend_title": "Transactions",
            "formset_button": "Add transaction",
        },
    )

@login_required
def statement_edit(request, statement_id):
    """Generate and processes form to edit a financial system"""

    def update_statement_form(form, statement_data):
        """Updates statement based on the provided form data"""

        # Collect the cleaned form fields
        account = form.cleaned_data["account"]
        date_start = form.cleaned_data["date_start"]
        date_end = form.cleaned_data["date_end"]

        # Set the model data and save the instance
        statement_data.account = account
        statement_data.date_start = date_start
        statement_data.date_end = date_end

        statement_data.save()

    def update_bank_transaction_formset(formset, statement_data):
        """Create/updates BankTransaction based on provided formset data"""
        # Only save non-empty forms
        if formset.cleaned_data:
            # Check if this item is marked for deletion
            can_delete = formset.cleaned_data["DELETE"]

            # Get this account ID
            if formset.cleaned_data["id"]:
                bank_transaction_exists = True

                # Retrieve item reference
                # pylint: disable=no-member
                bank_transaction_data = BankTransaction.objects.get(
                    id=formset.cleaned_data["id"].id
                )
            else:
                bank_transaction_exists = False
                bank_transaction_data = BankTransaction()

            if can_delete and bank_transaction_exists:
                # Delete the retrieved account
                bank_transaction_data.delete()
            else:
                # Collect the cleaned formset data
                date_transaction = formset.cleaned_data["date_transaction"]
                description_bank = formset.cleaned_data["description_bank"]
                description_user = formset.cleaned_data["description_user"]
                amount_debit = formset.cleaned_data["amount_debit"]
                amount_credit = formset.cleaned_data["amount_credit"]

                # Set the model data and save the instance
                bank_transaction_data.statement = statement_data
                bank_transaction_data.date_transaction = date_transaction
                bank_transaction_data.description_bank = description_bank
                bank_transaction_data.description_user = description_user
                bank_transaction_data.amount_debit = amount_debit
                bank_transaction_data.amount_credit = amount_credit

                bank_transaction_data.save()

    # Setup the inline formset for the Item model
    bank_transaction_inline_formset = inlineformset_factory(
        Statement,
        BankTransaction,
        fields=(
            "date_transaction", "description_bank", "description_user",
            "amount_debit", "amount_credit"
        ),
        labels={
            "date_transaction": "Transaction date",
            "description_bank": "Bank description",
            "description_user": "Custom description",
            "amount_debit": "Debit amount",
            "amount_credit": "Credit amount",
        },
        can_delete=True,
    )

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a Statement object
        statement_data = get_object_or_404(Statement, id=statement_id)

        # Create a form instance and populate it with data from the request (binding):
        form = StatementForm(request.POST, instance=statement_data)

        # Check if the form is valid:
        if form.is_valid():
            # Create a item form instance and provide it the transaction object
            formsets = bank_transaction_inline_formset(
                request.POST, instance=statement_data
            )

            if formsets.is_valid():
                update_statement_form(form, statement_data)

                # Cycle through each item_formset and save model data
                for formset in formsets:
                    update_bank_transaction_formset(formset, statement_data)

                # redirect to a new URL:
                messages.success(request, "Statement successfully updated")

                return HttpResponseRedirect(reverse("bank_dashboard"))

    # If this is a GET (or any other method) create populated forms
    else:
        # Populate the initial transaction data
        statement_data = get_object_or_404(Statement, id=statement_id)
        form = StatementForm(initial={
            "account": statement_data.account,
            "date_start": statement_data.date_start,
            "date_end": statement_data.date_end,
        })

        # Create dictionary of item data
        bank_transaction_data = statement_data.banktransaction_set.all()
        initial_bank_transaction_data = []

        for bank_transaction in bank_transaction_data:
            initial_bank_transaction_data.append({
                "id": bank_transaction.id,
                "statement": bank_transaction.statement.id,
                "date_transaction": bank_transaction.date_transaction,
                "description_bank": bank_transaction.description_bank,
                "description_user": bank_transaction.description_user,
                "amount_debit": bank_transaction.amount_debit,
                "amount_credit": bank_transaction.amount_credit,
            })

        # Populate the initial formset with the item data
        bank_transaction_inline_formset.extra = len(initial_bank_transaction_data)
        formsets = bank_transaction_inline_formset(
            initial=initial_bank_transaction_data
        )

    return render(
        request,
        "bank_transactions/edit.html",
        {
            "form": form,
            "formsets": formsets,
            "page_name": "bank statement",
            "legend_title": "Transaction items",
            "formset_button": "Add item",
        },
    )

@login_required
def statement_delete(request, statement_id):
    """Generates and handles delete requests of a transaction"""

    # Get the Transaction instance
    statement_data = get_object_or_404(Statement, id=statement_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        statement_data.delete()

        # Redirect back to main list
        messages.success(request, "Statement deleted")

        return HttpResponseRedirect(reverse("bank_dashboard"))

    return render(
        request,
        "bank_transactions/delete.html",
        {
            "page_name": "bank statement",
            "delete_message": "bank statement",
            "item_to_delete": str(statement_data),
        },
    )
