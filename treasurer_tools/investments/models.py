"""Models for the investment app"""

from django.db import models

from simple_history.models import HistoricalRecords

from bank_reconciliation.models import ReconciliationGroup


class Investment(models.Model):
    """Records data on financial invetments"""
    name = models.CharField(
        help_text="Name to identify the investment",
        max_length=256,
    )
    rate = models.CharField(
        help_text="Details on rate, term duration, etc.",
        max_length=256,
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name

class InvestmentDetail(models.Model):
    STATUS_CHOICES = (
        ("v", "invested"),
        ("m", "matured"),
        ("i", "interest paid"),
        ("c", "cancelled"),
    )

    investment = models.ForeignKey(
        Investment,
        on_delete=models.CASCADE,
        related_name="investmentdetails",
    )
    date_investment = models.DateField()
    detail_status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
    )
    amount = models.DecimalField(
        decimal_places=2,
        default=0,
        help_text="The amount invested, matured, or paid out",
        max_digits=12,
    )
    reconciled = models.ForeignKey(
        ReconciliationGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="investmentdetails",
    )

    def __str__(self):
        return "{} ({} ${})".format(self.investment, self.detail_status, self.amount)
