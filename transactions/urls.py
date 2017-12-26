"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, transaction_add, transaction_edit, transaction_delete
)
# pylint: disable=invalid-name
urlpatterns = [
    url(
        r"^(?P<transaction_type>(expense|revenue))/add$",
        transaction_add,
        name="transaction_add",
    ),
    url(
        r"^(?P<transaction_type>(expense|revenue))/edit/(?P<system_id>\d+)$",
        transaction_edit,
        name="transaction_edit",
    ),
    url(
        r"^(?P<transaction_type>(expense|revenue))/delete/(?P<system_id>\d+)$",
        transaction_edit,
        name="transaction_edit",
    ),
    url(r"^$", dashboard, name="transactions_dashboard"),
]
