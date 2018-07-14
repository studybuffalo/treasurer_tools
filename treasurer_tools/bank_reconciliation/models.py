"""Models for the bank_reconcilation app"""
from django.db import models

from simple_history.models import HistoricalRecords


class ReconciliationGroup(models.Model):
    history = HistoricalRecords()
