"""Models for the financial_codes app"""

from django.db import models

from simple_history.models import HistoricalRecords

class BudgetYear(models.Model):
    """Start and end dates of the budget year"""
    date_start = models.DateField(
        help_text="First day of the budget year",
    )
    date_end = models.DateField(
        help_text="Last day of the budget year",
    )
    history = HistoricalRecords()

class FinancialCodeSystem(models.Model):
    """Name and description of a financial code system"""
    title = models.CharField(
        help_text="Title of the financial code system",
        max_length=100,
    )
    status = models.CharField(
        choices=(
            ("a", "Active"),
            ("i", "Inactive")
        ),
        default="a",
        help_text="Current status of this code system",
        max_length=1,
    )
    history = HistoricalRecords()

class FinancialCodeGroup(models.Model):
    """A grouping for a set of Financial Codes"""
    title = models.CharField(
        help_text="Title of the financial code grouping",
        max_length=100,
    )
    description = models.CharField(
        help_text="Expanded description of the financial code gouping",
        max_length=500,
    )
    status = models.CharField(
        choices=(
            ("a", "Active"),
            ("i", "Inactive")
        ),
        help_text="Current status of this code system",
        max_length=1,
    )
    history = HistoricalRecords()

class FinancialCode(models.Model):
    """Holds data on an individual financial code"""
    code_system = models.ForeignKey(
        FinancialCodeSystem,
        on_delete=models.CASCADE,
    )
    code_group = models.ForeignKey(
        FinancialCodeGroup,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    budget_year = models.ForeignKey(
        BudgetYear,
        on_delete=models.PROTECT,
    )
    code = models.CharField(
        help_text="The numerical code for this financial code",
        max_length=6,
    )
    description = models.CharField(
        help_text="Description of this financial code",
        max_length=100,
    )
    history = HistoricalRecords()
