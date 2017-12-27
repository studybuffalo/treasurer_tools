"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard
)
# pylint: disable=invalid-name
urlpatterns = [
    url(r"^$", dashboard, name="bank_dashboard"),
]
"""
url(
    r"^(?P<t_type>(expense|revenue))/add$",
    transaction_add,
    name="transaction_add",
),
url(
    r"^(?P<t_type>(expense|revenue))/edit/(?P<transaction_id>\d+)$",
    transaction_edit,
    name="transaction_edit",
),
url(
    r"^(?P<t_type>(expense|revenue))/delete/(?P<transaction_id>\d+)$",
    transaction_delete,
    name="transaction_delete",
),
"""