"""Views for the investment app"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import InvestmentForm
from .models import Investment

@login_required
def dashboard(request):
    """Main dashboard to view investments"""
    # pylint: disable=no-member
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

    def save_investment_form(form, investment_data):
        """Saves Investment instance based on provided form data"""
        # Collect the cleaned form fields
        name = form.cleaned_data["name"]
        date_invested = form.cleaned_data["date_invested"]
        amount = form.cleaned_data["amount"]
        rate = form.cleaned_data["rate"]

        # Set the model data and save the instance
        investment_data.name = name
        investment_data.date_invested = date_invested
        investment_data.amount = amount
        investment_data.rate = rate

        investment_data.save()

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a Transaction object
        investment_data = Investment()

        # Create a form instance and populate it with data from the request (binding):
        form = InvestmentForm(request.POST, instance=investment_data)

        # Check if the form is valid:
        if form.is_valid():
            save_investment_form(form, investment_data)

            # redirect to a new URL:
            messages.success(request, "Investment successfully added")

            return HttpResponseRedirect(reverse("investments_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = InvestmentForm(initial={})

    return render(
        request,
        "investments/add.html",
        {
            "page_name": "investment",
            "form": form,
        },
    )

@login_required
def investment_edit(request, investment_id):
    """Generate and processes form to edit a financial system"""

    def update_investment_form(form, investment_data):
        """Updates/saves investment instance based on provided form data"""

        name = form.cleaned_data["name"]
        date_invested = form.cleaned_data["date_invested"]
        amount = form.cleaned_data["amount"]
        rate = form.cleaned_data["rate"]

        # Set the model data and save the instance
        investment_data.name = name
        investment_data.date_invested = date_invested
        investment_data.amount = amount
        investment_data.rate = rate

        investment_data.save()

    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Get the Investment object
        investment_data = get_object_or_404(Investment, id=investment_id)

        # Create a form instance and populate it with data from the request (binding):
        form = InvestmentForm(request.POST, instance=investment_data)

        # Check if the form is valid:
        if form.is_valid():
            update_investment_form(form, investment_data)

            # redirect to a new URL:
            messages.success(request, "Investment updated")

            return HttpResponseRedirect(reverse("investments_dashboard"))

    # If this is a GET (or any other method) create populated forms
    else:
        # Populate the initial transaction data
        investment_data = get_object_or_404(Investment, id=investment_id)
        form = InvestmentForm(initial={
            "name": investment_data.name,
            "date_invested": investment_data.date_invested,
            "amount": investment_data.amount,
            "rate": investment_data.rate,
        })

    return render(
        request,
        "investments/edit.html",
        {
            "page_name": "investment",
            "form": form,
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

        return HttpResponseRedirect(reverse("investments_dashboard"))

    return render(
        request,
        "investments/delete.html",
        {
            "page_name": "investment",
            "delete_message": "investment",
            "item_to_delete": str(investment_data),
        },
    )
