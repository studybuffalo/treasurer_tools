"""Models for the payee_payer app"""
from config.settings.base import AUTH_USER_MODEL
from django.db import models

from simple_history.models import HistoricalRecords


class Country(models.Model):
    """Possible countries for the demographics list"""
    # pylint: disable=missing-docstring,too-few-public-methods

    country_code = models.CharField(
        max_length=2,
    )
    country_name = models.CharField(
        max_length=50,
    )

    class Meta:
        verbose_name_plural = "countries"

    def __str__(self):
        return self.country_name

class PayeePayer(models.Model):
    """Payee/Payer details"""
    # pylint: disable=missing-docstring,too-few-public-methods

    user = models.OneToOneField(
        AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        unique=True,
    )
    name = models.CharField(
        help_text="The individual, company, or organization name",
        max_length=250,
        unique=True,
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
        blank=True,
        help_text="Mailing address postal code, zip code, etc.",
        max_length=10,
        null=True,
    )
    phone = models.CharField(
        blank=True,
        max_length=30,
        null=True,
        verbose_name="phone number",
    )
    fax = models.CharField(
        blank=True,
        max_length=30,
        null=True,
        verbose_name="fax number",
    )
    email = models.EmailField(
        blank=True,
        null=True,
    )
    status = models.CharField(
        choices=(
            ("a", "active"),
            ("i", "inactive"),
        ),
        help_text=(
            "Whether this individual has recent expense or revenue activity"
        ),
        max_length=2,
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "Payee/Payers"

    def __str__(self):
        return self.name
