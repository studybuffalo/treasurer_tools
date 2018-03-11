#"""Models for the Reports app"""

#from simple_history.models import HistoricalRecords

#from django.db import models

#from financial_codes.models import BudgetYear
#from financial_transactions.models import Item


#class BudgetYearMatch(models.Model):
#    """Model to match financial transaction items to budget years"""
#    item = models.ForeignKey(
#        Item,
#        on_delete=models.CASCADE,
#    )
#    budget_year = models.ForeignKey(
#        BudgetYear,
#        on_delete=models.CASCADE,
#    )
#    history = HistoricalRecords()

#    def __str__(self):
#        return ""