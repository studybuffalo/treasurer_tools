"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, retrieve_transactions, match_transactions, unmatch_transactions
)

urlpatterns = [
    url(r"^retrieve-transactions/", retrieve_transactions),
    url(r"^match-transactions/", match_transactions),
    url(r"^unmatch-transactions/", unmatch_transactions),
    url(r"^$", dashboard, name="dashboard"),
]
