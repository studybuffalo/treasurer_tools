"""Models for bank_transaction app"""
from django.db import models

from simple_history.models import HistoricalRecords


class Institution(models.Model):
    """Details on the bank/financial institution"""
    name = models.CharField(
        help_text="Name of the bank/financial institution",
        max_length=250,
    )
    address = models.CharField(
        max_length=1000,
    )
    phone = models.CharField(
        max_length=30,
        verbose_name="phone number",
    )
    fax = models.CharField(
        max_length=30,
        verbose_name="fax number",
    )
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Account(models.Model):
    """A single account associated with an institution"""
    institution = models.ForeignKey(
        Institution,
        help_text="The bank this account is associated with",
        on_delete=models.CASCADE,
    )
    account_number = models.CharField(
        help_text="The account number/reference for this account",
        max_length=100,
    )
    name = models.CharField(
        help_text="The name of the account",
        max_length=100,
    )
    status = models.CharField(
        choices=(
            ("a", "Active"),
            ("i", "Inactive"),
        ),
        default="a",
        help_text="The account status",
        max_length=1,
    )
    history = HistoricalRecords()

    def __str__(self):
        return "{} {} ({})".format(
            self.institution, self.name, self.account_number
        )
