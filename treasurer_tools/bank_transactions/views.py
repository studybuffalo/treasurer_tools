"""View for the bank_transaction app"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from documents.models import Attachment, BankStatementMatch
from bank_institutions.models import Account
from .models import Statement
from .forms import StatementForm, BankTransactionFormSet, AttachmentMatchFormSet, NewAttachmentForm


@login_required
def dashboard(request):
    """Main dashboard to display banking functions"""
    accounts = Account.objects.all()

    return render(
        request,
        "bank_transactions/index.html",
        context={
            "accounts": accounts,
        },
    )

@login_required
def statement_add(request):
    """Generates and processes form to add new bank statement"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create statement form
        statement_form = StatementForm(request.POST)

        # Create brank transaction formsets
        bank_transaction_formsets = BankTransactionFormSet(request.POST)
        bank_transaction_formsets.can_delete = False

        # Create new attachment form
        new_attachment_form = NewAttachmentForm(request.POST, request.FILES)

        # Check if forms are valid
        if statement_form.is_valid() and bank_transaction_formsets.is_valid() and new_attachment_form.is_valid():
            # Save new statement instance
            saved_statement = statement_form.save()

            # Cycle through each transaction formset
            for transaction_formset in bank_transaction_formsets:
                # Ignore empty forms
                if transaction_formset.cleaned_data:
                    # Create the transaction instance
                    saved_transaction = transaction_formset.save(commit=False)

                    # Update transaction instance with statement reference
                    saved_transaction.statement = saved_statement

                    # Save the transaction with new reference
                    saved_transaction.save()

            # Cycle through each new attachment
            for file in new_attachment_form.cleaned_data["files"]:
                # Create a new attachment instance
                saved_attachment = Attachment.objects.create(
                    location=file,
                )

                # Create the attachment match
                BankStatementMatch.objects.create(
                    statement=saved_statement,
                    attachment=saved_attachment,
                )

            messages.success(request, "Statement successfully added")

            return HttpResponseRedirect(reverse("bank_transactions:dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        statement_form = StatementForm()
        bank_transaction_formsets = BankTransactionFormSet()
        bank_transaction_formsets.can_delete = False
        new_attachment_form = NewAttachmentForm()

    return render(
        request,
        "bank_transactions/add_edit.html",
        {
            "statement_form": statement_form,
            "bank_transaction_formsets": bank_transaction_formsets,
            "new_attachment_form": new_attachment_form,
            "page_name": "Add New Bank Statement",
            "submit_button": "Add new bank statement",
            "type": "add",
        },
    )

@login_required
def statement_edit(request, statement_id):
    """Generate and processes form to edit a financial system"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Get this statement instance
        statement_instance = get_object_or_404(Statement, id=statement_id)

        # Create statement form
        statement_form = StatementForm(request.POST, instance=statement_instance)

        # Create bank transaction formsets
        bank_transaction_formsets = BankTransactionFormSet(
            request.POST,
            instance=statement_instance,
        )

        # Create attachment formsets
        attachment_match_formsets = AttachmentMatchFormSet(
            request.POST,
            instance=statement_instance,
        )

        # Create new attachment form
        new_attachment_form = NewAttachmentForm(request.POST, request.FILES)

        # Check if forms are valid
        if (
                statement_form.is_valid() and bank_transaction_formsets.is_valid()
                and attachment_match_formsets.is_valid() and new_attachment_form.is_valid()
        ):
            # Save new statement instance
            saved_statement = statement_form.save()

            # Cycle through each transaction formset
            for transaction_formset in bank_transaction_formsets:
                # Ignore emtpy forms
                if transaction_formset.cleaned_data:
                    # Delete any formset marked for deletion
                    if transaction_formset.cleaned_data["DELETE"]:
                        transaction_formset.cleaned_data["id"].delete()
                    else:
                        # Create the transaction instance
                        saved_transaction = transaction_formset.save(commit=False)

                        # Update transaction instance with statement reference
                        saved_transaction.statement = saved_statement

                        # Save the transaction with new reference
                        saved_transaction.save()

            # Delete any old attachments
            for attachment_match_formset in attachment_match_formsets:
                if attachment_match_formset.cleaned_data["DELETE"]:
                    # Get the match object
                    attachment_match = attachment_match_formset.cleaned_data["id"]

                    # Delete the attachment
                    attachment_match.attachment.delete()

                    # Delete the attachment match
                    attachment_match.delete()

            # Cycle through each new attachment
            for file in new_attachment_form.cleaned_data["files"]:
                # Create a new attachment instance
                saved_attachment = Attachment.objects.create(
                    location=file,
                )

                # Create the attachment match
                BankStatementMatch.objects.create(
                    statement=saved_statement,
                    attachment=saved_attachment,
                )

            messages.success(request, "Statement successfully updated")

            return HttpResponseRedirect(reverse("bank_transactions:dashboard"))
    # If this is a GET (or any other method) create populated forms
    else:
        statement_instance = get_object_or_404(Statement, id=statement_id)

        statement_form = StatementForm(instance=statement_instance)
        bank_transaction_formsets = BankTransactionFormSet(instance=statement_instance)
        attachment_match_formsets = AttachmentMatchFormSet(instance=statement_instance)
        new_attachment_form = NewAttachmentForm()

    return render(
        request,
        "bank_transactions/add_edit.html",
        {
            "statement_form": statement_form,
            "bank_transaction_formsets": bank_transaction_formsets,
            "attachment_match_formsets": attachment_match_formsets,
            "new_attachment_form": new_attachment_form,
            "page_name": "Edit Bank Statement",
            "submit_button": "Save changes",
            "type": "edit",
        },
    )

@login_required
def statement_delete(request, statement_id):
    """Generates and handles delete requests of a transaction"""

    # Get the Transaction instance
    statement_data = get_object_or_404(Statement, id=statement_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Delete any attachment matches
        if statement_data.bankstatementmatch_set.all():
            statement_data.bankstatementmatch_set.all().delete()

        # Delete the statement
        statement_data.delete()

        # Redirect back to main list
        messages.success(request, "Statement deleted")

        return HttpResponseRedirect(reverse("bank_transactions:dashboard"))

    return render(
        request,
        "bank_transactions/delete.html",
        {
            "page_name": "bank statement",
            "delete_message": "bank statement",
            "item_to_delete": str(statement_data),
        },
    )
