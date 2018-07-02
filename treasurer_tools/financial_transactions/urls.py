"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, request_transactions_list, transaction_add,
    transaction_edit, transaction_delete
)

app_name = "financial_transactions"

urlpatterns = [
    url(r"^(?P<t_type>(expense|revenue))/add/$", transaction_add, name="add",),
    url(r"^(?P<t_type>(expense|revenue))/edit/(?P<transaction_id>\d+)$", transaction_edit, name="edit",),
    url(r"^(?P<t_type>(expense|revenue))/delete/(?P<transaction_id>\d+)$", transaction_delete, name="delete",),
    url(r"^retrieve-transactions/", request_transactions_list),
    url(r"^$", dashboard, name="dashboard"),
]
