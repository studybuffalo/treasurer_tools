from django.conf import settings
from django.db import models

from simple_history.models import HistoricalRecords

class BranchMember(models.Model):
    """Many-To-Many through model for user-branch relations"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    branch = models.ForeignKey(
        "Branch",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{} - {}".format(self.branch.name_short, self.user.name)

class Branch(models.Model):
    """Details on the branch"""
    name_full = models.CharField(
        help_text="The full name of the branch",
        max_length=255,
    )
    name_short = models.CharField(
        help_text="The abbreviated name of the branch",
        max_length=255,
    )
    contact_name = models.CharField(
        help_text="The main contact for the branch",
        max_length=255,
        blank=True,
        null=True,
    )
    address = models.TextField(
        help_text="The full address of the branch",
        max_length=1000,
        blank=True,
        null=True,
    )
    phone = models.CharField(
        help_text="The main phone number for the branch",
        max_length=20,
        blank=True,
        null=True,
    )
    fax = models.CharField(
        help_text="The main fax number for the branch",
        max_length=20,
        blank=True,
        null=True,
    )
    email = models.CharField(
        help_text="The main email for the branch",
        max_length=255,
        blank=True,
        null=True,
    )
    logo_large = models.ImageField(
        help_text="A logo for the branch",
        blank=True,
        null=True,
    )
    logo_small = models.ImageField(
        help_text="A reduced width logo for smaller screens",
        blank=True,
        null=True,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.name_full
