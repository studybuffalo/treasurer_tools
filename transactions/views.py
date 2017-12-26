"""Views for the transactions app"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Transaction, Item

@login_required
def dashboard(request):
    """Main dashboard to expenses and revenue"""
    return render(
        request,
        "transactions/index.html",
        context={},
    )

@login_required
def transaction_add(request, transaction_type):
    """Generates and processes form to add expense"""
    """
    # If this is a POST request then process the Form data
    if request.method == "POST":
        expense_data = FinancialCodeSystem()

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
    """
    form = ""
    return render(
        request,
        "transactions/add.html",
        {
            "page_name": transaction_type,
            "form": form,
        },
    )

@login_required
def transaction_edit(request, transaction_type, expense_id):
    """Generate and processes form to edit a financial system"""
    """
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
    """
    return render(
        request,
        "transactions/edit.html",
        {
            "page_name": "expense",
            "form": form,
        },
    )

@login_required
def transaction_delete(request, transaction_type, expense_id):
    """Generates and handles delete requests of financial system"""
    """
    # Get the FinancialSystem instance for this user
    system = get_object_or_404(FinancialCodeSystem, id=system_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        system.delete()

        # Redirect back to main list
        messages.success(request, "Financial code system deleted")

        return HttpResponseRedirect(reverse('financial_codes_dashboard'))
    """
    return render(
        request,
        "financial_codes/delete.html",
        {
            "page_name": "expense",
            "title": system.title,
        },
    )
