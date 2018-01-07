"""Models for the financial_codes app"""

from django.db import models

from simple_history.models import HistoricalRecords

class FinancialCodeSystem(models.Model):
    """Name and description of a financial code system"""
    title = models.CharField(
        help_text="Title of the financial code system",
        max_length=100,
    )
    date_start = models.DateField(
        help_text="First day this assignment applies to",
        verbose_name="start date"
    )
    date_end = models.DateField(
        blank=True,
        help_text="Last day this assignment applies to (leave blank for no end date)",
        null=True,
        verbose_name="end date"
    )
    history = HistoricalRecords()

    def __str__(self):
        if self.date_end:
            return_string = "{} ({} to {})".format(
                self.title, self.date_start, self.date_end
            )
        else:
            return_string = "{} ({} to Present)".format(
                self.title, self.date_start
            )
        
        return return_string
    
class BudgetYear(models.Model):
    """Start and end dates of the budget year"""
    financial_code_system = models.ForeignKey(
        FinancialCodeSystem,
        on_delete=models.PROTECT,
        help_text="The financial code system that this budget year applies to",
    )
    date_start = models.DateField(
        help_text="First day of the budget year",
        verbose_name="start date",
    )
    date_end = models.DateField(
        help_text="Last day of the budget year",
        verbose_name="end date",
    )
    history = HistoricalRecords()

    def __str__(self):
        return "{} to {}".format(self.date_start, self.date_end)

class FinancialCodeGroup(models.Model):
    """A grouping for a set of Financial Codes"""
    budget_year = models.ForeignKey(
        BudgetYear,
        on_delete=models.PROTECT,
        help_text="The budget year that this group applies to",
    )
    title = models.CharField(
        help_text="Title of the financial code grouping",
        max_length=100,
    )
    description = models.CharField(
        help_text="Expanded description of the financial code gouping",
        max_length=500,
    )
    type = models.CharField(
        choices=(
            ("e", "Expense"),
            ("r", "Revenue"),
        ),
        default="e",
        max_length=1,
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

    def __str__(self):
        if self.type == "e":
            return_str = "Expense - {}".format(self.title)
        elif self.type == "r":
            return_str = "Revenue - {}".format(self.title)

        return return_str

class FinancialCode(models.Model):
    """Holds data on an individual financial code"""
    financial_code_group = models.ForeignKey(
        FinancialCodeGroup,
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

    def __str__(self):
        return "{} - {}".format(self.code, self.description)
