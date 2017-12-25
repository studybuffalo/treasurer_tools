"""Models for the investment app"""

from django.db import models

from simple_history.models import HistoricalRecords


class Investment(models.Model):
    """Records data on financial invetments"""
    name = models.CharField(
        help_text="Name to identify the investment",
        max_length=256,
    )
    date_invested = models.DateField(
        help_text="Date of initial investment",
    )
    amount = models.DecimalField(
        decimal_places=2,
        help_text="Initial amount invested",
        max_digits=12,
    )
    rate = models.CharField(
        help_text="Details on rate, term duration, etc.",
        max_length=256,
    )
    history = HistoricalRecords()
