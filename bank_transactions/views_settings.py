"""View for the bank_transaction app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import InstitutionForm
from .models import Institution, Account

@login_required
def settings(request):
    """Page to modify bank and account settings"""
    # pylint: disable=no-member
    institutions = Institution.objects.all()

    return render(
        request,
        "bank_settings/index.html",
        context={
            "institutions": institutions,
        },
    )

@login_required
def institution_add(request):
    """Generates & processes form to add new bank institutions and accounts"""

    def save_institution_form(form, institution_data):
        """Saves Institution instance based on provided form data"""
        # Collect the cleaned form fields
        name = form.cleaned_data["name"]
        address = form.cleaned_data["address"]
        phone = form.cleaned_data["phone"]
        fax = form.cleaned_data["fax"]

        # Set the model data and save the instance
        institution_data.name = name
        institution_data.address = address
        institution_data.phone = phone
        institution_data.fax = fax

        institution_data.save()

    def save_account_formset(formset, institution_data):
        """Saves BankTransaction based on provided formset data"""
        # Only save non-empty forms
        if formset.cleaned_data:
            # Create an BankTransaction object
            account_data = Account()

            # Collect the cleaned formset data
            account_number = formset.cleaned_data["account_number"]
            name = formset.cleaned_data["name"]
            status = formset.cleaned_data["status"]

            # Set the model data and save the instance
            account_data.institution = institution_data
            account_data.account_number = account_number
            account_data.name = name
            account_data.status = status

            account_data.save()

    # Setup the inline formset for the Item model
    account_formset = inlineformset_factory(
        Institution,
        Account,
        fields=("account_number", "name", "status",),
        min_num=1,
        validate_min=True,
        extra=0,
        can_delete=False,
    )

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a Statement object
        institution_data = Institution()

        # Create a form instance and populate it with data from the request (binding):
        form = InstitutionForm(request.POST, instance=institution_data)

        # Check if the form is valid:
        if form.is_valid():
            # Create a item form instance and provide it the institution object
            formsets = account_formset(
                request.POST, instance=institution_data
            )

            if formsets.is_valid():
                save_institution_form(form, institution_data)

                # Cycle through each item_formset and save model data
                for formset in formsets:
                    save_account_formset(formset, institution_data)

                # redirect to a new URL:
                messages.success(request, "Banking institution added")

                return HttpResponseRedirect(reverse("bank_settings"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = InstitutionForm(initial={})
        formsets = account_formset()

    return render(
        request,
        "bank_settings/add.html",
        {
            "form": form,
            "formsets": formsets,
        },
    )

@login_required
def institution_edit(request, institution_id):
    """Generate and processes form to edit a financial system"""

    def update_transaction_form(form):
        """Updates Institution instance based on provided form data"""
        # Collect the cleaned form fields
        name = form.cleaned_data["name"]
        address = form.cleaned_data["address"]
        phone = form.cleaned_data["phone"]
        fax = form.cleaned_data["fax"]

        # Set the model data and save the instance
        institution_data.name = name
        institution_data.address = address
        institution_data.phone = phone
        institution_data.fax = fax

        institution_data.save()

    def update_account_formset(formset, institution_data):
        """Create/updates BankTransaction based on provided formset data"""
        # Only save non-empty forms
        if formset.cleaned_data:
             # Check if this item is marked for deletion
            can_delete = formset.cleaned_data["DELETE"]
            
            if can_delete:
                # Retrieve the account for deletion
                # pylint: disable=no-member
                account_id = formset.cleaned_data["id"].id
                account_data = Account.objects.get(id=account_id)
                
                # Delete the retrieved account
                account_data.delete()
            else:
                # Get this account ID
                if formset.cleaned_data["id"]:
                    # Retrieve item reference
                    # pylint: disable=no-member
                    account_data = get_object_or_404(
                        Account, id=formset.cleaned_data["id"].id
                    )
                else:
                    account_data = Account()

                # Collect the cleaned formset data
                account_number = formset.cleaned_data["account_number"]
                name = formset.cleaned_data["name"]
                status = formset.cleaned_data["status"]

                # Set the model data and save the instance
                account_data.institution = institution_data
                account_data.account_number = account_number
                account_data.name = name
                account_data.status = status

                account_data.save()

    # Setup the inline formset for the Item model
    account_formset = inlineformset_factory(
        Institution,
        Account,
        fields=("account_number", "name", "status",),
        min_num=1,
        validate_min=True,
        can_delete=True,
    )

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Get the transaction object
        institution_data = get_object_or_404(Institution, id=institution_id)

        # Create a form instance and populate it with data from the request (binding):
        form = InstitutionForm(request.POST, instance=institution_data)

        # Check if the form is valid:
        if form.is_valid():
            # Create a item form instance and provide it the institution object
            formsets = account_formset(
                request.POST, instance=institution_data
            )
            
            if formsets.is_valid():
                
                update_transaction_form(form)

                # Cycle through each item_formset and save model data
                for formset in formsets:
                    update_account_formset(formset, institution_data)

                # redirect to a new URL:
                messages.success(
                    request,
                    "Institution and accounts successfully updated"
                )

                return HttpResponseRedirect(reverse("bank_settings"))

    # If this is a GET (or any other method) create populated forms
    else:
        # Populate the initial transaction data
        institution_data = get_object_or_404(Institution, id=institution_id)
        form = InstitutionForm(initial={
            "name": institution_data.name,
            "address": institution_data.address,
            "phone": institution_data.phone,
            "fax": institution_data.fax,
        })

        # Create dictionary of item data
        accounts = institution_data.account_set.all()
        initial_account_data = []

        for account in accounts:
            initial_account_data.append({
                "id": account.id,
                "account_number": account.account_number,
                "name": account.name,
                "status": account.status,
            })

        # Populate the initial formset with the item data
        account_formset.extra = len(accounts) - 1
        formsets = account_formset(initial=initial_account_data)

    return render(
        request,
        "bank_settings/edit.html",
        {
            "form": form,
            "formsets": formsets,
        },
    )

@login_required
def institution_delete(request, institution_id):
    """Generates and handles delete requests of a transaction"""

    # Get the Transaction instance
    institution_date = get_object_or_404(Institution, id=institution_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        institution_date.delete()

        # Redirect back to main list
        messages.success(request, "Institution and accounts deleted")

        return HttpResponseRedirect(reverse("bank_settings"))

    return render(
        request,
        "bank_settings/delete.html",
        {
            "title": institution_date,
        },
    )
