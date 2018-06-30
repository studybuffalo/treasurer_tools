"""Views for the payee_payer app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import PayeePayer
from .forms import PayeePayerForm

# Create your views here.
@login_required
def dashboard(request):
    """Main dashboard to manage payees and payers"""
    return render(
        request,
        "payee_payers/index.html",
        context={},
    )

@login_required
def request_payee_payers(request):
    """List of all payee/payers"""
    # pylint: disable=no-member
    return render(
        request,
        "payee_payers/payee_payer_list.html",
        context={
            "payee_payer_list": PayeePayer.objects.all(),
        }
    )

@login_required
def add_payee_payer(request):
    """Generates and processes form to add a new payee/payer"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        payee_payer_data = PayeePayer()

        # Create a form instance and populate it with data from the request (binding):
        form = PayeePayerForm(request.POST, instance=payee_payer_data)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Payee/payer successfully added")

            return HttpResponseRedirect(reverse("payee_payers:dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = PayeePayerForm(initial={})

    return render(
        request,
        "payee_payers/add.html",
        {
            "form": form,
            "page_name": "payee/payer",
        },
    )

@login_required
def edit_payee_payer(request, payee_payer_id):
    """Generates and processes form to edit a payee/payer"""
    # TODO: Fix javascript functions - defaults to Canada/Alberta on edit
    # If this is a POST request then process the Form data
    if request.method == "POST":
        payee_payer_data = get_object_or_404(PayeePayer, id=payee_payer_id)

        # Create a form instance and populate it with data from the request (binding):
        form = PayeePayerForm(request.POST, instance=payee_payer_data)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Payee/payer successfully edited")

            return HttpResponseRedirect(reverse("payee_payers:dashboard"))

    # If this is a GET (or any other method) populate the default form.
    else:
        # Get initial form data
        payee_payer_data = get_object_or_404(PayeePayer, id=payee_payer_id)

        form = PayeePayerForm(instance=payee_payer_data)

    return render(
        request,
        "payee_payers/edit.html",
        {
            "form": form,
            "page_name": "payee/payer",
        }
    )

@login_required
def delete_payee_payer(request, payee_payer_id):
    """Generates and processess deletion of payee_payer"""
     # Get the Shift Code instance for this user
    payee_payer = get_object_or_404(PayeePayer, id=payee_payer_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        payee_payer.delete()

        # Redirect back to main list
        messages.success(request, "Payee/payer deleted")
        return HttpResponseRedirect(reverse('payee_payers:dashboard'))

    return render(
        request,
        "payee_payers/delete.html",
        {
            "page_name": "payee/payer",
            "delete_message": "payee/payee",
            "delete_restriction": (
                "Note: A payee/payer can only be deleted once all associated "
                "expenses and revenue claims are either deleted or assigned "
                "to a new payee/payer."
            ),
            "item_to_delete": payee_payer.name,
        },
    )
