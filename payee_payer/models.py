from django.contrib.auth.models import User
from django.db import models

from simple_history.models import HistoricalRecords

from payee_payer.services import get_country_list

class Demographics(models.Model):
    """Demographic details for payees/payers"""
    user = models.OneToOneField(
        User,
        unique=True,
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=256,
    )
    address = models.CharField(
        max_length=1000,
    )
    city = models.CharField(
        max_length=1000,
    )
    province = models.CharField(
        max_length=100,
    )
    country = models.CharField(
        choices=get_country_list(),
        max_length=2,
    )
    postal_code = models.CharField(
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
        max_length=2,
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name_plural = "demographics"

    def __str__(self):
        return self.name