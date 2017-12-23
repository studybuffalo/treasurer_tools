from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
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

class RequestPayeePayers(LoginRequiredMixin, generic.ListView):
    model = Demographics

    context_object_name = "payee_payer_list"
    template_name = "payee_payer/payee_payer_list.html"
    
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
        {'form': form}
    )

@login_required
def edit_payee_payer(request):
    """Generates and processes form to edit a payee/payer"""
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
            messages.success(request, "Payee/payer successfully edited")

            return HttpResponseRedirect(reverse("payee_payer_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = PayeePayerForm(initial={})

    return render(
        request, 
        "payee_payer/edit.html", 
        {'form': form}
    )

@login_required
def delete_payee_payer(request):
    """Page to confirm deletion of payee/payer"""
    return render(
        request,
        "payee_payer/delete.html",
        context={},
    )