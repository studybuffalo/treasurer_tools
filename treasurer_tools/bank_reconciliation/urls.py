"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, retrieve_transactions, retrieve_matches, match_transactions, unmatch_transactions
)

app_name = "bank_reconciliation"

urlpatterns = [
    url(r"^retrieve-transactions/", retrieve_transactions),
    url(r"^retrieve-matches/", retrieve_matches),
    url(r"^match-transactions/", match_transactions),
    url(r"^unmatch-transactions/", unmatch_transactions),
    url(r"^$", dashboard, name="dashboard"),
]
