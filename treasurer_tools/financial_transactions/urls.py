"""Expense Transaction URLs"""
from django.conf.urls import url

from .views import (
    dashboard, transaction_add, transaction_edit, transaction_delete, retrieve_financial_code_systems
)
# pylint: disable=invalid-name
urlpatterns = [
    url(r"^(?P<t_type>(expense|revenue))/add/$", transaction_add, name="add",),
    url(r"^(?P<t_type>(expense|revenue))/edit/(?P<transaction_id>\d+)$", transaction_edit, name="edit",),
    url(r"^(?P<t_type>(expense|revenue))/delete/(?P<transaction_id>\d+)$", transaction_delete, name="delete",),
    url(r"^expense/add/retrieve-financial-code-systems/$", retrieve_financial_code_systems),
    url(r"^expense/edit/retrieve-financial-code-systems/$", retrieve_financial_code_systems),
    url(r"^revenue/add/retrieve-financial-code-systems/$", retrieve_financial_code_systems),
    url(r"^revenue/edit/retrieve-financial-code-systems/$", retrieve_financial_code_systems),
    url(r"^$", dashboard, name="dashboard"),
]
