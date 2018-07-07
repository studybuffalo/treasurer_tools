"""Forms for the financial_codes app"""

from django import forms
from django.core.exceptions import ValidationError

from .models import (
    BudgetYear, FinancialCodeSystem, FinancialCodeGroup, FinancialCode,
)
from .widgets import FinancialCodeGroupWithYearID

def get_years_with_opt_groups():
    """Creates nested dictionary financial code systems & budget years"""
    budget_year_choices = []

    for system in FinancialCodeSystem.objects.all():
        budget_years = []

        for budget_year in system.budgetyear_set.all():
            budget_years.append([budget_year.id, budget_year])

        budget_year_choices.append([system, budget_years])

    return budget_year_choices

class FinancialCodeSystemForm(forms.ModelForm):
    """Form to add & edit entries in the FinancialCodeSystem model"""

    class Meta:
        model = FinancialCodeSystem

        fields = [
            "title",
            "date_start",
            "date_end",
        ]

    def clean_date_end(self):
        """Checks that a valid date is provided"""
        # Get date_start (if provided)
        try:
            date_start = self.cleaned_data["date_start"]
        except KeyError:
            date_start = None

        # Get date_end
        date_end = self.cleaned_data["date_end"]

        # Check that the end date is greater than the start date
        if date_end:
            if date_start and date_end < date_start:
                raise ValidationError("The end date must occur after the start date.")

        return date_end

class BudgetYearForm(forms.ModelForm):
    """Form to add and edit budget years"""
    class Meta:
        model = BudgetYear

        fields = [
            "financial_code_system",
            "date_start",
            "date_end",
        ]

    def clean_date_end(self):
        # Get date_start (if provided)
        try:
            date_start = self.cleaned_data["date_start"]
        except KeyError:
            date_start = None

        # Get date_end
        date_end = self.cleaned_data["date_end"]

        # Check that the start date occurs before the end date
        if date_start and date_end and date_start > date_end:
            raise ValidationError("The end date must occur after the start date.")

        return date_end

    def clean(self):
        form_data = self.cleaned_data

        # Collect all required data for validation
        try:
            date_start_year = form_data["date_start"]
            date_end_year = form_data["date_end"]
            system = form_data["financial_code_system"]
        except KeyError:
            date_start_year = None
            date_end_year = None
            system = None

        # Check that dates occur within financial code system dates
        if date_start_year and date_end_year and system:
            date_start_system = system.date_start
            date_end_system = system.date_end

            # Check that start date occurs after financial code system start date
            if date_start_year < date_start_system:
                raise ValidationError({
                    "date_start": "The start date must occur after the start of the Financial Code System."
                })

            if date_end_system and date_end_year > date_end_system:
                raise ValidationError({
                    "date_end": "The end date must occur before the end of the Financial Code System."
                })

        return form_data

class FinancialCodeGroupForm(forms.ModelForm):
    """Form to add and edit financial code systems"""
    class Meta:
        model = FinancialCodeGroup

        fields = [
            "budget_year",
            "title",
            "description",
            "type",
            "status",
        ]

    def __init__(self, *args, **kwargs):
        super(FinancialCodeGroupForm, self).__init__(*args, **kwargs)

        self.fields["budget_year"].choices = get_years_with_opt_groups()

class FinancialCodeForm(forms.ModelForm):
    """Form to add and edit financial codes"""
    budget_year = forms.ChoiceField(
        choices=[],
        label="Budget Year",
        required=False,
    )

    class Meta:
        model = FinancialCode

        fields = [
            "budget_year",
            "financial_code_group",
            "code",
            "description",
        ]

        widgets = {
            "financial_code_group": FinancialCodeGroupWithYearID(),
        }

    def __init__(self, *args, **kwargs):
        super(FinancialCodeForm, self).__init__(*args, **kwargs)

        # Add the budget year choices
        self.fields["budget_year"].choices = get_years_with_opt_groups()

        # Set the proper default budget year (if applicable)
        if self.instance.id:
            self.fields["budget_year"].initial = self.instance.financial_code_group.budget_year.id
