"""Views for the payee_payer app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Demographics
from .forms import PayeePayerForm

# Create your views here.
@login_required
def dashboard(request):
    """Main dashboard to manage payees and payers"""
    return render(
        request,
        "payee_payer/index.html",
        context={},
    )

@login_required
def request_payee_payers(request):
    """List of all payee/payers"""
    return render(
        request,
        "payee_payer/payee_payer_list.html",
        context={
            "payee_payer_list": Demographics.objects.all(),
        }
    )

@login_required
def add_payee_payer(request):
    """Generates and processes form to add a new payee/payer"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        payee_payer_data = Demographics()

        # Create a form instance and populate it with data from the request (binding):
        form = PayeePayerForm(request.POST, instance=payee_payer_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            name = form.cleaned_data["name"]
            address = form.cleaned_data["address"]
            country = form.cleaned_data["country"]
            province = form.cleaned_data["province"]
            city = form.cleaned_data["city"]
            postal_code = form.cleaned_data["postal_code"]
            phone = form.cleaned_data["phone"]
            fax = form.cleaned_data["fax"]
            email = form.cleaned_data["email"]
            status = form.cleaned_data["status"]

            # Update the Demographics model object
            payee_payer_data.name = name
            payee_payer_data.address = address
            payee_payer_data.country = country
            payee_payer_data.province = province
            payee_payer_data.city = city
            payee_payer_data.postal_code = postal_code
            payee_payer_data.phone = phone
            payee_payer_data.fax = fax
            payee_payer_data.email = email
            payee_payer_data.status = status

            payee_payer_data.save()

            # redirect to a new URL:
            messages.success(request, "Payee/payer successfully added")

            return HttpResponseRedirect(reverse("payee_payer_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = PayeePayerForm(initial={})

    return render(
        request,
        "payee_payer/add.html",
        {'form': form},
    )

@login_required
def edit_payee_payer(request, payee_payer_id):
    """Generates and processes form to edit a payee/payer"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        payee_payer_data = get_object_or_404(Demographics, id=payee_payer_id)

        # Create a form instance and populate it with data from the request (binding):
        form = PayeePayerForm(request.POST, instance=payee_payer_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            name = form.cleaned_data["name"]
            address = form.cleaned_data["address"]
            country = form.cleaned_data["country"]
            province = form.cleaned_data["province"]
            city = form.cleaned_data["city"]
            postal_code = form.cleaned_data["postal_code"]
            phone = form.cleaned_data["phone"]
            fax = form.cleaned_data["fax"]
            email = form.cleaned_data["email"]
            status = form.cleaned_data["status"]

            # Update the Demographics model object
            payee_payer_data.name = name
            payee_payer_data.address = address
            payee_payer_data.country = country
            payee_payer_data.province = province
            payee_payer_data.city = city
            payee_payer_data.postal_code = postal_code
            payee_payer_data.phone = phone
            payee_payer_data.fax = fax
            payee_payer_data.email = email
            payee_payer_data.status = status

            payee_payer_data.save()

            # redirect to a new URL:
            messages.success(request, "Payee/payer successfully edited")

            return HttpResponseRedirect(reverse("payee_payer_dashboard"))

    # If this is a GET (or any other method) populate the default form.
    else:
        # Get initial form data
        payee_payer_data = get_object_or_404(Demographics, id=payee_payer_id)

        form = PayeePayerForm(initial={
            "name": payee_payer_data.name,
            "address": payee_payer_data.address,
            "country": payee_payer_data.country,
            "province": payee_payer_data.province,
            "city": payee_payer_data.city,
            "postal_code": payee_payer_data.postal_code,
            "phone": payee_payer_data.phone,
            "fax": payee_payer_data.fax,
            "email": payee_payer_data.email,
            "status": payee_payer_data.status,
        })

    return render(
        request,
        "payee_payer/edit.html",
        {'form': form}
    )

@login_required
def delete_payee_payer(request, payee_payer_id):
    """Generates and processess deletion of payee_payer"""
     # Get the Shift Code instance for this user
    payee_payer = get_object_or_404(Demographics, id=payee_payer_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        payee_payer.delete()

        # Redirect back to main list
        messages.success(request, "Payee/payer deleted")
        return HttpResponseRedirect(reverse('payee_payer_dashboard'))

    return render(
        request,
        "payee_payer/delete.html",
        {"name": payee_payer.name},
    )
