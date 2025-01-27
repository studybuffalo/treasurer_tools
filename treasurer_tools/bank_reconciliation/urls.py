"""Expense Transaction URLs"""
from django.urls import path

from .views import (
    dashboard, retrieve_transactions, retrieve_matches, match_transactions, unmatch_transactions
)

app_name = "bank_reconciliation"

urlpatterns = [
    path('retrieve-transactions/', retrieve_transactions),
    path('retrieve-matches/', retrieve_matches),
    path('match-transactions/', match_transactions),
    path('unmatch-transactions/', unmatch_transactions),
    path('', dashboard, name="dashboard"),
]
