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
    data = []
    system_index = 0

    # Get all the Financial Code Systems
    systems = FinancialCodeSystem.objects.all()

    # Get each financial code group releative to its parents
    for system in systems:
        data.append({
            "system": system,
            "budget_years": [],
        })

        year_index = 0
        budget_years = system.budgetyear_set.all()

        for year in budget_years:
            data[system_index]["budget_years"].append({
                "budget_year": year,
                "revenue_groups": [],
                "expense_groups": [],
            })

            financial_code_groups = year.financialcodegroup_set.all()

            for group in financial_code_groups:
                if group.type == "r":
                    data[system_index]["budget_years"][year_index]["revenue_groups"].append({
                        "financial_code_group": group,
                        "financial_codes": group.financialcode_set.all(),
                    })
                elif group.type == "e":
                    data[system_index]["budget_years"][year_index]["expense_groups"].append({
                        "financial_code_group": group,
                        "financial_codes": group.financialcode_set.all(),
                    })
            year_index = year_index + 1
        system_index = system_index + 1

    return render(
        request,
        "financial_codes/index.html",
        context={
            "data": data
        },
    )

@login_required
def system_add(request):
    """Generates and processes form to add financial code system"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        form = FinancialCodeSystemForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Financial code system successfully added")

            return HttpResponseRedirect(reverse("financial_codes:dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = FinancialCodeSystemForm()

    return render(
        request,
        "financial_codes/add_edit.html",
        {
            "page_name": "Add New Financial System",
            "form": form,
            "submit_button": "Add new financial system",
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
            form.save()

            # redirect to a new URL:
            messages.success(request, "Financial code system successfully edited")

            return HttpResponseRedirect(reverse("financial_codes:dashboard"))

    # If this is a GET (or any other method) populate the default form.
    else:
        # Get initial form data
        system_data = get_object_or_404(FinancialCodeSystem, id=system_id)

        form = FinancialCodeSystemForm(instance=system_data)

    return render(
        request,
        "financial_codes/add_edit.html",
        {
            "page_name": "Edit Financial Code System",
            "form": form,
            "submit_button": "Save changes"
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

        return HttpResponseRedirect(reverse('financial_codes:dashboard'))

    return render(
        request,
        "financial_codes/delete.html",
        {
            "page_name": "financial code system",
            "delete_message": "financial code system",
            "delete_restriction": (
                "Note: A financial code system can only be deleted when there"
                "are no transactions assigned to it."
            ),
            "item_to_delete": system.title,
        },
    )

@login_required
def year_add(request):
    """Generates and processes form to add a new budget year"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        form = BudgetYearForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Budget year successfully added")

            return HttpResponseRedirect(reverse("financial_codes:dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = BudgetYearForm()

    return render(
        request,
        "financial_codes/add_edit.html",
        {
            "page_name": "Add New Budget Year",
            "form": form,
            "submit_button": "Add new budget year",
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
            form.save()

            # redirect to a new URL:
            messages.success(request, "Budget year successfully edited")

            return HttpResponseRedirect(reverse("financial_codes:dashboard"))

    # If this is a GET (or any other method) populate the default form.
    else:
        # Get initial form data
        year_data = get_object_or_404(BudgetYear, id=year_id)

        form = BudgetYearForm(instance=year_data)

    return render(
        request,
        "financial_codes/add_edit.html",
        {
            "page_name": "Edit Budget Year",
            "form": form,
            "submit_button": "Save changes",
        },
    )

@login_required
def year_delete(request, year_id):
    """Generates and processes form to delete a budget year"""
        # Get the BudgetYear instance for this user
    year = get_object_or_404(BudgetYear, id=year_id)

    # If this is a POST request then process the Form data
    if request.method == "POST":
        year.delete()

        # Redirect back to main list
        messages.success(request, "Budget year deleted")

        return HttpResponseRedirect(reverse('financial_codes:dashboard'))

    return render(
        request,
        "financial_codes/delete.html",
        {
            "page_name": "budget year",
            "delete_message": "budget year",
            "delete_restriction": (
                "Note: A budget year only be deleted when there are no "
                "transactions assigned to it."
            ),
            "item_to_delete": str(year),
        },
    )

@login_required
def year_copy(request, year_id):
    """Copies a budget year's codes into a new budget year"""
    # Retrieve the old budget year to copy from
    old_year = get_object_or_404(BudgetYear, id=year_id)

    # If this is a POST request then copy the budget year
    if request.method == "POST":
        # Populate the new budget year data
        form = BudgetYearForm(request.POST)

        # Validate the new budget year data
        if form.is_valid():
            # Create the new budget year
            new_year = form.save()

            # Cycle through each financial code group in old budget year
            for group in old_year.financialcodegroup_set.all():
                # Copy the financial code group
                new_group = FinancialCodeGroup.objects.create(
                    budget_year=new_year,
                    title=group.title,
                    description=group.description,
                    type=group.type,
                    status=group.status,
                )

                # Cycle through each financial code in old budget year
                for code in group.financialcode_set.all():
                    # Copy the financial codes over
                    FinancialCode.objects.create(
                        financial_code_group=new_group,
                        code=code.code,
                        description=code.description,
                    )

            # redirect to the dashboard
            messages.success(request, "Budget year successfully copied")

            return HttpResponseRedirect(reverse("financial_codes:dashboard"))
    else:
        form = BudgetYearForm()

    # Get the revenue and expense groups
    revenue_groups = old_year.financialcodegroup_set.filter(type="r")
    expense_groups = old_year.financialcodegroup_set.filter(type="e")

    return render(
        request,
        "financial_codes/copy.html",
        {
            "budget_year": old_year,
            "revenue_groups": revenue_groups,
            "expense_groups": expense_groups,
            "form": form,
        },
    )

@login_required
def group_add(request):
    """Generates and processes form to add a new financial code group"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        # Create a form instance and populate it with data from the request (binding):
        form = FinancialCodeGroupForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Financial code group successfully added")

            return HttpResponseRedirect(reverse("financial_codes:dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = FinancialCodeGroupForm()

    return render(
        request,
        "financial_codes/add_edit.html",
        {
            "page_name": "Add New Financial Code Group",
            "form": form,
            "submit_button": "Add new financial code group",
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
            form.save()

            # redirect to a new URL:
            messages.success(request, "Financial code group successfully edited")

            return HttpResponseRedirect(reverse("financial_codes:dashboard"))

    # If this is a GET (or any other method) populate the default form.
    else:
        # Get initial form data
        group_data = get_object_or_404(FinancialCodeGroup, id=group_id)

        form = FinancialCodeGroupForm(instance=group_data)

    return render(
        request,
        "financial_codes/add_edit.html",
        {
            "page_name": "Edit Financial Code Group",
            "form": form,
            "submit_button": "Save changes",
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

        return HttpResponseRedirect(reverse('financial_codes:dashboard'))

    return render(
        request,
        "financial_codes/delete.html",
        {
            "page_name": "financial code group",
            "delete_message": "financial code group",
            "delete_restriction": (
                "Note: A financial code group can only be deleted when there"
                "are no transactions assigned to it."
            ),
            "item_to_delete": group.title,
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
            form.save()

            # redirect to a new URL:
            messages.success(request, "Financial code successfully added")

            return HttpResponseRedirect(reverse("financial_codes:dashboard"))

    # If this is a GET (or any other method) create the default form.
    else:
        form = FinancialCodeForm()

    return render(
        request,
        "financial_codes/code_add_edit.html",
        {
            "page_name": "Add New Financial Code",
            "form": form,
            "submit_button": "Add new financial code",
        },
    )

@login_required
def code_edit(request, code_id):
    """Generates and processes form to edit a financial code"""
    # If this is a POST request then process the Form data
    if request.method == "POST":
        code_data = get_object_or_404(FinancialCode, id=code_id)  # pylint: disable=no-member

        # Create a form instance and populate it with data from the request (binding):
        form = FinancialCodeForm(request.POST, instance=code_data)

        # Check if the form is valid:
        if form.is_valid():
            form.save()

            # redirect to a new URL:
            messages.success(request, "Financial code successfully added")

            return HttpResponseRedirect(reverse("financial_codes:dashboard"))

    # If this is a GET (or any other method) populate the default form.
    else:
        # Get initial form data
        code_data = get_object_or_404(FinancialCode, id=code_id)

        form = FinancialCodeForm(instance=code_data)

    return render(
        request,
        "financial_codes/code_add_edit.html",
        {
            "page_name": "Edit Financial Code",
            "form": form,
            "submit_button": "Save changes",
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

        return HttpResponseRedirect(reverse('financial_codes:dashboard'))

    return render(
        request,
        "financial_codes/delete.html",
        {
            "page_name": "financial code",
            "delete_message": "financial code",
            "delete_restriction": (
                "Note: A financial code only be deleted when there are no "
                "transactions assigned to it."
            ),
            "item_to_delete": str(code),
        },
    )
