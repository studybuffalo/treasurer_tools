"""Views for the investment app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import InvestmentForm, InvestmentDetailForm
from .models import Investment, InvestmentDetail

@login_required
def dashboard(request):
    """Main dashboard to view investments"""
    investments = Investment.objects.all()

    return render(
        request,
        "investments/index.html",
        context={
            "investments": investments,
        },
    )

@login_required
def investment_add(request):
    """Generates and processes form to add an investment"""

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a Transaction object
        investment_data = Investment()

        # Create a form instance and populate it with data from the request (binding):
        form = InvestmentForm(request.POST, instance=investment_data)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Investment successfully added")

            return HttpResponseRedirect(reverse("investments:dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = InvestmentForm(initial={})

    return render(
        request,
        "investments/add_edit.html",
        {
            "page_name": "Add New Investment",
            "form": form,
            "submit_button": "Add new investment",
        },
    )

@login_required
def investment_edit(request, investment_id):
    """Generate and processes form to edit a financial system"""

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Get the Investment object
        investment_data = get_object_or_404(Investment, id=investment_id)

        # Create a form instance and populate it with data from the request (binding):
        form = InvestmentForm(request.POST, instance=investment_data)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Investment updated")

            return HttpResponseRedirect(reverse("investments:dashboard"))

    # If this is a GET (or any other method) create populated forms
    else:
        # Populate the initial transaction data
        investment_data = get_object_or_404(Investment, id=investment_id)
        form = InvestmentForm(instance=investment_data)

    return render(
        request,
        "investments/add_edit.html",
        {
            "page_name": "Edit Investment",
            "form": form,
            "submit_button": "Save investment changes",
        },
    )

@login_required
def investment_delete(request, investment_id):
    """Generates and handles delete requests of an investment"""

    # Get the Investment instance
    investment_data = get_object_or_404(Investment, id=investment_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        investment_data.delete()

        # Redirect back to main list
        messages.success(request, "Investment deleted")

        return HttpResponseRedirect(reverse("investments:dashboard"))

    return render(
        request,
        "investments/delete.html",
        {
            "page_name": "investment",
            "delete_message": "investment",
            "item_to_delete": str(investment_data),
        },
    )

@login_required
def detail_add(request, investment_id):
    """Generates and processes form to add an investment"""

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        form = InvestmentDetailForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Investment details successfully added")

            return HttpResponseRedirect(reverse("investments:dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = InvestmentDetailForm(initial={"investment": investment_id})

    return render(
        request,
        "investments/add_edit.html",
        {
            "page_name": "Add New Investment Details",
            "form": form,
            "submit_button": "Add new details",
        },
    )

@login_required
def detail_edit(request, detail_id):
    """Generate and processes form to edit a financial system"""

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Get the Investment object
        detail_data = get_object_or_404(InvestmentDetail, id=detail_id)

        # Create a form instance and populate it with data from the request (binding):
        form = InvestmentDetailForm(request.POST, instance=detail_data)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Investment details updated")

            return HttpResponseRedirect(reverse("investments:dashboard"))

    # If this is a GET (or any other method) create populated forms
    else:
        # Populate the initial transaction data
        detail_data = get_object_or_404(InvestmentDetail, id=detail_id)
        form = InvestmentDetailForm(instance=detail_data)

    return render(
        request,
        "investments/add_edit.html",
        {
            "page_name": "Edit Investment Details",
            "form": form,
            "submit_button": "Save changes",
        },
    )

@login_required
def detail_delete(request, detail_id):
    """Generates and handles delete requests of an investment"""

    # Get the Investment instance
    detail_data = get_object_or_404(InvestmentDetail, id=detail_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        detail_data.delete()

        # Redirect back to main list
        messages.success(request, "Investment detail deleted")

        return HttpResponseRedirect(reverse("investments:dashboard"))

    return render(
        request,
        "investments/delete.html",
        {
            "page_name": "investment detail",
            "delete_message": "investment detail",
            "item_to_delete": str(detail_data),
        },
    )
