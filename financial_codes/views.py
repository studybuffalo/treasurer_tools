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
    FinancialCodeSystemForm, FinancialCodeGroupForm, BudgetYearForm,
    FinancialCodeForm,
)

@login_required
def dashboard(request):
    """Main dashboard to manage financial codes"""
    # pylint: disable=no-member
    systems = FinancialCodeSystem.objects.all()
    groups = FinancialCodeGroup.objects.all()
    years = BudgetYear.objects.all()
    codes = FinancialCode.objects.all()

    return render(
        request,
        "financial_codes/index.html",
        context={
            "systems": systems,
            "groups": groups,
            "years": years,
            "codes": codes,
        },
    )

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
        "financial_codes/add.html",
        {
            "page_name": "financial system",
            "form": form,
        },
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
        "financial_codes/edit.html",
        {
            "page_name": "financial code system",
            "form": form,
        },
    )

@login_required
def system_delete(request, system_id):
    """Generates and handles delete requests of financial system"""
    # Get the FinancialSystem instance for this user
    system = get_object_or_404(FinancialCodeSystem, id=system_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        system.delete()

        # Redirect back to main list
        messages.success(request, "Financial code system deleted")

        return HttpResponseRedirect(reverse('financial_codes_dashboard'))

    return render(
        request,
        "financial_codes/delete.html",
        {
            "page_name": "financial code system",
            "title": system.title,
        },
    )

@login_required
def group_add(request):
    """Generates and processes form to add a new financial code group"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        group_data = FinancialCodeGroup()

        # Create a form instance and populate it with data from the request (binding):
        form = FinancialCodeGroupForm(request.POST, instance=group_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            financial_code_system = form.cleaned_data["financial_code_system"]
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            status = form.cleaned_data["status"]

            # Update the FinancialCodeGroup model object
            group_data.financial_code_system = financial_code_system
            group_data.title = title
            group_data.description = description
            group_data.status = status

            group_data.save()

            # redirect to a new URL:
            messages.success(request, "Financial code group successfully added")

            return HttpResponseRedirect(reverse("financial_codes_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = FinancialCodeGroupForm(initial={})

    return render(
        request,
        "financial_codes/add.html",
        {
            "page_name": "financial code group",
            "form": form
        },
    )

@login_required
def group_edit(request, group_id):
    """Generates and processes form to edit a financial code group"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        group_data = get_object_or_404(FinancialCodeGroup, id=group_id)

        # Create a form instance and populate it with data from the request (binding):
        form = FinancialCodeGroupForm(request.POST, instance=group_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            status = form.cleaned_data["status"]

            # Update the Financial Systems object
            group_data.title = title
            group_data.description = description
            group_data.status = status

            group_data.save()

            # redirect to a new URL:
            messages.success(request, "Financial code group successfully edited")

            return HttpResponseRedirect(reverse("financial_codes_dashboard"))

    # If this is a GET (or any other method) populate the default form.
    else:
        # Get initial form data
        group_data = get_object_or_404(FinancialCodeGroup, id=group_id)

        form = FinancialCodeGroupForm(initial={
            "title": group_data.title,
            "description": group_data.description,
            "status": group_data.status,
        })

    return render(
        request,
        "financial_codes/edit.html",
        {
            "page_name": "financial code group",
            "form": form,
        },
    )

@login_required
def group_delete(request, group_id):
    """Generates and processes form to delete financial code group"""
    # Get the FinancialCodeGroup instance for this user
    group = get_object_or_404(FinancialCodeGroup, id=group_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        group.delete()

        # Redirect back to main list
        messages.success(request, "Financial code group deleted")

        return HttpResponseRedirect(reverse('financial_codes_dashboard'))

    return render(
        request,
        "financial_codes/group_delete.html",
        {
            "page_name": "financial code group",
            "title": group.title,
        },
    )

@login_required
def year_add(request):
    """Generates and processes form to add a new budget year"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        year_data = BudgetYear()

        # Create a form instance and populate it with data from the request (binding):
        form = BudgetYearForm(request.POST, instance=year_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            date_start = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]

            # Update the FinancialSystem model object
            year_data.date_start = date_start
            year_data.date_end = date_end

            year_data.save()

            # redirect to a new URL:
            messages.success(request, "Budget year successfully added")

            return HttpResponseRedirect(reverse("financial_codes_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = BudgetYearForm()

    return render(
        request,
        "financial_codes/add.html",
        {
            "page_name": "budget year",
            "form": form,
        },
    )

@login_required
def year_edit(request, year_id):
    """Generates and processes form to edit a budget year"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        year_data = get_object_or_404(BudgetYear, id=year_id)

        # Create a form instance and populate it with data from the request (binding):
        form = BudgetYearForm(request.POST, instance=year_data)

        # Check if the form is valid:
        if form.is_valid():
            date_start = form.cleaned_data["date_start"]
            date_end = form.cleaned_data["date_end"]

            # Update the FinancialSystem model object
            year_data.date_start = date_start
            year_data.date_end = date_end

            year_data.save()

            # redirect to a new URL:
            messages.success(request, "Budget year successfully edited")

            return HttpResponseRedirect(reverse("financial_codes_dashboard"))

    # If this is a GET (or any other method) populate the default form.
    else:
        # Get initial form data
        year_data = get_object_or_404(BudgetYear, id=year_id)

        form = BudgetYearForm(initial={
            "date_start": year_data.date_start,
            "date_end": year_data.date_end,
        })

    return render(
        request,
        "financial_codes/edit.html",
        {
            "page_name": "budget year",
            "form": form,
        },
    )

@login_required
def year_delete(request, year_id):
    """Generates and processes form to delete a budget year"""
        # Get the BudgetYear instance for this user
    year = get_object_or_404(FinancialCodeGroup, id=year_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        year.delete()

        # Redirect back to main list
        messages.success(request, "Budget yeardeleted")

        return HttpResponseRedirect(reverse('financial_codes_dashboard'))

    return render(
        request,
        "financial_codes/delete.html",
        {
            "page_name": "budget year",
            "title": str(year),
        },
    )

@login_required
def code_add(request):
    """Generates and processes form to add a new financial code"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        code_data = FinancialCode()

        # Create a form instance and populate it with data from the request (binding):
        form = FinancialCodeForm(request.POST, instance=code_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            code = form.cleaned_data["code"]
            description = form.cleaned_data["description"]
            code_system = form.cleaned_data["code_system"]
            code_group = form.cleaned_data["code_group"]
            budget_year = form.cleaned_data["budget_year"]

            # Update the Demographics model object
            code_data.code = code
            code_data.description = description
            code_data.code_system = code_system
            code_data.code_group = code_group
            code_data.budget_year = budget_year

            code_data.save()

            # redirect to a new URL:
            messages.success(request, "Financial code successfully added")

            return HttpResponseRedirect(reverse("financial_codes_dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = FinancialCodeForm(initial={})

    return render(
        request,
        "financial_codes/add.html",
        {
            "page_name": "financial code",
            "form": form,
        },
    )

@login_required
def code_edit(request, code_id):
    """Generates and processes form to edit a financial code"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        code_data = FinancialCode().objects.get(id=code_id)  # pylint: disable=no-member

        # Create a form instance and populate it with data from the request (binding):
        form = FinancialCodeForm(request.POST, instance=code_data)

        # Check if the form is valid:
        if form.is_valid():
            # Collect the form fields
            code = form.cleaned_data["code"]
            description = form.cleaned_data["description"]
            code_system = form.cleaned_data["code_system"]
            code_group = form.cleaned_data["code_group"]
            budget_year = form.cleaned_data["budget_year"]

            # Update the Demographics model object
            code_data.code = code
            code_data.description = description
            code_data.code_system = code_system
            code_data.code_group = code_group
            code_data.budget_year = budget_year

            code_data.save()

            # redirect to a new URL:
            messages.success(request, "Financial code successfully added")

            return HttpResponseRedirect(reverse("financial_codes_dashboard"))

    # If this is a GET (or any other method) populate the default form.
    else:
        # Get initial form data
        code_data = get_object_or_404(FinancialCode, id=code_id)

        form = FinancialCodeForm(initial={
            "code": code_data.code,
            "description": code_data.description,
            "code_system": code_data.code_system,
            "code_group": code_data.code_group,
            "budget_year": code_data.budget_year,
        })

    return render(
        request,
        "financial_codes/edit.html",
        {
            "page_name": "financial code",
            "form": form,
        },
    )

@login_required
def code_delete(request, code_id):
    """Generates and processes deletion of financial code"""
     # Get the Shift Code instance for this user
    code = get_object_or_404(FinancialCode, id=code_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        code.delete()

        # Redirect back to main list
        messages.success(request, "Financial code deleted")

        return HttpResponseRedirect(reverse('financial_code_dashboard'))

    return render(
        request,
        "financial_code/delete.html",
        {
            "page_name": "financial code",
            "title": str(code),
        },
    )
