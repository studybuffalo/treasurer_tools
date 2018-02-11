"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, statement_add, statement_edit, statement_delete
)

# pylint: disable=invalid-name
urlpatterns = [
    url(r"^statement/add/$", statement_add, name="add"),
    url(r"^statement/edit/(?P<statement_id>\d+)$", statement_edit, name="edit"),
    url(r"^statement/delete/(?P<statement_id>\d+)$", statement_delete, name="delete"),
    url(r"^$", dashboard, name="dashboard"),
]
