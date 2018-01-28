"""View for the bank_transaction app"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from bank_transactions.models import Statement, BankTransaction, AttachmentMatch
from bank_transactions.forms import StatementForm, BankTransactionFormset, AttachmentMatchFormset, NewAttachmentForm
from documents.models import Attachment
from transactions.models import Transaction
from transactions.services import BankReconciliation


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
    # pylint: disable=no-member
    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create statement form
        statement_form = StatementForm(request.POST)

        # Create brank transaction formsets
        bank_transaction_formsets = BankTransactionFormset(request.POST)
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
                AttachmentMatch.objects.create(
                    statement=saved_statement,
                    attachment=saved_attachment,
                )

            messages.success(request, "Statement successfully added")

            return HttpResponseRedirect(reverse("bank_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        statement_form = StatementForm()
        bank_transaction_formsets = BankTransactionFormset()
        bank_transaction_formsets.can_delete = False
        new_attachment_form = NewAttachmentForm()

    return render(
        request,
        "bank_transactions/add.html",
        {
            "statement_form": statement_form,
            "bank_transaction_formsets": bank_transaction_formsets,
            "new_attachment_form": new_attachment_form,
        },
    )

@login_required
def statement_edit(request, statement_id):
    """Generate and processes form to edit a financial system"""
    # pylint: disable=no-member
    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Get this statement instance
        statement_instance = get_object_or_404(Statement, id=statement_id)

        # Create statement form
        statement_form = StatementForm(request.POST, instance=statement_instance)

        # Create bank transaction formsets
        bank_transaction_formsets = BankTransactionFormset(
            request.POST,
            instance=statement_instance,
        )

        # Create attachment formsets
        attachment_match_formsets = AttachmentMatchFormset(
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
                    attachment_match_formset.cleaned_data["id"].delete()

            # Cycle through each new attachment
            for file in new_attachment_form.cleaned_data["files"]:
                # Create a new attachment instance
                saved_attachment = Attachment.objects.create(
                    location=file,
                )

                # Create the attachment match
                AttachmentMatch.objects.create(
                    statement=saved_statement,
                    attachment=saved_attachment,
                )

            messages.success(request, "Statement successfully updated")

            return HttpResponseRedirect(reverse("bank_dashboard"))
    # If this is a GET (or any other method) create populated forms
    else:
        statement_instance = get_object_or_404(Statement, id=statement_id)

        statement_form = StatementForm(instance=statement_instance)
        bank_transaction_formsets = BankTransactionFormset(instance=statement_instance)
        attachment_match_formsets = AttachmentMatchFormset(instance=statement_instance)
        new_attachment_form = NewAttachmentForm()

    return render(
        request,
        "bank_transactions/edit.html",
        {
            "statement_form": statement_form,
            "bank_transaction_formsets": bank_transaction_formsets,
            "attachment_match_formsets": attachment_match_formsets,
            "new_attachment_form": new_attachment_form,
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

@login_required
def reconciliation_dashboard(request):
    """Page to handle bank reconciliation"""
    # pylint: disable=no-member

    return render(
        request,
        "reconciliation/index.html",
        context={},
    )

@login_required
def retrieve_transactions(request):
    """Retrieves and returns all transactions in provided date range"""
    # pylint: disable=no-member
    transaction_type = request.GET.get("transaction_type", None)
    date_start = request.GET.get("date_start", None)
    date_end = request.GET.get("date_end", None)

    if date_start and date_end and transaction_type == "financial":
        transactions = Transaction.objects.filter(
            Q(date_submitted__gte=date_start) & Q(date_submitted__lte=date_end)
        )

        transaction_list = []
        
        for transaction in transactions:
            transaction_list.append({
                "transaction": str(transaction),
                "id": transaction.id,
                "total": transaction.total,
                "reconciled": transaction.rm_financial_transaction.all().exists()
            })

        json_data = {
            "data": transaction_list,
            "type": "financial"
        }

    elif date_start and date_end and transaction_type == "bank":
        transactions = BankTransaction.objects.filter(
            Q(date_transaction__gte=date_start) & Q(date_transaction__lte=date_end)
        )

        transaction_list = []
        
        for transaction in transactions:
            transaction_list.append({
                "transaction": str(transaction),
                "id": transaction.id,
                "debit": transaction.amount_debit,
                "credit": transaction.amount_credit,
                "reconciled": transaction.rm_bank_transaction.all().exists()
            })

        json_data = {
            "data": transaction_list,
            "type": "bank"
        }
    else:
        json_data = {}
    
    return JsonResponse(json_data)

@login_required
def match_transactions(request):
    """Matches financial and banking transactions (if valid)"""
    reconciliation = BankReconciliation(request.body, "match")

    # Check if provided data is valid
    if reconciliation.is_valid():
        # Make reconcilation matches
        reconciliation.create_matches()

    return JsonResponse({
        "success": reconciliation.success,
        "errors": reconciliation.errors,
    })

@login_required
def unmatch_transactions(request):
    """Unmatches financial and banking transactions (if valid)"""
    reconciliation = BankReconciliation(request.body, "unmatch")

    # Check if provided data is valid
    if reconciliation.is_valid():
        # Make reconcilation matches
        reconciliation.delete_matches()

    return JsonResponse({
        "success": reconciliation.success,
        "errors": reconciliation.errors,
    })
