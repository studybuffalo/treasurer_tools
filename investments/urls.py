"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, investment_add, investment_edit, investment_delete
)
# pylint: disable=invalid-name
urlpatterns = [
    url(
        r"^add$",
        investment_add,
        name="investment_add",
    ),
    url(
        r"^edit/(?P<investment_id>\d+)$",
        investment_edit,
        name="investment_edit",
    ),
    url(
        r"^delete/(?P<investment_id>\d+)$",
        investment_delete,
        name="investment_delete",
    ),
    url(r"^$", dashboard, name="investments_dashboard"),
]
