from django.contrib.auth.models import User
from django.db import models

from simple_history.models import HistoricalRecords

class Country(models.Model):
    """Possible countries for the demographics list"""
    country_code = models.CharField(
        max_length=2,
    )
    country_name = models.CharField(
        max_length=50,
    )

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.country_name

class Demographics(models.Model):
    """Demographic details for payees/payers"""
    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        unique=True,
    )
    name = models.CharField(
        help_text="The individual, company, or organization name",
        max_length=256,
    )
    address = models.CharField(
        help_text="The Mailing address for this individual",
        max_length=1000,
    )
    city = models.CharField(
        max_length=1000,
    )
    province = models.CharField(
        help_text="Mailing address province, state, etc.",
        max_length=100,
    )
    country = models.ForeignKey(
        Country,
        null=True,
        on_delete=models.SET_NULL,
    )
    postal_code = models.CharField(
        help_text="Mailing address postal code, zip code, etc.",
        max_length=10,
    )
    phone = models.CharField(
        max_length=20,
    )
    fax = models.CharField(
        blank=True,
        max_length=20,
        null=True,
    )
    email = models.EmailField()
    status = models.CharField(
        choices=(
            ("a", "active"),
            ("i", "inactive"),
        ),
        help_text=(
            "Whether this individual has current activity expenses or revenue"
        ),
        max_length=2,
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Demographics"

    def __str__(self):
        return self.name
