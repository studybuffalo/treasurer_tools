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
    )
    address = models.TextField(
        help_text="The full address of the branch",
        max_length=1000,
    )
    phone = models.CharField(
        help_text="The main phone number for the branch",
        max_length=20,
    )
    fax = models.CharField(
        help_text="The main fax number for the branch",
        max_length=20,
    )
    email = models.CharField(
        help_text="The main email for the branch",
        max_length=255,
    )
    logo_large = models.ImageField(
        help_text="A logo for the branch",
    )
    logo_small = models.ImageField(
        help_text="A reduced width logo for smaller screens",
    )
    member = models.ManyToManyField(
        to=settings.AUTH_USER_MODEL,
        through=BranchMember,
    )

    history = HistoricalRecords()

    def __str__(self):
        return self.branch_name

