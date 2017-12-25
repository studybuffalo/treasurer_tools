"""View for the financial_codes app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import (
    BudgetYear, FinancialCodeSystem, FinancialCodeGroup, FinancialCode,
)

from .forms import (
    FinancialCodeSystemForm,
)

@login_required
def dashboard(request):
    """Main dashboard to manage financial codes"""
    systems = FinancialCodeSystem.objects.all()  # pylint: disable=no-member

    return render(
        request,
        "financial_codes/index.html",
        context={
            "systems": systems,
        },
    )

@login_required
def add_new_year(request):
    """Generates and processes form to add budget year"""

@login_required
def system_add(request):
    """Generates and processes form to add financial code system"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        system_data = FinancialCodeSystem()

        # Create a form instance and populate it with data from the request (binding):
        form = FinancialCodeSystemForm(request.POST, instance=system_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            title = form.cleaned_data["title"]
            status = form.cleaned_data["status"]

            # Update the FinancialSystem model object
            system_data.title = title
            system_data.status = status

            system_data.save()

            # redirect to a new URL:
            messages.success(request, "Financial code system successfully added")

            return HttpResponseRedirect(reverse("financial_codes_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = FinancialCodeSystemForm(initial={})

    return render(
        request,
        "financial_codes/system_add.html",
        {'form': form}
    )

@login_required
def system_edit(request, system_id):
    """Generate and processes form to edit a financial system"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        system_data = get_object_or_404(FinancialCodeSystem, id=system_id)

        # Create a form instance and populate it with data from the request (binding):
        form = FinancialCodeSystemForm(request.POST, instance=system_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            title = form.cleaned_data["title"]
            status = form.cleaned_data["status"]

            # Update the Financial Systems object
            system_data.title = title
            system_data.status = status

            system_data.save()

            # redirect to a new URL:
            messages.success(request, "Financial code system successfully edited")

            return HttpResponseRedirect(reverse("financial_codes_dashboard"))

    # If this is a GET (or any other method) populate the default form.
    else:
        # Get initial form data
        system_data = get_object_or_404(FinancialCodeSystem, id=system_id)

        form = FinancialCodeSystemForm(initial={
            "title": system_data.title,
            "status": system_data.status,
        })

    return render(
        request,
        "financial_codes/system_edit.html",
        {'form': form}
    )

@login_required
def system_delete(request, system_id):
    """Generates and handles delete requests of financial system"""
    # Get the Shift Code instance for this user
    system = get_object_or_404(FinancialCodeSystem, id=system_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        system.delete()

        # Redirect back to main list
        messages.success(request, "Financial code system deleted")

        return HttpResponseRedirect(reverse('financial_codes_dashboard'))
    return render(
        request,
        "financial_codes/system_delete.html",
        {"title": system.title},
    )

@login_required
def add_code(request):
    """Generates and processes form to add a new financial code"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        code_data = FinancialCode()

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
def edit_code(request, code_id):
    """Generates and processes form to edit a payee/payer"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        payee_payer_data = get_object_or_404(Demographics, id=code_id)

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
        payee_payer_data = get_object_or_404(Demographics, id=code_id)

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
def code_delete(request, code_id):
    """Generates and processes deletion of financial code"""
     # Get the Shift Code instance for this user
    payee_payer = get_object_or_404(Demographics, id=code_id)

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
