"""View for the bank_transaction app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import InstitutionForm, AccountFormSet
from .models import Institution

@login_required
def dashboard(request):
    """Page to modify bank and account settings"""

    return render(
        request,
        "bank_institutions/index.html",
        context={
            "institutions": Institution.objects.all(),
        },
    )

@login_required
def add(request):
    """Generates & processes form to add new bank institutions and accounts"""

    # POST request - attempt to save data
    if request.method == "POST":
        # Create the institution form
        institution_form = InstitutionForm(request.POST)

        # Check if the form is valid:
        if institution_form.is_valid():
            # Get an institution instance to create the account formset
            institution_instance = institution_form.save(commit=False)

            # Create the account formset
            account_formsets = AccountFormSet(request.POST, instance=institution_instance)

            if account_formsets.is_valid():
                # All forms are valid, save the data
                institution_instance.save()
                account_formsets.save()

                # redirect back to the dashboard
                messages.success(request, "Banking institution and accounts added")
                return HttpResponseRedirect(reverse("bank_institutions:dashboard"))

        # Institution form is invalid, create a unbound account_formsets
        else:
            # Create an account formset to return
            account_formsets = AccountFormSet(request.POST)

    # GET request - create blank forms and formsets
    else:
        institution_form = InstitutionForm()
        account_formsets = AccountFormSet()

    return render(
        request,
        "bank_institutions/add.html",
        {
            "form": institution_form,
            "formsets": account_formsets,
            "page_name": "banking institution & accounts",
            "legend_title": "Accounts",
            "formset_button": "Add account",
        },
    )

@login_required
def edit(request, institution_id):
    """Generate and processes form to edit a financial system"""

    # POST request - attempt to save data
    if request.method == "POST":
        # Get the institution instance
        institution_instance = get_object_or_404(Institution, id=institution_id)

        # Create the institution form
        institution_form = InstitutionForm(request.POST, instance=institution_instance)

        # Check if the form is valid:
        if institution_form.is_valid():
            # Create a item form instance and provide it the institution object
            account_formsets = AccountFormSet(
                request.POST, instance=institution_instance
            )
            account_formsets.can_delete = True

            if account_formsets.is_valid():
                institution_form.save()
                account_formsets.save()

                # redirect to a new URL:
                messages.success(
                    request,
                    "Institution and accounts successfully updated"
                )

                return HttpResponseRedirect(reverse("bank_institutions:dashboard"))

        # Institution form is invalid, create a unbound account_formsets
        else:
            # Create an account formset to return
            account_formsets = AccountFormSet(request.POST, instance=institution_instance)

    # GET request - create blank forms and formsets
    else:
        # Populate the initial institution data
        institution_instance = get_object_or_404(Institution, id=institution_id)
        institution_form = InstitutionForm(instance=institution_instance)

        # Populate the initial accounts data
        account_formsets = AccountFormSet(instance=institution_instance)
        account_formsets.can_delete = True

    return render(
        request,
        "bank_institutions/edit.html",
        {
            "form": institution_form,
            "formsets": account_formsets,
            "page_name": "banking institution & accounts",
            "legend_title": "accounts",
            "formset_button": "Add account",
        },
    )

@login_required
def delete(request, institution_id):
    """Generates and handles delete requests of a transaction"""

    # Get the Transaction instance
    institution_date = get_object_or_404(Institution, id=institution_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        institution_date.delete()

        # Redirect back to main list
        messages.success(request, "Institution and accounts deleted")

        return HttpResponseRedirect(reverse("bank_institutions:dashboard"))

    return render(
        request,
        "bank_institutions/delete.html",
        {
            "page_name": "institution & accounts",
            "delete_message": "institution (and all associated accounts)",
            "item_to_delete": str(institution_date),
        },
    )
