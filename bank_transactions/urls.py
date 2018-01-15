"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, statement_add, statement_edit, statement_delete, reconciliation,
    retrieve_transactions
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^statement/add/$", statement_add, name="statement_add"),
    url(r"^statement/edit/(?P<statement_id>\d+)$", statement_edit, name="statement_edit"),
    url(r"^statement/delete/(?P<statement_id>\d+)$", statement_delete, name="statement_delete"),
    url(r"^$", dashboard, name="bank_dashboard"),
    url(r"^reconciliation/retrieve-transactions/", retrieve_transactions),
    url(r"^reconciliation/$", reconciliation, name="banking_reconciliation"),
]
