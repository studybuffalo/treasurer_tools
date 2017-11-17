from django.db import models

from simple_history.models import HistoricalRecords

class Demographics(models.Model):
    """Demographic details for payees/payers"""
    name = models.CharField()
    address = models.CharField()
    city = models.CharField()
    province = models.CharField()
    country = models.CharField()
    postal_code = models.CharField()
    phone = models.CharField()
    fax = models.CharField()
    email = models.EmailField()
    status = models.CharField()
    user_modified = models.ForeignKey()
    date_modified = models.DateTimeField()
    history = HistoricalRecords()
    class Meta:
        None

    def __str__(self):
        return ""