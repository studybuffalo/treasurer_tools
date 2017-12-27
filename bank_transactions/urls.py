"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, statement_add, statement_edit, statement_delete, settings
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^statement/add$", statement_add, name="statement_add"),
    url(
        r"^statement/edit/(?P<statement_id>\d+)$",
        statement_edit,
        name="statement_edit"
    ),
    url(
        r"^statement/delete/(?P<statement_id>\d+)$",
        statement_delete,
        name="statement_delete"
    ),
    url(r"^$", dashboard, name="bank_dashboard"),
]